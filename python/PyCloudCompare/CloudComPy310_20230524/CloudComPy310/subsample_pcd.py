import cloudComPy as cc 
import os 
import shutil

cc.initCC()
SPLIT = 'test'
TYPE = 'noisy'

# resolutions = ["10000","30000","50000","100000", "500000", "1000000"]
resolutions = ["10000","30000","50000"]
# root = f"C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/IsaacNetRes"
# root = f"C:/Users/ahmed/Documents/vvreconstruction/python/synthetic_data_gen/SYNTHNet"
root = f"C:/Users/ahmed/Documents/vvreconstruction/python/synthetic_data_gen/data/alien_pcl"
# dirpath = "C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/Narvis/dataset_old/clean"
# dirpath = f"C:/Users/ahmed/Documents/vvreconstruction/python/synthetic_data_gen/dataset/{SPLIT}/{TYPE}"
dirpath = "C:/Users/ahmed/Documents/vvreconstruction/python/synthetic_data_gen/data/alien_pcl/noisy"
files = os.listdir(dirpath)

for res in resolutions:
    output_path = os.path.join(root,res)
    if os.path.exists(output_path):
        shutil.rmtree(output_path)
    os.makedirs(output_path)

for i, filename in enumerate(files):
    filepath = os.path.join(dirpath,filename)
    name = os.path.basename(filepath)
    name,_ = os.path.splitext(name)
    cloud = cc.loadPointCloud(filepath)
    print(f"Loading pcd at {filepath}...")
    print(f"Size = {cloud.size()}")
    for r in resolutions:
        if cloud.size() < int(r):
            continue
        refCloud = cc.CloudSamplingTools.subsampleCloudRandomly(cloud, int(r))
        (randomCloud, res) = cloud.partialClone(refCloud)
        randomCloud.setName("randomCloud")
        if refCloud.size() != int(r):
            raise RuntimeError
        if res != 0:
            raise RuntimeError
        
        # output_path = os.path.join(root,SPLIT,r,TYPE)
        output_path = os.path.join(root,r)
        ret = cc.SavePointCloud(randomCloud, os.path.join(output_path,name+".xyz"))
        if ret != 0:
            raise RuntimeError
    