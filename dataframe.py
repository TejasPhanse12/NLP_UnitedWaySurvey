import os
import re
import pandas as pd
import numpy as np

# Define input and output paths
input_folder = "UWSM_Input_Transcaripts_txt"
output_file = "data/UWSM_Community_Input_Transcripts_Split.csv"

# Metadata extraction patterns
FIELD_PATTERNS = {
    "Name of Facilitator(s)": re.compile(
        r"^\s*Name\s+of\s+Facilitator(?:\(s\))?\s*:\s*(.*)",
        re.IGNORECASE | re.MULTILINE
    ),
    "Date of Conversation": re.compile(
        r"^\s*Date\s+of\s+conversation\s*:\s*(.*)",
        re.IGNORECASE | re.MULTILINE
    ),
    "Name of Organization/Group": re.compile(
        r"^\s*Name\s+of\s+Organization/(?:Group|Population)\s*[:;]\s*([^\n]*)",
        re.IGNORECASE | re.MULTILINE
    ),
    "Meeting Location": re.compile(
        r"^\s*Meeting(?:\s+Details)?\s*,?\s*location\s*:?\s*([^\n]*)",
        re.IGNORECASE | re.MULTILINE
    ),
    "Length of Time": re.compile(
        r"^\s*Length\s+of\s+time\s*:\s*(.*)",
        re.IGNORECASE | re.MULTILINE
    ),
    "Number of Attendees": re.compile(
        r"^\s*Number\s+of\s+attendees\s*:\s*(.*)",
        re.IGNORECASE | re.MULTILINE
    ),
    "Population": re.compile(
        r"^\s*(?:Population|Name\s+of\s+Organization/Population)(?:\s*-\s*[^:]+)?\s*:\s*([^\n]*)",
        re.IGNORECASE | re.MULTILINE
    ),
}

KEYWORDS_PATTERN = re.compile(
    r"(?:SUMMARY\s+KEYWORDS|CORE\s+THEMES:)\s*\n([\s\S]+?)(?=\n\s*(?:Speaker|SPEAKERS|Name of Facilitator)|$)",
    re.IGNORECASE | re.MULTILINE
)

FIELD_LABEL_BLEED = re.compile(
    r"^\s*(?:"
    r"Name\s+of\s+Facilitator"
    r"|Date\s+of\s+[Cc]onversation"
    r"|Name\s+of\s+Organization"
    r"|Meeting(?:\s+Details)?"
    r"|Length\s+of\s+[Tt]ime"
    r"|Number\s+of\s+[Aa]ttendees"
    r"|Population"
    r"|Connected"
    r"|SPEAKERS"
    r"|SUMMARY\s+KEYWORDS"
    r")\s*[:/]",
    re.IGNORECASE
)

# Robust speaker detection
# Priority 1: Explicit "Speaker X"
# Priority 2: Capitalized names on their own line (very common in these transcripts)
SPEAKER_PATTERN = re.compile(
    r"^\s*(Speaker\s+\d+|(?:Speaker\s+)?[A-Z][a-z]+(?:[,\s]+[A-Z][a-z]+){0,2})\s*$", 
    re.MULTILINE
)

def extract_metadata(text: str) -> dict:
    """Extract metadata fields from text."""
    result = {}
    for field, pattern in FIELD_PATTERNS.items():
        match = pattern.search(text)
        if match:
            lines = [line.strip() for line in match.group(1).splitlines() if line.strip()]
            value = " ".join(lines)
            if not value or FIELD_LABEL_BLEED.match(value):
                result[field] = np.nan
            else:
                result[field] = value
        else:
            result[field] = np.nan
            
    keywords_match = KEYWORDS_PATTERN.search(text)
    if keywords_match:
        kw = keywords_match.group(1).strip()
        kw = re.split(r'\n\s*\n', kw)[0]
        kw = re.split(r'\n\s*(?:Speaker|SPEAKERS|Name of Facilitator)', kw)[0].strip()
        result["Summary Keywords"] = kw
    else:
        result["Summary Keywords"] = np.nan
    return result

def split_conversation(text: str):
    """Split text into speaker and conversation blocks."""
    # Find where metadata ends.
    # We look for "SPEAKERS" list or the first "Speaker 1"
    speakers_match = re.search(r"^SPEAKERS\s*$", text, re.MULTILINE | re.IGNORECASE)
    
    start_pos = 0
    if speakers_match:
        # Skip the SPEAKERS header and the next 1-2 lines (the list of speaker names)
        # Often: 
        # SPEAKERS
        # Speaker 1, Speaker 2...
        lines = text[speakers_match.end():].split('\n', 3)
        if len(lines) > 2:
            start_pos = text.find(lines[2], speakers_match.end())
        else:
            start_pos = speakers_match.end()
    else:
        # Fallback: find first "Speaker 1"
        s1_match = re.search(r"^\s*Speaker\s+1\s*$", text, re.MULTILINE | re.IGNORECASE)
        if s1_match:
            start_pos = s1_match.start()
            
    conv_text = text[start_pos:]
    
    # Split by speaker pattern
    parts = SPEAKER_PATTERN.split(conv_text)
    
    rows = []
    # parts[0] is text before first speaker match
    i = 1
    while i < len(parts):
        speaker = parts[i].strip()
        content = parts[i+1].strip() if i+1 < len(parts) else ""
        
        # Final safety check on speaker name
        if speaker and content and not FIELD_LABEL_BLEED.match(speaker) and len(speaker) < 40:
            rows.append({
                "Speaker": speaker,
                "Text": content.replace('\n', ' ') # Flatten multi-line text for CSV
            })
        i += 2
        
    return rows

if __name__ == "__main__":
    all_rows = []
    
    filenames = [f for f in os.listdir(input_folder) if f.endswith(".txt")]
    filenames.sort()
    
    for filename in filenames:
        file_path = os.path.join(input_folder, filename)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        except UnicodeDecodeError:
            with open(file_path, "r", encoding="latin-1") as f:
                text = f.read()
            
        text = re.sub(r"Fill\s+out\s+this\s*:\s*", "", text, flags=re.IGNORECASE)
        
        metadata = extract_metadata(text)
        metadata["Source File"] = filename
        
        conversation_rows = split_conversation(text)
        
        for conv in conversation_rows:
            row = metadata.copy()
            row.update(conv)
            all_rows.append(row)
            
    df = pd.DataFrame(all_rows)
    
    # Reorder columns
    cols = ["Source File"] + list(FIELD_PATTERNS.keys()) + ["Summary Keywords", "Speaker", "Text"]
    df = df[cols]
    
    # Save to CSV
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    df.to_csv(output_file, index=False)
    print(f"Saved {len(df)} rows to {output_file}")
