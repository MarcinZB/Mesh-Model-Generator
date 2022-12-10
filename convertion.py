import whitebox as wb
import os
from tkinter import filedialog
import pandas as pd
import math

global selected_file
global name_of_file
global selected_output_folder
filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("ASCII",
                                                      "*.xyz*"),
                                                     ("all files",
                                                      "*.*")))
selected_file = filename
name_of_file = os.path.basename(filename)
print(filename)
selected_output_folder = filedialog.askdirectory()

dfs = []
tools = wb.WhiteboxTools()

if selected_file.endswith(".csv"):
    print("It is already a csv file.")
else:
    print("Calculating...")
    tools.las_to_ascii(selected_file)
    
catalog_of_file = os.path.dirname(selected_file)
print("The file is placed in:" f"{catalog_of_file}")

for file in os.listdir(catalog_of_file):
    if file.endswith(".csv"):
        name_of_file = os.path.basename(file)
        print(name_of_file)

absolute_path = f"{catalog_of_file}/{name_of_file}"
dfs.append(pd.read_csv(absolute_path))
used_csv = dfs[0]
additional_csv = dfs[0]
print(additional_csv)
additional_delete_csv = additional_csv.drop(additional_csv.columns[3:12], axis=1)
print(used_csv)
deleted_csv = used_csv.drop(used_csv.columns[3:9], axis=1)
print(deleted_csv)
print(additional_delete_csv)

new_column_red = deleted_csv['RED'].apply(lambda r: math.trunc(r * 255 / 65535))
new_column_green = deleted_csv['GREEN'].apply(lambda g: math.trunc(g * 255 / 65535))
new_column_blue = deleted_csv['BLUE'].apply(lambda b: math.trunc(b * 255 / 65535))

additional_delete_csv['RED'] = new_column_red
additional_delete_csv['GREEN'] = new_column_green
additional_delete_csv['BLUE'] = new_column_blue

print(f"Final csv:\n {additional_delete_csv}")
converted_file = additional_delete_csv.to_csv(
     f"{selected_output_folder}/{name_of_file}_converted.xyz", index=False, sep=" ")