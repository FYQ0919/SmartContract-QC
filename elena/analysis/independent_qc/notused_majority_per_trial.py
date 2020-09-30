import ast
import os
import pandas as pd


data_folder = "../../data"
input_filename = "simulation_2_input_18"
workpiece_list = [f"wp_{idx + 1}" for idx in range(5)]
threshold_list = [3, 5, 7, 9, 11, 13, 15, 17]
trial_list = list(range(1))
input_folder = f"{data_folder}/{input_filename}"
output_folder = f"{data_folder}/postprocessed/simulation_2/per_workpiece"
if not os.path.exists(output_folder):
    # Create target Directory
    os.makedirs(output_folder)
    print("Directory ", output_folder,  " Created ")
else:
    print("Directory ", output_folder,  " already exists")

for trial in trial_list:    # Each trial
    trial += 1
    writer = pd.ExcelWriter(f"{output_folder}/results_{input_filename}_trial_{trial}.xlsx", mode="w")
    for workpiece in workpiece_list:
        prefix = f"{workpiece}_"
        data = {
            "threshold": [],
            "TP": [],
            "TN": [],
            "FP": [],
            "FN": [],
            "production_time": [],
            "transport_time": [],
            "inspection_time": [],
            "network_time": [],
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
        compiled_df = pd.DataFrame(data)
        for threshold in threshold_list:
            suffix = f"_{threshold}.csv"
            for folder in os.listdir(f"{input_folder}/{trial}"):     # Each datetime folder
                print(folder)
                for filename in os.listdir(f"{input_folder}/{trial}/{folder}"):  # Each results
                    print(filename)
                    data = dict()
                    if filename.startswith(prefix) and filename.endswith(suffix):
                        df = pd.read_csv(f"{input_folder}/{trial}/{folder}/{filename}")
                        consent_df = df[df["consent"] == 1]
                        # Compile qc score through row by row iteration
                        for row in consent_df.itertuples():
                            print(row)
                            winner_qc_list = row.winner_qc_list
                            winner_qc_list = ast.literal_eval(winner_qc_list)
                            for qc, score in winner_qc_list:
                                data[qc] = score    # Keep overwriting the score until the last time the qc appear
                        # Get confusion matrix data
                        tp_df = consent_df[(consent_df["actual_quality"] == "Fail") & (consent_df["qc_results"] == "['Fail']")]
                        tn_df = consent_df[(consent_df["actual_quality"] == "Pass") & (consent_df["qc_results"] == "['Pass']")]
                        fp_df = consent_df[(consent_df["actual_quality"] == "Fail") & (consent_df["qc_results"] == "['Pass']")]
                        fn_df = consent_df[(consent_df["actual_quality"] == "Pass") & (consent_df["qc_results"] == "['Fail']")]
                        data["threshold"] = threshold
                        data["TP"] = len(tp_df)
                        data["TN"] = len(tn_df)
                        data["FP"] = len(fp_df)
                        data["FN"] = len(fn_df)
                        data["production_time"] = df.production_time.sum()
                        data["transport_time"] = df.transport_time.sum()
                        data["inspection_time"] = df.inspection_time.sum()
                        # Normalizing network time, which is elapsed time per RESTapi request
                        network_time_unit = df.loc[df["network_time"].first_valid_index()]["network_time"] # first value
                        data["network_time"] = df.network_time.sum()/network_time_unit * 0.003  # each unit is 0.003 s
                        print(data)
                        compiled_df = compiled_df.append(data, ignore_index=True)
        compiled_df.to_excel(writer, sheet_name=workpiece, index=False)
    writer.save()
    writer.close()
