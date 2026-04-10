'''
The Main goal in this file is to convert the raw txt files into a csv file that can be used for further analysis. 
This is done using the pandas, regex, os libraries, which allows us to easily manipulate and analyze data in a tabular format. 
The code is structured in a way that it can be easily modified to include additional functionality, such as handling multiple .text files or adding error handling.
'''

# Import nessary libraries
import os
import re
import pandas as pd

# Define input and output paths
input_folder = "UWSM_Input_Transcaripts_txt"
output_file = "data/UWSM_Community_Input_Transcripts.csv"

# Field extraction patterns 
'''
Each pattern captures everything after the label up to the end of that line. re.IGNORECASE handles any casing inconsistencies across files.
'''

import re
import os
import pandas as pd

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
    r"((?:Speaker\s*1|Transcript)\b[\s\S]+)",
    re.IGNORECASE
)

# Initialize an empty list to hold the extracted data dictionaries
data = {
    "File Name" : [], 
    "Name of Facilitator(s)" : [],
    "Date of Conversation" :[],
    "Name of Organization/Group":[],
    "Meeting Location":[],
    "Length of Time":[],
    "Number of Attendees":[],
    "Population":[],
    "Summary Keywords":[],
    "Conversation":[],
}  

# Defineing a for loop to process each file from input folder into a dictionary and then into a dataframe

for filename in os.listdir(input_folder):
    if filename.endswith(".txt"):
        with open(os.path.join(input_folder, filename), "r", encoding="utf-8") as f:
            text = f.read()

        # Header-only slice prevents false matches inside transcript body
        #header_text = "\n".join(text.splitlines()[:HEADER_LINE_LIMIT])

        data["File Name"].append(filename)

        text = re.sub(r"Fill\s+out\s+this\s*:\s*", "", text, flags=re.IGNORECASE)

        for field, pattern in FIELD_PATTERNS.items():
            match = pattern.search(text)  
            data[field].append(match.group(1).strip() if match and match.group(1).strip() else "N/A")

        keywords_match = KEYWORDS_PATTERN.search(text)  
        data["Summary Keywords"].append(
            keywords_match.group(1).strip() if keywords_match else "N/A"
        )

        # Conversation still searches full text — it needs the whole file
        conversation_match = CONVERSATION_PATTERN.search(text)
        data["Conversation"].append(
            conversation_match.group(1).strip() if conversation_match else "N/A"
        )

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)

# Save the DataFrame to a CSV file
df.to_csv(output_file, index=False)