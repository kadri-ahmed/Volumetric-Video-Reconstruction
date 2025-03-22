import numpy as np
import random
from scipy.stats import norm
import open3d as o3d
import os

class NoiseModel(object):
    pass 



class KinectLinearNoise(object):

    def __init__(self, stddev_max=0.017, dist_err_max=0.011) -> None:
        super().__init__()
        self.stddev_max = stddev_max
        self.dist_err_max = dist_err_max
        
    """
    2D : image with shape (H,W)
    """
    def __call__(self, data):
        pcl = data['pcl_clean'].copy()
        height,width = pcl.shape
        noise = []
        for x in range(height):
            for y in range(width):
                noise_std = random.uniform(0.01, self.stddev_max)
                random_error = np.random.normal(0,noise_std)
                noise.append(random_error)
                systematic_error = np.random.uniform(0, self.dist_err_max) + 1e-3 * pcl[x][y] 
                pcl[x][y] += random_error + systematic_error
        data['pcl_noisy'] = pcl
        # print(f'max error = {np.max(noise)}')
        # print(f'min error = {np.min(noise)}')
        return data


        

class GaussianNoise(NoiseModel):
    def __init__(self, min_std, max_std, dim):
        super().__init__()
        self.min_std = min_std
        self.max_std = max_std
        self.dim = dim
    
    """
    2D : image with shape (H,W)
    3D : list of points with shape (N,3)
    """
    def __call__(self, data):
        if self.dim == 2:
            pcl = data['pcl_clean'].copy()
            height,width = pcl.shape
            noise = []
            for x in range(height):
                for y in range(width):
                    noise_std = random.uniform(self.min_std, self.max_std)
                    random_error = np.random.normal(0,noise_std)
                    noise.append(random_error)
                    pcl[x][y] += random_error
            data['pcl_noisy'] = pcl
        # print(f'max error = {np.max(noise)}')
        # print(f'min error = {np.min(noise)}')
            return data
        elif self.dim == 3:
            points,_ = data.shape 
            noise_std = random.uniform(self.min_std, self.max_std)
            noise = np.random.normal(0,noise_std,data.shape)
            data += noise
            return data

if __name__ == '__main__':
    NOISY_MODEL="C:/Users/ahmed/Documents/vvreconstruction/testdata/OLD_DATA/NARVIS_RAW/or_room_raw_100k.xyz"
    pcd = o3d.io.read_point_cloud(NOISY_MODEL)
    points = np.array(pcd.points)
    noise = GaussianNoise(0.01,0.03)
    pcd= noise(points,3)
    pcd_o3d = o3d.geometry.PointCloud() 
    pcd_o3d.points = o3d.utility.Vector3dVector(pcd)
    o3d.visualization.draw_geometries([pcd_o3d])
    o3d.io.write_point_cloud(os.path.join("C:/Users/ahmed/Documents/vvreconstruction/testdata/OLD_DATA/NARVIS_RAW","or_room_noisy.xyz"),pcd_o3d)
