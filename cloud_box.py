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
#print(f"Csv without normals: \n {csv_wo_normals}")


frame = pd.DataFrame(csv_wo_normals)

maximum_value_x = csv_wo_normals["X" or "x"].max()
maximum_value_y = csv_wo_normals["Y" or "y"].max()
maximum_value_z = csv_wo_normals["Z" or "z"].max()

minimum_value_x = csv_wo_normals["X" or "x"].min()
minimum_value_y = csv_wo_normals["Y" or "y"].min()
minimum_value_z = csv_wo_normals["Z" or "z"].min()

list_of_value = [minimum_value_x,minimum_value_y,minimum_value_z,maximum_value_x,
maximum_value_y, maximum_value_z]

minimum_value = min(list_of_value)
max_value = max(list_of_value)

line_length = ((math.fabs(minimum_value)+2)+(math.fabs(max_value)+2))
print(line_length)

maskXmax = csv_wo_normals["X" or "x"] == maximum_value_x
maskYmax = csv_wo_normals["Y" or "y"] == maximum_value_y
maskZmax = csv_wo_normals["Z" or "z"] == maximum_value_z
maskXmin = csv_wo_normals["X" or "x"] == minimum_value_x
maskYmin = csv_wo_normals["Y" or "y"] == minimum_value_y
maskZmin = csv_wo_normals["Z" or "z"] == minimum_value_z

dfs_Xmax = pd.DataFrame(csv_wo_normals[maskXmax])
dfs_Ymax = pd.DataFrame(csv_wo_normals[maskYmax])
dfs_Zmax = pd.DataFrame(csv_wo_normals[maskZmax])

dfs_Xmin = pd.DataFrame(csv_wo_normals[maskXmin])
dfs_Ymin = pd.DataFrame(csv_wo_normals[maskYmin])
dfs_Zmin = pd.DataFrame(csv_wo_normals[maskZmin])

point1_min = dfs_Xmin.to_numpy()
coordinate_X_of_first_extreme_point = float(point1_min[0,[0]])
coordinate_Y_of_first_extreme_point = float(point1_min[0,[1]])
coordinate_Z_of_first_extreme_point = float(point1_min[0,[2]])
point_min_1 = [coordinate_X_of_first_extreme_point,coordinate_Y_of_first_extreme_point,coordinate_Z_of_first_extreme_point]


point2_min = dfs_Ymin.to_numpy()
coordinate_X_of_second_extreme_point = float(point2_min[0,[0]])
coordinate_Y_of_second_extreme_point = float(point2_min[0,[1]])
coordinate_Z_of_second_extreme_point = float(point2_min[0,[2]])
point_min_2 = [coordinate_X_of_second_extreme_point,coordinate_Y_of_second_extreme_point,coordinate_Z_of_second_extreme_point]


point3_min = dfs_Zmin.to_numpy()
coordinate_X_of_third_extreme_point = float(point3_min[0,[0]])
coordinate_Y_of_third_extreme_point = float(point3_min[0,[1]])
coordinate_Z_of_third_extreme_point = float(point3_min[0,[2]])
point_min_3 = [coordinate_X_of_third_extreme_point,coordinate_Y_of_third_extreme_point,coordinate_Z_of_third_extreme_point]


point1_max = dfs_Xmax.to_numpy()
coordinate_X_of_first_extreme_point_maximum = float(point1_max[0,[0]])
coordinate_Y_of_first_extreme_point_maximum = float(point1_max[0,[1]])
coordinate_Z_of_first_extreme_point_maximum = float(point1_max[0,[2]])
point_max_1 = [coordinate_X_of_first_extreme_point_maximum,coordinate_Y_of_first_extreme_point_maximum,coordinate_Z_of_first_extreme_point_maximum]


point2_max = dfs_Ymax.to_numpy()
coordinate_X_of_second_extreme_point_maximum = float(point2_max[0,[0]])
coordinate_Y_of_second_extreme_point_maximum = float(point2_max[0,[1]])
coordinate_Z_of_second_extreme_point_maximum = float(point2_max[0,[2]])
point_max_2 = [coordinate_X_of_second_extreme_point_maximum,coordinate_Y_of_second_extreme_point_maximum,coordinate_Z_of_second_extreme_point_maximum]

point3_max = dfs_Zmax.to_numpy()
coordinate_X_of_third_extreme_point_maximum = float(point3_max[0,[0]])
coordinate_Y_of_third_extreme_point_maximum = float(point3_max[0,[1]])
coordinate_Z_of_third_extreme_point_maximum = float(point3_max[0,[2]])
point_max_3 = [coordinate_X_of_third_extreme_point_maximum,coordinate_Y_of_third_extreme_point_maximum,coordinate_Z_of_third_extreme_point_maximum]

print(f"\nX range: ({minimum_value_x};{maximum_value_x})")
print(f"\nY range: ({minimum_value_y};{maximum_value_y})")
print(f"\nZ range: ({minimum_value_z};{maximum_value_z})")
print(f"Points:\n {point_max_1},{point_max_2},{point_max_3},{point_min_1},{point_min_2},{point_min_3}")

punkt_A = [(maximum_value_x+2), (maximum_value_y+2), (maximum_value_z+2)]
punkt_B = [(minimum_value_x-2),punkt_A[1], punkt_A[2]]
length_of_line = (math.fabs(punkt_A[0])+math.fabs(punkt_B[0]))
punkt_C = [punkt_B[0], punkt_B[1], (punkt_B[2]-length_of_line)]
punkt_D = [punkt_C[0], (punkt_C[1]-length_of_line), punkt_C[2]]
punkt_E = [punkt_D[0],punkt_D[1],(punkt_D[2]+length_of_line)]
punkt_F = [(punkt_E[0]+length_of_line),punkt_E[1],punkt_E[2]]
punkt_G = [punkt_F[0],punkt_F[1],(punkt_F[2]-length_of_line)]
punkt_H = [punkt_G[0], (punkt_G[1]+length_of_line), punkt_G[2]]
print(punkt_A)
print(punkt_B)
print(punkt_C)
print(punkt_D)
print(punkt_E)
print(punkt_F)
print(punkt_G)
print(punkt_H)
length_of_line_2 = (math.fabs(punkt_C[2])+math.fabs(punkt_B[2]))
print(length_of_line)
print(length_of_line_2)
