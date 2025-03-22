import json 
import numpy as np 
from PIL import Image
from matplotlib import pyplot as plt
import open3d as o3d
import os
from scipy.spatial.transform import Rotation as R
import random
from utils import Logger,colorama
from macros import *
from tqdm import tqdm
from noise_model import *

class Camera:

    def __init__(self, noise_model) -> None:
        self.noise_model = noise_model
    
    def update_camera_pose(self, config_path):
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
        self.config = config
        self.focal_length = config["cameraFocalLength"]
        self.sensor_width = config["cameraAperture"][0]
        self.im_width = config["renderProductResolution"][0]
        self.im_height = config["renderProductResolution"][1]

        self.sensor_height = self.im_height/self.im_width * self.sensor_width 
        self.fx = (self.im_width * self.focal_length) / self.sensor_width
        self.fy = (self.im_height * self.focal_length) / self.sensor_height
        self.cx = self.im_width * 0.5
        self.cy = self.im_height * 0.5
        
        self.projection_matrix = config['cameraProjection']
        self.view_matrix = config['cameraViewTransform']

        # Calculate Transform from Omniverse to Open3D
        # Extrinsics Matrix
        Mext = np.array(self.view_matrix).reshape(4,4).T
        
        # Create a 4x4 identity matrix
        Mrotx = np.eye(4)
        Mroty = np.eye(4)
        # Set the upper-left 3x3 block of the 4x4 matrix to the rotation matrix
        Mrotx[:3, :3] = R.from_euler('x', 90, degrees=True).as_matrix() 
        Mroty[:3, :3] = R.from_euler('y', 90, degrees=True).as_matrix() 
        
        Mrot = Mrotx @ Mroty
        r = R.from_euler('x', 180, degrees=True).as_matrix()
        OmniCam_to_Open3dCam = np.eye(4)
        OmniCam_to_Open3dCam[:3,:3] = r 
        self.Transform = np.linalg.inv(Mrot) @ np.linalg.inv(Mext) @ OmniCam_to_Open3dCam

    def backward_from_implane(self,name, depth_image_path, camera_pose_path, output_pcl_path='', export_pcl=False,apply_noise=False,visualize=False):
        pcd = []
        # Logger.info(f'Loading depthmap {depth_image_path} with shape {depthmap.shape}', colorama.Fore.CYAN)
        depthmap = np.load(depth_image_path)
        # Logger.info(f"Loading camera model {camera_pose_path}", colorama.Fore.YELLOW)
        self.update_camera_pose(camera_pose_path)

        height, width = depthmap.shape
        data = {
            'pcl_clean' : depthmap
        }
        if apply_noise:
            data = self.noise_model(data)
            depthmap = data['pcl_noisy']
        for y in range(height):
            for x in range(width):
                Z = depthmap[y][x]
                if Z == float('+inf') or Z == float('-inf'):
                    continue
                X = Z * (x - self.cx) / self.fx
                Y = Z * (y - self.cy) / self.fy
                [U,V,W, _] = self.Transform @ [X, Y, Z, 1] # cam coords to world coords
                pcd.append([U,V,W])
        pcd_o3d = o3d.geometry.PointCloud() 
        pcd_o3d.points = o3d.utility.Vector3dVector(pcd)
        if visualize:
           o3d.visualization.draw_geometries([pcd_o3d])
        if export_pcl:
            if apply_noise:
                o3d.io.write_point_cloud(os.path.join(output_pcl_path,"noisy",f'{name}.xyz'), pcd_o3d) 
            else:
                o3d.io.write_point_cloud(os.path.join(output_pcl_path,"clean",f'{name}.xyz'), pcd_o3d)
        return pcd 
        
    def generate_fullview_pcl(self, depthmaps_path, output_pcl_path='',export=False,visualize=False,apply_noise=False, number_of_frames=8):
        """
        Computes the point cloud from 2D depth images (NP Array of floats)
        of multiple views and returns the 3D points
        """
        pcd = []
        files = os.listdir(depthmaps_path)
        name = os.path.basename(depthmaps_path)
        for i, fn in enumerate(tqdm(files,desc='Generating Fullview')):
            if i >= number_of_frames:
                break
            depth_image_path = os.path.join(depthmaps_path,f"distance_to_image_plane_{i:04d}.npy")
            config_path = os.path.join(depthmaps_path, f"camera_params_{i:04d}.json")
            if output_pcl_path == '':
                raise Exception("No output directory was specified")
            frame_name = f'{name}_{i}'
            pcd += self.backward_from_implane(frame_name,depth_image_path,config_path,output_pcl_path,
                                               export_pcl=False, visualize=False, apply_noise=apply_noise)
        pcd_o3d = o3d.geometry.PointCloud() 
        pcd_o3d.points = o3d.utility.Vector3dVector(pcd)
        if visualize:
            o3d.visualization.draw_geometries([pcd_o3d])
        if export:
            if apply_noise:
                o3d.io.write_point_cloud(os.path.join(output_pcl_path,"noisy",f'{name}.xyz'), pcd_o3d) 
            else:
                o3d.io.write_point_cloud(os.path.join(output_pcl_path,"clean",f'{name}.xyz'), pcd_o3d) 

def generate_dataset(data_dir, dataset_dir):
    splits = ['train','test']
    camera = Camera(KinectLinearNoise())
    for split in splits:
        Logger.info(f'Starting to generate models for {split}',colorama.Fore.CYAN)
        for add_noise in [True,False]:
            for model in tqdm(os.listdir(os.path.join(data_dir,split)), desc=f'Creating {"noisy" if add_noise else "clean"} PCLs'):
                model_path = os.path.join(data_dir,split,model)
                output_model_path = os.path.join(dataset_dir,split)
                if not os.path.exists(output_model_path):
                    os.makedirs(output_model_path)
                camera.generate_fullview_pcl(model_path,output_model_path,export=True,apply_noise=add_noise)

def generate_noisy_from_raw(data_dir, dataset_dir):
    noise = GuassianNoise(0.03,0.05)
    for model in tqdm(os.listdir(os.path.join(data_dir,'clean')), desc=f'Creating noisy PCLs'):
        model_path = os.path.join(data_dir,'clean',model)
        output_model_path = os.path.join(dataset_dir,'noisy')
        if not os.path.exists(output_model_path):
            os.makedirs(output_model_path)
        pcd_src = o3d.io.read_point_cloud(model_path)
        pcd = np.asarray(pcd_src.points)
        pcd = noise(pcd,dim=3)
        pcd_o3d = o3d.geometry.PointCloud() 
        pcd_o3d.points = o3d.utility.Vector3dVector(pcd)
        # o3d.visualization.draw_geometries([pcd_o3d])
        o3d.io.write_point_cloud(os.path.join(output_model_path,f'{model}.xyz'), pcd_o3d) 

def generate_noisy_from_clean_resolutions(root, resolutions):
    for res in resolutions:
        for model in tqdm(os.listdir(os.path.join(root,'clean_res',res)), desc=f'Creating noisy PCLs'):
            model_path = os.path.join(root,'clean_res',res,model)
            output_model_path = os.path.join(root,'noisy_res',res)
            if not os.path.exists(output_model_path):
                os.makedirs(output_model_path)
            pcd_src = o3d.io.read_point_cloud(model_path)
            pcd = np.asarray(pcd_src.points)
            noise = GaussianNoise(0.03,0.05,3)
            pcd = noise(pcd)
            pcd_o3d = o3d.geometry.PointCloud() 
            pcd_o3d.points = o3d.utility.Vector3dVector(pcd)
            # o3d.visualization.draw_geometries([pcd_o3d])
            o3d.io.write_point_cloud(os.path.join(output_model_path,f'{model}'), pcd_o3d) 

if __name__ == "__main__":
    camera = Camera(GaussianNoise(0.03,0.05,2))
    foldername = "japanese_room"
    datadir = os.path.join(os.getcwd(),f"data")
    datasetdir = os.path.join(os.getcwd(),f"dataset")
    generate_noisy_from_clean_resolutions("C:/Users/ahmed/Documents/vvreconstruction/python/synthetic_data_gen/data/alien_pcl",['10000','30000','50000'])
    # generate_noisy_from_raw("C:/Users/ahmed/Documents/vvreconstruction/testdata/UNCOMPRESSED_DATASETS/RAWDataset", "C:/Users/ahmed/Documents/vvreconstruction/testdata/UNCOMPRESSED_DATASETS/RAWDataset")