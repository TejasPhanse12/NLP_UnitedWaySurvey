'''
The main goal of this file is to convert docx files to txt files. This is done using the python-docx library, 
which allows us to read the contents of a docx file and write it to a txt file. The code is structured in a way that it can be 
easily modified to include additional functionality, such as handling different file formats or adding error handling.
'''
# Import nessary libraries
import os
from docx import Document


input_folder = "UWSM Community Input Transcripts"
output_folder = "UWSM_Input_Transcaripts_txt" 

# Create output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

print("--"*50)
print("Starting conversion process...")
print("--"*50)

# Function to extract text from tables in the docx file
def extract_table_text(table):
    lines = []
    for row in table.rows:
        row_text = " ".join(cell.text.strip() for cell in row.cells if cell.text.strip())
        if row_text:
            lines.append(row_text)
    return "\n".join(lines)

# Iterate through all docx files in the input folder and convert them to txt files
for filename in os.listdir(input_folder):
    if filename.endswith(".docx"):
        doc = Document(os.path.join(input_folder, filename))
        content = []

        for block in doc.element.body:
            tag = block.tag.split("}")[-1]
            if tag == "p":
                para = block.text.strip()
                if para:
                    content.append(para)
            elif tag == "tbl":
                for table in doc.tables:
                    if table._element is block:
                        content.append(extract_table_text(table))
                        break

        txt_filename = filename.replace(".docx", ".txt")
        with open(os.path.join(output_folder, txt_filename), "w", encoding="utf-8") as f:
            f.write("\n".join(content))

        print(f"Converted {filename} to {txt_filename}")

print("--"*50)
print("Conversion process completed!")
print("--"*50)