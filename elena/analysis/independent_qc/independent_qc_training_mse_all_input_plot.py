import os
import pandas as pd
import matplotlib.pyplot as plt

data_folder = "../../data"
num_of_workpiece = 20
workpiece_list = [f"wp_{idx + 1}" for idx in range(num_of_workpiece)]
workcell_list = [f"wc_{idx + 1}" for idx in range(17)]
input_filename = "input_20"
score_type = "independent_qc"
threshold = 0.9
input_folder = f"{data_folder}/postprocessed/independent_qc/{score_type}/{num_of_workpiece}_workpiece/per_input"
output_folder = f"{data_folder}/postprocessed/independent_qc/{score_type}/{num_of_workpiece}_workpiece/graph/"
if not os.path.exists(output_folder):
    # Create target Directory
    os.makedirs(output_folder)
    print("Directory ", output_folder,  " Created ")
else:
    print("Directory ", output_folder,  " already exists")

fig, ax = plt.subplots(3, 7)
fig.suptitle('MSE vs QC iteration subplots')
row = 0
col = 0
col_lim = 6
for idx, filename in enumerate(os.listdir(f"{input_folder}")):  # Each datetime folder
    if filename.endswith(".xlsx"):
        if idx > col_lim:
            row += 1
            col = 0
            col_lim += col_lim
        # Plot individual MSE curve
        print(row, col)
        df = pd.read_excel(f"{input_folder}/{filename}")
        ax[row, col].plot(df.qc_iteration, df.MSE, color="black")
        # ax[row, col].set_ylabel('MSE', fontsize=5)
        # ax[row, col].set_xlabel('QC Iteration', fontsize=5)
        ax[row, col].set_ylim([0, 0.5])
        ax[row, col].set_xlim([0, 800])
        col += 1
plt.savefig(f"{output_folder}/all")
plt.show()
