import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import filedialog
import numpy as np
import os
import open3d as od
from tkinter.messagebox import showinfo
import whitebox as wb
import pandas as pd
import math
from pathlib import Path

selected_file = r""
selected_output_folder = r""
name_of_file = ""
depth_octree = ""
converted_file = ""


def model():

    global depth_octree

    if selected_file.endswith(".xyz"):
        point_cloud = np.loadtxt(selected_file, skiprows=1)

        pcd = od.geometry.PointCloud()
        pcd.points = od.utility.Vector3dVector(point_cloud[:, :3])
        pcd.colors = od.utility.Vector3dVector(point_cloud[:, 3:6]/255)
        pcd.normals = od.utility.Vector3dVector(point_cloud[:, 6:9])

        poisson_mesh = od.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd, depth=depth_octree, width=0, scale=1, linear_fit=True)[0]
        bbox = pcd.get_axis_aligned_bounding_box()
        p_mesh_crop = poisson_mesh.crop(bbox)
        od.io.write_triangle_mesh(f"{selected_output_folder}/{name_of_file}_Mesh.ply", p_mesh_crop)

        def lod_mesh_export(mesh, lods, path):

            mesh_lods = {}
            for j in lods:
                mesh_lod = mesh.simplify_quadric_decimation(j)
                od.io.write_triangle_mesh(f"{selected_output_folder}/{name_of_file}_Model_w_LoD.ply", mesh_lod)
                mesh_lods[j] = mesh_lod
                bbox = pcd.get_axis_aligned_bounding_box()
                p_mesh_crop = mesh_lod.crop(bbox)
                mesh_lod = p_mesh_crop

            print("generation of "+str(i)+" LoD successful")
            return mesh_lods
        my_lods = lod_mesh_export(poisson_mesh, [300000000], selected_output_folder)
        od.visualization.draw_geometries([my_lods[300000000]])
    else:
        showinfo(
            title="Warning",
            message=f"Input file does not have .xyz extension, please check Conversion checkbox to continue.")


def browse_file():
    global selected_file
    global name_of_file
    filename = filedialog.askopenfilename(initialdir="/",
                                          title="Select a File",
                                          filetypes=(("ASCII",
                                                      "*.xyz*"),
                                                     ("all files",
                                                      "*.*")))
    selected_file = filename
    name_of_file = os.path.basename(filename)
    print(filename)
    variables['Input_File'].set(selected_file)


def select_output_folder():
    global selected_output_folder
    selected_output_folder = filedialog.askdirectory()
    variables['Output_Directory'].set(selected_output_folder)


def csv_convert():

    global name_of_file
    global converted_file
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


def normals_generation():

    input_path = Path(selected_file)
    dataname = name_of_file
    all_name = f"{input_path}/{dataname}"
    point_cloud = np.loadtxt(all_name, skiprows=1)

    pcd = od.geometry.PointCloud()
    pcd.points = od.utility.Vector3dVector(point_cloud[:, :3])
    pcd.colors = od.utility.Vector3dVector(point_cloud[:, 3:6] / 255)

    pcd.estimate_normals(search_param=od.geometry.KDTreeSearchParamHybrid(radius=0.008, max_nn=6))
    pcd.orient_normals_consistent_tangent_plane(k=6)

    absolute_path = f"{input_path}/{dataname}"
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

    csv_wo_normals.to_csv(f"{selected_output_folder}/{converted_file}_w_normals.xyz", index=False, sep=" ")

    print(csv_wo_normals)


def show_point_cloud():

    if bool(selected_file) == True:

        if selected_file.endswith(".xyz"):
            point_cloud = np.loadtxt(selected_file, skiprows=1)
            pcd = od.geometry.PointCloud()
            pcd.points = od.utility.Vector3dVector(point_cloud[:, :3])
            pcd.colors = od.utility.Vector3dVector(point_cloud[:, 3:6] / 255)
            od.visualization.draw_geometries([pcd])
        else:
            showinfo(
                title="Warning",
                message=f"Input file does not have .xyz extension, please convert the file")

    else:
        showinfo(
            title="Warning",
            message=f"You have not selected file, please select .xyz file.")


def show_normals():

    if bool(selected_file) == True:

        if selected_file.endswith(".xyz"):

            point_cloud = np.loadtxt(selected_file, skiprows=1)
            pcdf = pd.DataFrame(point_cloud)
            number_of_columns = len(pcdf.columns)

            if number_of_columns == 9:
                pcd = od.geometry.PointCloud()
                pcd.points = od.utility.Vector3dVector(point_cloud[:, :3])
                pcd.colors = od.utility.Vector3dVector(point_cloud[:, 3:6] / 255)
                pcd.normals = od.utility.Vector3dVector(point_cloud[:, 6:9])
                od.visualization.draw_geometries([pcd], point_show_normal=True)
            else:
                showinfo(
                    title="Warning",
                    message=f"There is no normals, please select file which have normals or generate them.")
        else:
            showinfo(
                title="Warning",
                message=f"Input file does not have .xyz extension, please convert the file")
    else:
        showinfo(
            title="Warning",
            message=f"You have not selected file, please select .xyz file.")


variables = dict()
root = tk.Tk()
root.title("Mesh Model Generator")
root.geometry("300x520")
root.grid_columnconfigure(0, weight=1)
#root.iconbitmap("logo4_mini.ico")

frame = ttk.Frame(root)
frame.grid(padx=10, sticky='EW')
frame.columnconfigure(0, weight=1)


name = Image.open("logo4.png")
img_resize = name.resize((name.height, name.width))
name = ImageTk.PhotoImage(name)

name_label = tk.Label(frame, image=name)
name_label.grid(column=0, row=0)

for i in range(2):
    name_label.columnconfigure(i, weight=1)

data_frame = ttk.LabelFrame(frame, text="Data")
data_frame.grid(sticky="EW")

for i in range(2):
    data_frame.columnconfigure(i, weight=1)
variables["Input_File"] = tk.StringVar()
ttk.Label(data_frame, text="Input File: ").grid(column=0, row=0, sticky="W")
ttk.Button(data_frame, text="Browse for file", command=browse_file).grid(column=1, row=1)
ttk.Entry(data_frame, textvariable=variables["Input_File"]).grid(column=0, row=1, sticky="EW", pady=10)

variables["Output_Directory"] = tk.StringVar()
ttk.Label(data_frame, text="Output Directory: ").grid(column=0, row=2, sticky="W")
ttk.Button(data_frame, text="Choose Directory", command=select_output_folder).grid(column=1, row=3)
ttk.Entry(data_frame, textvariable=variables["Output_Directory"]).grid(column=0, row=3, sticky="EW", pady=10)

data_config_frame = ttk.LabelFrame(frame, text="Data Configuration")
data_config_frame.grid(sticky="EW")
for i in range(3):
    data_config_frame.columnconfigure(i, weight=1)

variables["Convert_Input_Data"] = tk.BooleanVar()
ttk.Checkbutton(data_config_frame, variable=variables["Convert_Input_Data"],
                text="Convert input file to .xyz").grid(column=0, row=1, sticky='EW')

variables["Generate_Normals"] = tk.BooleanVar()
ttk.Checkbutton(data_config_frame, variable=variables["Generate_Normals"],
                text="Generate Normals").grid(column=0, row=2, sticky='EW')


model_options_frame = ttk.LabelFrame(frame, text="Model Options")
model_options_frame.grid(sticky="EW")

for i in range(2):
    model_options_frame.columnconfigure(i, weight=1)

LOD = ('Low', 'Medium', 'High', 'Very High')
var = tk.StringVar()
ttk.Label(model_options_frame, text='Level of Details').grid(column=0, row=0, sticky="W")
combo = ttk.Combobox(model_options_frame, textvariable=var, state='readonly')
combo['values'] = LOD
combo.grid(column=0, row=1, sticky='WE')


def combo_options(*args):
    global depth_octree
    global combo
    depth_octree_for_label = combo.get()
    depth_octree_label = {
        "Very High": 12,
        "High": 9,
        "Medium": 6,
        "Low": 3,
        "": 0,
    }
    depth_octree = depth_octree_label[depth_octree_for_label]
    print(depth_octree)
    if combo.get() == "Very High" or combo.get() == "High":
        showinfo(
            title="Warning",
            message=f"You have chosen {combo.get()} "
                    f"level of details, be patient please. The generation process may last long.")


combo.bind("<<ComboboxSelected>>", combo_options)

buttons = tk.Frame(frame)
buttons.grid(sticky="NW")
save_button = ttk.Button(buttons, text="VISUALIZE NORMALS", command=show_normals)
save_button.pack(side=tk.RIGHT, pady=10)


buttons.grid(sticky="NS")
save_button = ttk.Button(buttons, text="SHOW POINT CLOUD", command=show_point_cloud)
save_button.pack(side=tk.RIGHT, pady=10)

status_variable = tk.StringVar()
ttk.Label(root, textvariable=status_variable).grid(
    sticky="WE", row=99, padx=10
)
buttons = tk.Frame(frame)
buttons.grid(sticky="NS")
save_button = ttk.Button(buttons, text="GENERATE MODEL", command=model)
save_button.pack(side=tk.RIGHT, pady=5)

root.mainloop()