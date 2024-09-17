import json
import os


def read_jsonl_files(folder):
    jsonl_files = sorted([f for f in os.listdir(folder) if f.endswith(".jsonl")])
    print(jsonl_files, len(jsonl_files))
    data = {}
    for file in jsonl_files:
        print("Reading file: ", file)
        with open(os.path.join(folder, file), "r") as f:
            data[file.split(".")[0]] = [json.loads(line) for line in f]
    return data


data_folder = "Data/ToMFiltration-russian"
result_file_path = "Data/russian_cultural_data_raw.csv"

data = read_jsonl_files(data_folder)

refined_data = []
serial = 0
for key, value in data.items():
    for item in value:

        d = {
            "INDEX": serial,
            "ABILITY": item.get("ABILITY", None),
            "ORIGIN_FILE": key,
            "DATA_INDEX": item.get("INDEX", None),
            "STORY": item.get("STORY", None),
            "QUESTION": item.get("QUESTION", None),
            "OPTION-A": item.get("OPTION-A", None),
            "OPTION-B": item.get("OPTION-B", None),
            "OPTION-C": item.get("OPTION-C", "nan"),  # Use NaN if missing
            "OPTION-D": item.get("OPTION-D", "nan"),  # Use NaN if missing
            "ANSWER": item.get("ANSWER", None),
        }

        refined_data.append(d)
        serial += 1

# for key, value in data.items():
#     for item in value:

#         d = {
#             "INDEX": serial,
#             "ABILITY": item.get("能力\nABILITY", None),
#             "ORIGIN_FILE": key,
#             "DATA_INDEX": item.get("序号\nINDEX", None),
#             "STORY": item.get("故事", None),
#             "QUESTION": item.get("问题", None),
#             "OPTION-A": item.get("选项A", "nan"),
#             "OPTION-B": item.get("选项B", "nan"),
#             "OPTION-C": item.get("选项C", "nan"),  # Use NaN if missing
#             "OPTION-D": item.get("选项D", "nan"),  # Use NaN if missing
#             "ANSWER": item.get("答案\nANSWER", None),
#         }

#         refined_data.append(d)
#         serial += 1

import pandas as pd

df = pd.DataFrame(refined_data)
df.to_csv(result_file_path, index=False)
