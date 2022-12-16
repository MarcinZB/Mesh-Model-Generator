import open3d as od
import numpy as np
import pandas as pd
import tkinter
import os
from tkinter import filedialog
from pathlib import Path
import math

points = []
d1 = ""
d2 = ""
d3 = ""
d4 = ""
d5 = ""

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

punkt_A = [(maximum_value_x+2), (maximum_value_y+2), (maximum_value_z+2)]
punkt_B = [(minimum_value_x-2),punkt_A[1], punkt_A[2]]
length_of_line = (math.fabs(punkt_A[0])+math.fabs(punkt_B[0]))
punkt_C = [punkt_B[0], punkt_B[1], (punkt_B[2]-length_of_line)]
punkt_D = [punkt_C[0], (punkt_C[1]-length_of_line), punkt_C[2]]
punkt_E = [punkt_D[0],punkt_D[1],(punkt_D[2]+length_of_line)]
punkt_F = [(punkt_E[0]+length_of_line),punkt_E[1],punkt_E[2]]
punkt_G = [punkt_F[0],punkt_F[1],(punkt_F[2]-length_of_line)]
punkt_H = [punkt_G[0], (punkt_G[1]+length_of_line), punkt_G[2]]

length_of_line_2 = (math.fabs(punkt_C[2])+math.fabs(punkt_B[2]))

diagonal_middle_point_1 = [((punkt_A[0]+punkt_G[0])/2),((punkt_A[1]+
punkt_G[1])/2),((punkt_A[2]+punkt_G[2])/2)]
diagonal_middle_point_2 = [((punkt_B[0]+punkt_H[0])/2),((punkt_B[1]+
punkt_H[1])/2),((punkt_B[2]+punkt_H[2])/2)]
diagonal_middle_point_3 = [((punkt_E[0]+punkt_C[0])/2),((punkt_E[1]+
punkt_C[1])/2),((punkt_E[2]+punkt_C[2])/2)]
diagonal_middle_point_4 = [((punkt_F[0]+punkt_D[0])/2),((punkt_F[1]+
punkt_D[1])/2),((punkt_F[2]+punkt_D[2])/2)]
diagonal_middle_point_5 = [((punkt_A[0]+punkt_E[0])/2),((punkt_A[1]+
punkt_E[1])/2),((punkt_A[2]+punkt_E[2])/2)]



csv_wo_normals["d1"] = np.sqrt((diagonal_middle_point_1[0]+csv_wo_normals["X" or "x"])**2+
(diagonal_middle_point_1[1]+csv_wo_normals["X" or "x"])**2+
(diagonal_middle_point_1[2]+csv_wo_normals["X" or "x"])**2)

csv_wo_normals["d2"] = np.sqrt((diagonal_middle_point_2[0]+csv_wo_normals["X" or "x"])**2+
(diagonal_middle_point_2[1]+csv_wo_normals["X" or "x"])**2+
(diagonal_middle_point_2[2]+csv_wo_normals["X" or "x"])**2)

csv_wo_normals["d3"] = np.sqrt((diagonal_middle_point_3[0]+csv_wo_normals["X" or "x"])**2+
(diagonal_middle_point_3[1]+csv_wo_normals["X" or "x"])**2+
(diagonal_middle_point_3[2]+csv_wo_normals["X" or "x"])**2)

csv_wo_normals["d4"] = np.sqrt((diagonal_middle_point_4[0]+csv_wo_normals["X" or "x"])**2+
(diagonal_middle_point_4[1]+csv_wo_normals["X" or "x"])**2+
(diagonal_middle_point_4[2]+csv_wo_normals["X" or "x"])**2)

csv_wo_normals["d5"] = np.sqrt((diagonal_middle_point_5[0]+csv_wo_normals["X" or "x"])**2+
(diagonal_middle_point_5[1]+csv_wo_normals["X" or "x"])**2+
(diagonal_middle_point_5[2]+csv_wo_normals["X" or "x"])**2)

pcd.estimate_normals(search_param=od.geometry.KDTreeSearchParamHybrid(radius=0.008, max_nn=6))

normals_show = pcd.normals
normals_array = np.asarray(normals_show)
print(normals_array)

for i in csv_wo_normals.index:
    if csv_wo_normals["d1"][i]>csv_wo_normals["d2"][i] and csv_wo_normals["d1"][i]>csv_wo_normals["d3"][i] and csv_wo_normals["d1"][i]>csv_wo_normals["d4"][i] and csv_wo_normals["d1"][i]>csv_wo_normals["d5"][i]:
        pcd.orient_normals_towards_camera_location(pcd, camera_location=np.array(diagonal_middle_point_1))
    elif csv_wo_normals["d2"][i]>csv_wo_normals["d1"][i] and csv_wo_normals["d2"][i]>csv_wo_normals["d3"][i] and csv_wo_normals["d2"][i]>csv_wo_normals["d4"][i] and csv_wo_normals["d2"][i]>csv_wo_normals["d5"][i]:
        pcd.orient_normals_towards_camera_location(pcd, camera_location=np.array(diagonal_middle_point_2))
    elif csv_wo_normals["d3"][i]>csv_wo_normals["d1"][i] and csv_wo_normals["d3"][i]>csv_wo_normals["d2"][i] and csv_wo_normals["d3"][i]>csv_wo_normals["d4"][i] and csv_wo_normals["d3"][i]>csv_wo_normals["d5"][i]:
        pcd.orient_normals_towards_camera_location(pcd, camera_location=np.array(diagonal_middle_point_3))
    elif csv_wo_normals["d4"][i]>csv_wo_normals["d1"][i] and csv_wo_normals["d4"][i]>csv_wo_normals["d2"][i] and csv_wo_normals["d4"][i]>csv_wo_normals["d3"][i] and csv_wo_normals["d4"][i]>csv_wo_normals["d5"][i]:
        pcd.orient_normals_towards_camera_location(pcd, camera_location=np.array(diagonal_middle_point_4))
    elif csv_wo_normals["d5"][i]>csv_wo_normals["d1"][i] and csv_wo_normals["d5"][i]>csv_wo_normals["d2"][i] and csv_wo_normals["d5"][i]>csv_wo_normals["d3"][i] and csv_wo_normals["d5"][i]>csv_wo_normals["d4"][i]:
        pcd.orient_normals_towards_camera_location(pcd, camera_location=np.array(diagonal_middle_point_5))
print(csv_wo_normals)



