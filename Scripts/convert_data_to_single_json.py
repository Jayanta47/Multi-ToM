import json
import os


def read_jsonl_files(folder):
    jsonl_files = [f for f in os.listdir(folder) if f.endswith(".jsonl")]
    print(jsonl_files, len(jsonl_files))
    data = {}
    for file in jsonl_files:
        with open(os.path.join(folder, file), "r") as f:
            data[file.split(".")[0]] = [json.loads(line) for line in f]
    return data


data = read_jsonl_files("Data/RawData")

refined_data = []
serial = 0
for key, value in data.items():
    for item in value:
        d = {
            "INDEX": serial,
            "ABILITY": item["能力\nABILITY"],
            "DATA_INDEX": item["序号\nINDEX"],
            "STORY": item["STORY"],
            "QUESTION": item["QUESTION"],
            "OPTION-A": item["OPTION-A"],
            "OPTION-B": item["OPTION-B"],
            "OPTION-C": item["OPTION-C"],
            "OPTION-D": item["OPTION-D"],
            "ANSWER": item["答案\nANSWER"],
        }

        refined_data.append(d)
        serial += 1

import pandas as pd

df = pd.DataFrame(refined_data)
df.to_csv("Data/RefinedData/data.csv", index=False)
