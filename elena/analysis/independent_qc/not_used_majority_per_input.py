import os
import pandas as pd


data_folder = "../../data"
workpiece_list = [f"wp_{idx + 1}" for idx in range(20)]
threshold_list = [3, 5, 7, 9, 11, 13, 15, 17]
# threshold_list = [0.9]
input_filename = "simulation_2_input_18"
input_folder = f"{data_folder}/postprocessed/simulation_2/per_workpiece"
output_folder = f"{data_folder}/postprocessed/simulation_2/per_input"
if not os.path.exists(output_folder):
    # Create target Directory
    os.makedirs(output_folder)
    print("Directory ", output_folder,  " Created ")
else:
    print("Directory ", output_folder,  " already exists")

header = {
    "threshold": [],
    "TP": [],
    "TN": [],
    "FP": [],
    "FN": [],
    "production_time": [],
    "transport_time": [],
    "inspection_time": [],
    "network_time": [],
}
writer = pd.ExcelWriter(f"{output_folder}/results_{input_filename}.xlsx", mode="w")
for filename in os.listdir(input_folder):   # Each results for each trial
    if "3trials" in filename:
        continue
    if f"{input_filename}_" in filename:
        trial = filename[len(f"results_{input_filename}_"):].strip(".xlsx")
        additional_header = {
            "wc_1": [],
            "wc_2": [],
            "wc_3": [],
            "wc_4": [],
            "wc_5": [],
            "wc_6": [],
            "wc_7": [],
            "wc_8": [],
            "wc_9": [],
            "wc_10": [],
            "wc_11": [],
            "wc_12": [],
            "wc_13": [],
            "wc_14": [],
            "wc_15": [],
            "wc_16": [],
            "wc_17": [],
        }
        temp = header.copy()
        temp.update(additional_header)
        compiled_df = pd.DataFrame(temp)
        sheets_dict = pd.read_excel(f"{input_folder}/{filename}", sheet_name=None)
        df = pd.concat(sheets_dict.values())
        for threshold in threshold_list:
            data = dict()
            filtered_df = df[df["threshold"] == threshold]
            data["threshold"] = threshold
            data["TP"] = filtered_df["TP"].sum()
            data["TN"] = filtered_df["TN"].sum()
            data["FP"] = filtered_df["FP"].sum()
            data["FN"] = filtered_df["FN"].sum()
            data["production_time"] = filtered_df.production_time.sum()
            data["transport_time"] = filtered_df.transport_time.sum()
            data["inspection_time"] = filtered_df.inspection_time.sum()
            data["network_time"] = filtered_df.network_time.sum()
            for key in additional_header.keys():
                print(filtered_df[key])
                data[key] = filtered_df[filtered_df[key].notnull()][key].values[-1]
            compiled_df = compiled_df.append(data, ignore_index=True)
        print(compiled_df)
        compiled_df.to_excel(writer, sheet_name=trial, index=False)
writer.save()
# Average the data
additional_header = {
    "accuracy": [],
    "miss": [],
    "precision": [],
    "recall": [],
    "F1": [],
    "transport_time_norm": [],
    "inspection_time_norm": [],
    "network_time_norm": [],
}
temp = header.copy()
temp.update(additional_header)
compiled_df = pd.DataFrame(temp)
sheets_dict = pd.read_excel(f"{output_folder}/results_{input_filename}.xlsx", sheet_name=None)
df = pd.concat(sheets_dict.values())
for threshold in threshold_list:
    data = dict()
    filtered_df = df[df["threshold"] == threshold]
    data["threshold"] = threshold
    data["TP"] = filtered_df["TP"].sum()/len(sheets_dict)
    data["TN"] = filtered_df["TN"].sum()/len(sheets_dict)
    data["FP"] = filtered_df["FP"].sum()/len(sheets_dict)
    data["FN"] = filtered_df["FN"].sum()/len(sheets_dict)
    data["accuracy"] = (data["TP"] + data["TN"]) / (data["TP"] + data["TN"] + data["FP"] + data["FN"])
    data['miss'] = data["FN"] / (data["TP"] + data["FN"])
    data['precision'] = data["TP"] / (data["TP"] + data["FP"])
    data['recall'] = data["TP"] / (data["TP"] + data["FN"])
    data['F1'] = 2 * data["TP"] / (2 * data["TP"] + data["FP"] + data["FN"])
    data["production_time"] = filtered_df.production_time.sum()/len(sheets_dict)
    data["transport_time"] = filtered_df.transport_time.sum()/len(sheets_dict)
    data["inspection_time"] = filtered_df.inspection_time.sum()/len(sheets_dict)
    data["network_time"] = filtered_df.network_time.sum()/len(sheets_dict)
    data["transport_time_norm"] = data["transport_time"]/data["production_time"]
    data["inspection_time_norm"] = data["inspection_time"]/data["production_time"]
    data["network_time_norm"] = data["network_time"]/data["production_time"]
    compiled_df = compiled_df.append(data, ignore_index=True)
# print(compiled_df)
compiled_df.to_excel(writer, sheet_name="average", index=False)
writer.save()
writer.close()


