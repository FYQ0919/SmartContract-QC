import os
import shutil

data_folder = "../data"
sim_num = 2
input_folder = f"{data_folder}"
for idx, folder in enumerate(os.listdir(f"{input_folder}")):  # Each datetime folder
    if f"simulation_{sim_num}_" in folder and os.path.exists(f"{input_folder}/{folder}/test"):
        folder_name = os.listdir(f"{input_folder}/{folder}/test")[0]
        src_file = f"{input_folder}/{folder}/test/{folder_name}"
        dst_file = f"{input_folder}/{folder}/score/{folder_name}"
        # os.rename(src_file, dst_file)
        shutil.copytree(src_file, dst_file)
