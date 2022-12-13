import open3d as od
import numpy as np
import pandas as pd
import tkinter
import os
from tkinter import filedialog
from pathlib import Path
import math

points = []

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
input_path = Path(selected_file)
dataname = name_of_file
all_name = f"{input_path}"
point_cloud = np.loadtxt(all_name, skiprows=1)

pcd = od.geometry.PointCloud()
pcd.points = od.utility.Vector3dVector(point_cloud[:, :3])
pcd.colors = od.utility.Vector3dVector(point_cloud[:, 3:6] / 255)
#od.visualization.draw_geometries([pcd])

absolute_path = f"{input_path}"
csv_wo_normals = pd.read_csv(absolute_path, sep=" ")
print(f"Csv without normals: \n {csv_wo_normals}")


frame = pd.DataFrame(csv_wo_normals)

maximum_value_x = csv_wo_normals["X" or "x"].max()
maximum_value_y = csv_wo_normals["Y" or "y"].max()
maximum_value_z = csv_wo_normals["Z" or "z"].max()

minimum_value_x = csv_wo_normals["X" or "x"].min()
minimum_value_y = csv_wo_normals["Y" or "y"].min()
minimum_value_z = csv_wo_normals["Z" or "z"].min()

print(f"Maximum x value: {maximum_value_x}")
print(f"Maximum y value: {maximum_value_y}")
print(f"Maximum z value: {maximum_value_z}")

print(f"Minimum x value: {minimum_value_x}")
print(f"Minimum y value: {minimum_value_y}")
print(f"Minimum z value: {minimum_value_z}")

list_of_value = [minimum_value_x,minimum_value_y,minimum_value_z,maximum_value_x,
maximum_value_y, maximum_value_z]

print(list_of_value)

minimum_value = min(list_of_value)
max_value = max(list_of_value)

line_length = ((math.fabs(minimum_value)+2)+(math.fabs(max_value)+2))
print(line_length)

print(f"X value: ({minimum_value_x};{maximum_value_x})")
print(f"Y value: ({minimum_value_y};{maximum_value_y})")
print(f"Z value: ({minimum_value_z};{maximum_value_z})")

