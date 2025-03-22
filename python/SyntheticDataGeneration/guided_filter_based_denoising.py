import numpy as np
import open3d as o3d
import os

AIRPLANE_CLEAN_PATH = "C:/Users/ahmed/Documents/vvreconstruction/testdata/PC_DENOISE/PDFLOW_DENOISED/Airplane/airplane_clean.xyz"

NOISY_MODEL="C:/Users/ahmed/Documents/vvreconstruction/testdata/OLD_DATA/NARVIS_RAW/or_room_noisy_100k.xyz"
OUTPUT_PATH = "C:/Users/ahmed/Documents/vvreconstruction/testdata/UNCOMPRESSED_DATASETS/TESTSET/Guided_Filter_denoised"
MAX_ITERS = 5

def main():
    pcd = o3d.io.read_point_cloud(NOISY_MODEL)

    # add_noise(pcd, 0.03)
    o3d.visualization.draw_geometries([pcd])
    # o3d.io.write_point_cloud(os.path.join(OUTPUT_PATH,"noisy_plane.xyz"),pcd)

    # filtering multiple times will reduce the noise significantly
    # but may cause the points distribute unevenly on the surface.
    for i in range(MAX_ITERS):
        print(f'Iteration {i}: Applying filtering...')
        guided_filter(pcd, 0.03, 0.1)
        print(f'Iteration {i}: Done!')

    o3d.visualization.draw_geometries([pcd])
    o3d.io.write_point_cloud(os.path.join(OUTPUT_PATH,"or_room_filtered.xyz"),pcd)


def guided_filter(pcd, radius, epsilon):
    kdtree = o3d.geometry.KDTreeFlann(pcd)
    points_copy = np.array(pcd.points)
    points = np.asarray(pcd.points)
    num_points = len(pcd.points)

    for i in range(num_points):
        k, idx, _ = kdtree.search_radius_vector_3d(pcd.points[i], radius)
        if k < 3:
            continue

        neighbors = points[idx, :]
        mean = np.mean(neighbors, 0)
        cov = np.cov(neighbors.T)
        e = np.linalg.inv(cov + epsilon * np.eye(3))

        A = cov @ e
        b = mean - A @ mean

        points_copy[i] = A @ points[i] + b

    pcd.points = o3d.utility.Vector3dVector(points_copy)


def add_noise(pcd, sigma):
    points = np.asarray(pcd.points)
    noise = np.random.normal(0, sigma, size=points.shape)
    points += noise

if __name__ == '__main__':
    main()