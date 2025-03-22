import open3d as o3d
import numpy as np
from PIL import Image

def point_cloud_from_depth_image():
    cam_extrinsic = [[1,0,0,0], [0,-1,0,0], [0,0,-1,0]]
    cam_intrinsics = o3d.camera.PinholeCameraIntrinsic()


    im_frame = Image.open("test_depth02.png")

    depth_image = np.array(im_frame.getdata(),dtype=np.float32)
    depth_o3d = o3d.geometry.Image(depth_image)

    pcd = o3d.geometry.PointCloud.create_from_depth_image(depth_o3d, cam_intrinsic)
    # pcd.transform(cam_extrinsic)
    o3d.visualization.draw_geometries([pcd])

def surface_recon():
    pcd = o3d.data.PLYPointCloud()
    pcd = o3d.io.read_point_cloud("clean_merged_pc.ply")
    print(pcd)
    print('run Poisson surface reconstruction')
    with o3d.utility.VerbosityContextManager(
            o3d.utility.VerbosityLevel.Debug) as cm:
        mesh, densities = o3d.geometry.TriangleMesh.create_from_point_cloud_poisson(
            pcd, depth=9)
    print(mesh)
    o3d.visualization.draw_geometries([mesh])

if __name__ == "__main__":
    surface_recon()