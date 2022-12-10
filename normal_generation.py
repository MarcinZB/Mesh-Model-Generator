import numpy as np
import open3d as od
import pandas as pd
from tkinter import filedialog
from pathlib import Path
import os

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
input_path = Path(selected_file)
dataname = name_of_file
all_name = f"{input_path}"
point_cloud = np.loadtxt(all_name, skiprows=1)

pcd = od.geometry.PointCloud()
pcd.points = od.utility.Vector3dVector(point_cloud[:, :3])
pcd.colors = od.utility.Vector3dVector(point_cloud[:, 3:6] / 255)

pcd.estimate_normals(search_param=od.geometry.KDTreeSearchParamHybrid(radius=0.008, max_nn=6))
pcd.orient_normals_consistent_tangent_plane(k=6)

absolute_path = f"{input_path}"
csv_wo_normals = pd.read_csv(absolute_path, sep=" ")
print(f"Csv without normals: \n {csv_wo_normals}")
"o3d.visualization.draw_geometries([pcd], point_show_normal=True)"

normals_show = pcd.normals
normals_array = np.asarray(normals_show)
print(normals_array)
data_frame_w_normals = array_to_csv = pd.DataFrame(normals_array)

normals_one_nx = data_frame_w_normals.drop(array_to_csv.columns[1:3], axis=1)
normals_two_ny_1 = data_frame_w_normals.drop(array_to_csv.columns[0], axis=1)
normals_two_ny_2 = normals_two_ny_1.drop(normals_two_ny_1.columns[1:2], axis=1)
normals_three_nz = data_frame_w_normals.drop(array_to_csv.columns[0:2], axis=1)

print(f"Nx:\n {normals_one_nx}")
print(f"Ny:\n {normals_two_ny_2}")
print(f"Nz:\n {normals_three_nz}")

csv_wo_normals['Nx'] = normals_one_nx
csv_wo_normals['Ny'] = normals_two_ny_2
csv_wo_normals['Nz'] = normals_three_nz

csv_wo_normals.to_csv(f"{selected_output_folder}/{name_of_file}_w_normals.xyz", index=False, sep=" ")

print(csv_wo_normals)

point_cloud = np.loadtxt(csv_wo_normals, skiprows=1)
pcd = od.geometry.PointCloud()
pcd.points = od.utility.Vector3dVector(point_cloud[:, :3])
pcd.colors = od.utility.Vector3dVector(point_cloud[:, 3:6] / 255)
pcd.normals = od.utility.Vector3dVector(point_cloud[:, 6:9])
od.visualization.draw_geometries([pcd], point_show_normal=True)