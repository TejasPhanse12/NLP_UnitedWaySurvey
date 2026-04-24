'''
The Main goal in this file is to convert the raw txt files into a csv file that can be used for further analysis. 
This is done using the pandas, regex, os libraries, which allows us to easily manipulate and analyze data in a tabular format. 
The code is structured in a way that it can be easily modified to include additional functionality, such as handling multiple .text files or adding error handling.
'''

# Import necessary libraries
import os
import re
import pandas as pd
import numpy as np

# Define input and output paths
input_folder = "UWSM_Input_Transcaripts_txt"
output_file = "data/UWSM_Community_Input_Transcripts.csv"

# Field extraction patterns 
'''
Each pattern captures everything after the label up to the end of that line. re.IGNORECASE handles any casing inconsistencies across files.
'''

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
    r"(?:SUMMARY\s+KEYWORDS|CORE\s+THEMES:)\s*\n([\s\S]+?)(?:\n\s*\n|$)",
    re.IGNORECASE
)

CONVERSATION_PATTERN = re.compile(
    r"((?:Speaker\s*1|Transcript|Core Ideas:)\b[\s\S]+)",
    re.IGNORECASE
)

# Initialize an empty list to hold the extracted data dictionaries
data = {
    "File Name": [],
    "Name of Facilitator(s)": [],
    "Date of Conversation": [],
    "Name of Organization/Group": [],
    "Meeting Location": [],
    "Length of Time": [],
    "Number of Attendees": [],
    "Population": [],
    "Summary Keywords": [],
    "Conversation": [],
}

# Detects if a captured value is actually a field label from the next line
FIELD_LABEL_BLEED = re.compile(
    r"^\s*(?:"
    r"Name\s+of\s+Facilitator"
    r"|Date\s+of\s+[Cc]onversation"
    r"|Name\s+of\s+Organization"
    r"|Meeting(?:\s+Details)?"
    r"|Length\s+of\s+[Tt]ime"
    r"|Number\s+of\s+[Aa]ttendees"
    r"|Population"
    r")\s*[:/]",
    re.IGNORECASE
)

def extract_fields(text: str) -> dict:
    """Extract fields from text, returning NaN for missing, blank, newline-only, or bled values."""
    result = {}
    for field, pattern in FIELD_PATTERNS.items():
        match = pattern.search(text)
        if match:
            lines = [line.strip() for line in match.group(1).splitlines() if line.strip()]
            value = " ".join(lines)
            # ← If value looks like a field label, it's bleed — kill it
            if not value or FIELD_LABEL_BLEED.match(value):
                result[field] = np.nan
            else:
                result[field] = value
        else:
            result[field] = np.nan
    return result

# Define a for loop to process each file from input folder into a dictionary and then into a dataframe
for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
            text = f.read()

        text = re.sub(r"Fill\s+out\s+this\s*:\s*", "", text, flags=re.IGNORECASE)

        data["File Name"].append(filename)

        # store result in a separate variable, then append each field into data
        fields = extract_fields(text)
        for field in FIELD_PATTERNS:
            data[field].append(fields[field])

        keywords_match = KEYWORDS_PATTERN.search(text)
        data["Summary Keywords"].append(
            keywords_match.group(1).strip() if keywords_match else np.nan
        )

        conversation_match = CONVERSATION_PATTERN.search(text)
        data["Conversation"].append(
            conversation_match.group(1).strip() if conversation_match else np.nan
        )

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)

df.sort_values("File Name", inplace=True)

# Save the DataFrame to a CSV file
df.to_csv(output_file, index=False)