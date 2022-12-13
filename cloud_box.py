import open3d as od
import numpy as np
import pandas as pd
import tkinter
import os
from tkinter import filedialog
from pathlib import Path


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
od.visualization.draw_geometries([pcd])
