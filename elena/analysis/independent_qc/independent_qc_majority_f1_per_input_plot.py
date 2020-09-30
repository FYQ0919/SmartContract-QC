import os
import pandas as pd
import matplotlib.pyplot as plt


data_folder = "../../data"
num_of_workpiece = 5
workpiece_list = [f"wp_{idx + 1}" for idx in range(num_of_workpiece)]
score_type = "majority"
input_filename = "input_12"
majority_folder = f"{data_folder}/postprocessed/independent_qc/{score_type}/{num_of_workpiece}_workpiece/per_input"
output_folder = f"{data_folder}/postprocessed/independent_qc/{score_type}/{num_of_workpiece}_workpiece/graph"
if not os.path.exists(output_folder):
    # Create target Directory
    os.makedirs(output_folder)
    print("Directory ", output_folder,  " Created ")
else:
    print("Directory ", output_folder,  " already exists")

majority_df = pd.read_excel(
    f"{majority_folder}/independent_qc_{score_type}_{num_of_workpiece}_workpiece_{input_filename}.xlsx", sheet_name="average")
fig = plt.figure()
ax1 = fig.add_subplot(111)
p1 = ax1.plot(
    majority_df.threshold,
    majority_df.F1,
    c='black',
    label="F1",
)
y = [0.7, 1.00]
x = [2, 18]
ax1.set_ylabel('F1', fontsize=15)
ax1.set_xlabel('Threshold', fontsize=15)
ax1.set_ylim(y)
ax1.set_xlim(x)
ax1.set_xticks(range(1, 17, 2))
# ax1.set_xticklabels([3, 5, ])
# leg = plt.legend(labels=(["True capability", ]), loc='upper left')
# leg = plt.legend(loc='upper left')
# ax2 = ax1.twinx()
plt.savefig(f"{output_folder}/{input_filename}")
# plt.show()

