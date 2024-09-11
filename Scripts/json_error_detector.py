import json

def read_jsonl(file_path):
    with open(file_path, 'r') as f:
        for i, line in enumerate(f, 1):
            try:
                # Attempt to load each line as JSON
                json_obj = json.loads(line)
            except json.JSONDecodeError as e:
                print(f"Error in line {i}: {line.strip()}")
                print(f"Error message: {e}")
                break  # Optionally, stop after the first error

# Provide your JSONL file path
file_path = '/Data/ToMFiltration-english/False Belief Task.jsonl'
read_jsonl(file_path)
