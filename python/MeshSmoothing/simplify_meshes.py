import pymeshlab as ml
import os

input = "C:/Users/ahmed/Documents/4D-VRmovie/testdata/narvis-data-uncompressed/camera06-000000.e57/Data/Model/test.obj"
output = "C:/Users/ahmed/Documents/4D-VRmovie/testdata/narvis-data-uncompressed/camera06-000000.e57/Data/Model/testOutput.obj"

dirPath = "C:/Users/ahmed/Documents/4D-VRmovie/testdata/stryker-uncompressed/Productions"

def simplify_meshes():
    models = os.listdir(dirPath)
    nModels = len(models)
    for i,model in enumerate(models):
        filepath = os.path.join(dirPath,model,"Data\\Model\\Model.obj")
        ms = ml.MeshSet()
        ms.load_new_mesh(filepath)
        m = ms.current_mesh()
        print('input mesh has', m.vertex_number(), 'vertex and', m.face_number(), 'faces')

        #Target number of vertices
        TARGET=50000

        #Estimate number of faces to have 100+10000 vertex using Euler
        numFaces = 100 + 2*TARGET

        #Simplify the mesh. Only first simplification will be agressive
        while (ms.current_mesh().vertex_number() > TARGET):
            ms.apply_filter('meshing_decimation_quadric_edge_collapse_with_texture', targetfacenum=numFaces, preservenormal=True)
            print("Decimated to", numFaces, "faces mesh has", ms.current_mesh().vertex_number(), "vertices")
            #Refine our estimation to slowly converge to TARGET vertex number
            numFaces = numFaces - (ms.current_mesh().vertex_number() - TARGET)

        m = ms.current_mesh()
        print('output mesh has', m.vertex_number(), 'vertex and', m.face_number(), 'faces')
        outputpath = os.path.join(dirPath,model,"Data\\Model\\model_simplified_wtex.obj")
        ms.save_current_mesh(outputpath, save_wedge_texcoord=True)
        

if __name__ == '__main__':
    simplify_meshes()