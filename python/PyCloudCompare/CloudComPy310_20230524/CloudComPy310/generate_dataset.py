import cloudComPy as cc 
import os 
import shutil

cc.initCC()

# PATH = "C:/Users/ahmed/Documents/vvreconstruction/testdata/stryker_4dor_export/export"
PATH = "C:/Users/ahmed/Documents/vvreconstruction/testdata/OLD_DATA/ALLDATA/sample_point_cloud/dataset"
OUTPUTPATH = "C:/Users/ahmed/Documents/vvreconstruction/testdata/stryker_4dor_export/full_views"

# x = ['a', 'b', 'c']
# print(x[1:])

# pcl_count = 100
# for dirname in os.listdir(PATH):
#     n = len(os.listdir(os.path.join(PATH,dirname)))
#     if pcl_count > n:
#         pcl_count = n

# if os.path.exists(OUTPUTPATH):
#     shutil.rmtree(OUTPUTPATH)
# os.makedirs(OUTPUTPATH)

# for i in range(pcl_count):
#     pcl_full = []
#     for j in range(5):
#         filepath = os.path.join(PATH,f'cn0{j+1}',f'camera0{j+1}-{i:06d}.e57')
#         name = os.path.basename(filepath)
#         name,_ = os.path.splitext(name)
#         cloud = cc.loadPointCloud(filepath)
#         print(f"Loading pcd at {filepath}...")
#         print(f"Size = {cloud.size()}")
#         if j == 0:
#             pcl_full = cloud 
#         else:
#             pcl_full.fuse(cloud)
#     print(f"Size = {pcl_full.size()}")
#     ret = cc.SavePointCloud(pcl_full, os.path.join(OUTPUTPATH,name+".xyz"))

export_dir = "C:/Users/ahmed/Documents/vvreconstruction/testdata/UNCOMPRESSED_DATASETS/TESTSET"

for j,fn in enumerate(os.listdir(PATH)):
    filepath = os.path.join(PATH,fn)
    name = os.path.basename(filepath)
    name,_ = os.path.splitext(name)
    cloud = cc.loadPointCloud(filepath)
    print(f"Loading pcd at {filepath}...")
    print(f"Size = {cloud.size()}")
    if j == 0:
        pcl_full = cloud 
    else:
        pcl_full.fuse(cloud)
print(f"Size = {pcl_full.size()}")
ret = cc.SavePointCloud(pcl_full, os.path.join(PATH,name+".xyz"))

# for j,fn in enumerate(os.listdir(export_dir+'/clean')):
#     filepath = os.path.join(export_dir,'clean',fn)
#     name = os.path.basename(filepath)
#     name,_ = os.path.splitext(name)
#     cloud = cc.loadPointCloud(filepath)
#     print(f"Loading pcd at {filepath}...")
#     print(f"Size = {cloud.size()}")
#     ret = cc.SavePointCloud(cloud, os.path.join(export_dir+'/converted',name+".e57"))