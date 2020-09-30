import os
import pandas as pd
import matplotlib.pyplot as plt

data_folder = "../data"
workpiece_list = ["wp_1", "wp_2", "wp_3", "wp_4", "wp_5"]
threshold_list = [3, 5, 7, 9, 11, 13, 15, 17, 0.7, 0.8, 0.9]
# threshold_list = [0.7, 0.8, 0.9]
input_filename = "simulation_2_input_6"
input_folder = f"../input_5_workpiece"
output_folder = f"{data_folder}/postprocessed"
if not os.path.exists(output_folder):
    # Create target Directory
    os.makedirs(output_folder)
    print("Directory ", output_folder,  " Created ")
else:
    print("Directory ", output_folder,  " already exists")

workcells = [f"wc_{i+1}" for i in range(17)]
header = {
    "input": [],
}
for wc_id in workcells:
    header[wc_id] = list()

writer = pd.ExcelWriter(f"{output_folder}/qc_capability.xlsx", mode="w")
compiled_df = pd.DataFrame(header)
for filename in os.listdir(input_folder):   # Each input sheet
    df = pd.read_csv(f"{input_folder}/{filename}")
    data = dict()
    data["input"] = int(filename[len("simulation_2_input_"):(len(filename) - len(".csv"))])
    for wc_id in workcells:
        data[wc_id] = df.iloc[0][f"qc_{wc_id}_confidence"]
    compiled_df = compiled_df.append(data, ignore_index=True)
# Transpose
compiled_df = compiled_df.sort_values(by=['input'], ignore_index=True)
compiled_df = compiled_df.set_index('input').transpose().reset_index()
# Write to excel
compiled_df.to_excel(writer, sheet_name="data", index=False)
print(compiled_df)
# Output box plot
bp = compiled_df.boxplot(
    column=sorted([
        int(filename[len("simulation_2_input_"):(len(filename) - len(".csv"))])
        for filename in os.listdir(input_folder)
    ]),
    grid=False,
    fontsize=12,
    return_type='dict'
)
# Style box plot
[item.set_color('k') for item in bp['boxes']]
[item.set_color('k') for item in bp['fliers']]
[item.set_color('k') for item in bp['medians']]
[item.set_color('k') for item in bp['whiskers']]
# Adjust axis
ax = plt.gca()
ax.set_ylabel('QC Capability', fontsize=15)
ax.set_xlabel('Input', fontsize=15)
# Show plot
plt.show()
# Analyze
analysis_df = pd.DataFrame({
    "input": [],
})
analysis_df = analysis_df.set_index('input').transpose().reset_index()
data_df = compiled_df.copy()
analysis_df = analysis_df.append(data_df.mean(), ignore_index=True)
analysis_df.iloc[-1, 0] = "mean"
analysis_df = analysis_df.append(data_df.quantile(q=0.25), ignore_index=True)
analysis_df.iloc[-1, 0] = "0.25Q"
analysis_df = analysis_df.append(data_df.quantile(q=0.5), ignore_index=True)
analysis_df.iloc[-1, 0] = "0.50Q"
analysis_df = analysis_df.append(data_df.quantile(q=0.75), ignore_index=True)
analysis_df.iloc[-1, 0] = "0.75Q"
analysis_df = analysis_df.append(data_df.min(), ignore_index=True)
analysis_df.iloc[-1, 0] = "min"
analysis_df = analysis_df.append(data_df.max(), ignore_index=True)
analysis_df.iloc[-1, 0] = "max"
analysis_df.to_excel(writer, sheet_name="analysis", index=False)
# Save
writer.save()
writer.close()

df = pd.read_excel(f"{output_folder}/qc_capability.xlsx", sheet_name=None)
print(df)