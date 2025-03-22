import numpy as np
import open3d as o3d
import os 

def calculate_chamfer_distance(source, target):

    print(source)
    pcd_src = o3d.io.read_point_cloud(source)
    pcd_dest = o3d.io.read_point_cloud(target)

    # computes for each point in the source point cloud the distance to the closest point in the target point cloud.
    dist_src_to_dest = np.asarray(pcd_src.compute_point_cloud_distance(pcd_dest)) 
    dist_dest_to_src = np.asarray(pcd_dest.compute_point_cloud_distance(pcd_src)) 
    chamfer_distance = np.mean(dist_src_to_dest) + np.mean(dist_dest_to_src)

    print(f"CD = {chamfer_distance * 1e2}")
    return chamfer_distance

def calculate_hausdorf_distance(source, target):
    print(source)
    pcd_src = o3d.io.read_point_cloud(source)
    pcd_dest = o3d.io.read_point_cloud(target)

    # computes for each point in the source point cloud the distance to the closest point in the target point cloud.
    dist_src_to_dest = np.asarray(pcd_src.compute_point_cloud_distance(pcd_dest)) 
    dist_dest_to_src = np.asarray(pcd_dest.compute_point_cloud_distance(pcd_src)) 
    max_src = np.max(dist_src_to_dest)
    max_dst = np.max(dist_dest_to_src)
    hausdorf_distance = max(max_src,max_dst)
    print(f"HD = {hausdorf_distance * 1e2}") 

def visualize_pcd(filepath):
    print(f"Visualizing point cloud at path = {filepath} ...")
    pcd = o3d.io.read_point_cloud(filepath)
    o3d.visualization.draw_geometries([pcd])

PATH = "C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/Narvis/experiments"

def eval_single_file(root, name):
    calculate_chamfer_distance(os.path.join(root,'noisy',name), os.path.join(root,'clean',name))
    calculate_chamfer_distance(os.path.join(root,'denoised',name), os.path.join(root,'clean',name))

if __name__ == "__main__":
    name = 'charite_or_50k'

    # eval_single_file(PATH,f'{name}.xyz')
    # filepath = f'{PATH}/clean/{name}.xyz
    root = 'C:/Users/ahmed/Documents/vvreconstruction/assets/experiments/experiment_1_raw_data_denoise'
    dirPath = 'C:/Users/ahmed/Documents/vvreconstruction/assets/experiments/experiment_1_raw_data_denoise/raw'
    score_noisy = []
    score_denoised = []
    # visualize_pcd(filepath)
    for fn in os.listdir(dirPath):
        pcl_clean = os.path.join(root,'raw',fn)
        pcl_noisy = os.path.join(root,'noisy',fn)
        pcl_denoised = os.path.join(root,'denoised',fn)
        score_noisy.append(calculate_chamfer_distance(pcl_noisy, pcl_clean))
        score_denoised.append(calculate_chamfer_distance(pcl_denoised, pcl_clean))
    score_noisy = np.average(np.array(score_noisy)) * 1e2
    score_denoised = np.average(np.array(score_denoised)) * 1e2
    print(f'Avg. Score noisy = {score_noisy} - Avg. Score denoised = {score_denoised}')
    print(f'Improvement = {(score_denoised / score_noisy) * 1e2}%')