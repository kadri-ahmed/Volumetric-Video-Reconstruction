import numpy as np
from matplotlib import pyplot as plt
from PIL import Image
import math 
import open3d as o3d

WORKSPACE_PATH="C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/IsaacSim/composer-workspace"

# Camera parameters
HEIGHT = 576
WIDTH = 640
FOCAL_LENGTH = 20 # in mm
HORIZ_APERTURE = 20
VERT_APERTURE = 18 
FIELD_OF_VIEW = 2 * math.atan(HORIZ_APERTURE/ (2 * FOCAL_LENGTH))

# Compute focal point and center
FX_DEPTH = HEIGHT * FOCAL_LENGTH / VERT_APERTURE
FY_DEPTH = WIDTH * FOCAL_LENGTH / HORIZ_APERTURE
CX_DEPTH = HEIGHT * 0.5
CY_DEPTH = WIDTH * 0.5 

SCENE_NR = 69

filepath = f"{WORKSPACE_PATH}/_out_sdrec_0/RenderProduct_Replicator_01/distance_to_camera/distance_to_camera_{SCENE_NR:0>4}.npy"
outputpath = f"{WORKSPACE_PATH}/dataset/narvis/data/distance_to_camera/distance_to_camera_{SCENE_NR:0>4}.png"

in_pcd = "C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/IsaacSim/composer-workspace/_out_sdrec_1/RenderProduct_Replicator_02/pointcloud"



def save_depth_image(depth_map, output_path):
     # Display depth and grayscale image
    fig, axs = plt.subplots(1,2)
    axs[0].imshow(depth_map, cmap='gray')
    axs[0].set_title('Depth image')
    axs[1].imshow(depth_instensity, cmap='gray')
    axs[1].set_title('Depth grayscale image')
    plt.show()

    # Compute grayscale image and save it
    depth_instensity = np.array(256 * depth_map / 0x0fff, dtype=np.float32)
    im = Image.fromarray(depth_instensity.astype(np.float32))
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    im.save(output_path)

def display_depth_image(filepath):
    img_array = np.load(filepath)   
    print(img_array.shape)
    im = Image.fromarray(img_array.astype(np.uint8))
    im.show()

def compute_point_cloud(depth_image):
    pcd = []
    print(depth_image.shape)
    height, width, _ = depth_image.shape
    for i in range(height):
        for j in range(width):
            z = depth_image[i][j]
            x = (j - CX_DEPTH) * z / FX_DEPTH
            y = (i - CY_DEPTH) * z / FY_DEPTH
            pcd.append([x, y, z])
    pcd_o3d = o3d.geometry.PointCloud() 
    pcd_o3d.points = o3d.utility.Vector3dVector(pcd)
    o3d.visualization.draw_geometries([pcd_o3d])

def render_point_cloud(point_cloud):
    pcd = np.load(point_cloud)
    print(pcd.shape)

def demo_depth_to_pcd():
    # Read depth image
    #depth_map_path = f"{WORKSPACE_PATH}/dataset/narvis/data/distance_to_camera/distance_to_camera_69.npy"
    # depth_map_path = "C:/Users/ahmed/Documents/vvreconstruction/testdata/KAOLIN_GENERATED/0_depth.npy"
    depth_map_path = "C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/Kaolin/grid_room_forklist/0_depth.npy" 
    depth_image = np.load(depth_map_path)

    # Print properties
    print(f"Image resolution : {depth_image.shape}")
    print(f"Data type : {depth_image.dtype}")
    print(f"Min value: {np.min(depth_image)}")
    print(f"Max value: {np.max(depth_image)}")
    compute_point_cloud(depth_image)

if __name__ == "__main__":
    path = "C:/Users/ahmed/Documents/vvreconstruction/testdata/KAOLIN_GENERATED/0_depth.npy"
    # save_depth_image(path,path)
    # render_point_cloud()
    demo_depth_to_pcd()

