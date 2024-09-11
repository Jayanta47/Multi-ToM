import os
import json

def fix_jsonl(file_path, output_path):
    with open(file_path, 'r') as f:
        content = f.read()

    fixed_lines = []
    current_json = ""
    
    # Read the content and construct JSON objects
    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        
        current_json += line
        
        try:
            # Try to load the current json object, if successful, save it
            json_obj = json.loads(current_json)
            fixed_lines.append(json.dumps(json_obj))
            current_json = ""  # Reset for the next object
        except json.JSONDecodeError:
            # Incomplete JSON object, keep concatenating lines
            continue

    # Write the fixed JSON objects to the new jsonl file
    with open(output_path, 'w') as f:
        for line in fixed_lines:
            f.write(line + "\n")

def process_folder(source_folder, destination_folder):
    # Ensure the destination folder exists
    os.makedirs(destination_folder, exist_ok=True)
    
    # Loop through all the files in the source folder
    for filename in os.listdir(source_folder):
        if filename.endswith('.jsonl'):
            # Define the full path for both input and output
            input_file_path = os.path.join(source_folder, filename)
            output_file_path = os.path.join(destination_folder, filename)
            
            # Process each file
            fix_jsonl(input_file_path, output_file_path)
            print(f"Processed: {filename}")

# Paths to your source and destination folders
source_folder = 'Data/ToMFiltration-russian/'
destination_folder = 'Data/ToMFiltration-russian-fixed/'

# Call the function to process all the files
process_folder(source_folder, destination_folder)
