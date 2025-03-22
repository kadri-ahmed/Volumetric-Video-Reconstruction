from omni.isaac.kit import SimulationApp
import os
from macros import *

# Set rendering parameters and create an instance of kit
CONFIG = {"renderer": "RayTracedLighting", "headless": True, "width": 640, "height": 567, "num_frames": 8}
simulation_app = SimulationApp(launch_config=CONFIG)

###############################################################################################################
############################################## Assets #########################################################
###############################################################################################################
############# Environments ##############
ENV_URL = "/Isaac/Environments/Grid/gridroom_black.usd"
OR_ROOM_URL="C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/Narvis/extras/OR_room_charite_scale_1.usd"
VR_GALLERY_URL="C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/Narvis/extras/VR_Round_Art_Gallery.usdz"
LIVING_ROOM_URL="C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/Narvis/extras/White_Modern_Living_Room.usdz"
SIMPLE_ROOM_URL="omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Environments/Simple_Room/simple_room.usd"
WAREHOUSE_URL="omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Environments/Simple_Warehouse/full_warehouse.usd"
ATTIC_URL="omniverse://localhost/NVIDIA/Samples/OldAttic/Sublayers/Attic_NVIDIA.usd"
SPACE_URL="omniverse://localhost/NVIDIA/Samples/Astronaut/Astronaut.usd"

############# Objects ###################
FORKLIFT_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Props/Forklift/forklift.usd"
SPHERE_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Props/Shapes/sphere.usd"
CUBE_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Props/Shapes/cube.usd"
PATIENT_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/People/Characters/M_Medical_01/M_Medical_01.usd"
BED_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Environments/Hospital/Props/SM_HospitalBed_02d.usd"
PLANE_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Props/Shapes/plane.usd"
PALLET_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Props/Pallet/o3dyn_pallet.usd"
SORBOT_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Props/Sortbot_Housing/sortbot_housing.usd"
WOMAN_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/People/Characters/F_Business_02/F_Business_02.usd"
TABLE_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Props/Mounts/table.usd"
BIN_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Props/KLT_Bin/small_KLT.usd"
DOLLY_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Props/Dolly/dolly.usd"
ROBOT_URL = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/Robots/Jetracer/jetracer.usd"
BEAR_URL = "omniverse://localhost/NVIDIA/Samples/OldAttic/Props/bear.usd"
CLOCK_URL = "omniverse://localhost/NVIDIA/Samples/OldAttic/Props/clock.usd"
WALL_URL = "omniverse://localhost/NVIDIA/Samples/OldAttic/Props/wood_walls.usd" 
SOFA_URL = "omniverse://localhost/NVIDIA/Samples/OldAttic/Props/couch_body.usd"
PIANO_URL ="omniverse://localhost/NVIDIA/Samples/OldAttic/Props/piano.usd"
WOODEN_HORSE = "omniverse://localhost/NVIDIA/Samples/OldAttic/Props/horse.usd"
GRAMA_URL = "omniverse://localhost/NVIDIA/Samples/OldAttic/Props/grama.usd"
SHELF_URL = "omniverse://localhost/NVIDIA/Samples/OldAttic/Props/shelf.usd"
TENNIS_BALL = "omniverse://localhost/NVIDIA/Samples/OldAttic/Props/tennis_ball.usd"
RUGBY_BALL = "omniverse://localhost/NVIDIA/Samples/OldAttic/Props/football.usd"
JAR_URL = "omniverse://localhost/NVIDIA/Samples/OldAttic/Props/GlassJar.usd"
CONSTRUCTION_WORKER = "omniverse://localhost/NVIDIA/Assets/Isaac/2022.2.1/Isaac/People/Characters/male_adult_construction_03/male_adult_construction_03.usd"
VENICE_MASK = "C:/Users/ahmed/Documents/vvreconstruction/python/NvidiaOmniverse/Narvis/extras/Venice_Mask.usdz"


SCOPE_NAME = "/NarvisScope"

import carb
import random
import math
import numpy as np
from pxr import UsdGeom, Usd, Gf, UsdPhysics, PhysxSchema

import omni.usd
from omni.isaac.core import World
from omni.isaac.core.utils import prims
from omni.isaac.core.prims import RigidPrim
from omni.isaac.core.utils.nucleus import get_assets_root_path
from omni.isaac.core.utils.stage import get_current_stage, open_stage, set_stage_up_axis
from omni.isaac.core.utils.rotations import euler_angles_to_quat, quat_to_euler_angles, lookat_to_quatf
from omni.isaac.core.utils.bounds import compute_combined_aabb, create_bbox_cache

import omni.replicator.core as rep

# Helper function to find the assets server
def prefix_with_isaac_asset_server(relative_path):
    assets_root_path = get_assets_root_path()
    if assets_root_path is None:
        raise Exception("Nucleus server not found, could not access Isaac Sim assets folder")
    return assets_root_path + relative_path

# Starts replicator and waits until all data was successfully written
def run_orchestrator():
    rep.orchestrator.run()

    # Wait until started
    while not rep.orchestrator.get_is_started():
        simulation_app.update()

    # Wait until stopped
    while rep.orchestrator.get_is_started():
        simulation_app.update()

    rep.BackendDispatch.wait_until_done()
    rep.orchestrator.stop()

def main():
    # Open the environment in a new stage
    # print(f"Loading Stage {OR_ROOM_URL}")
    # set_stage_up_axis(axis='y')
    # open_stage(prefix_with_isaac_asset_server(ENV_URL))
    # print(f"Loading Stage {SPACE_URL}")
    # open_stage(SPACE_URL)

    ################################################################
    ####### Setting up the camera
    ################################################################
    kinect_cam_1 = rep.create.camera() 

    ################################################################
    ####### Setting up the writer 
    ################################################################

    writer = rep.WriterRegistry.get("BasicWriter")
    output_directory = os.getcwd() + "/../data/venice_mask"
    print("Outputting data to ", output_directory)
    writer.initialize(
        output_dir=output_directory,
        rgb=True,
        distance_to_image_plane=True,
        camera_params=True,
    )

    RESOLUTION = (CONFIG["width"], CONFIG["height"])
    kinect_rp_1 = rep.create.render_product(kinect_cam_1, RESOLUTION)
    writer.attach([kinect_rp_1])

    ################################################################
    ####### Add target object to the scene
    ################################################################


    # Spawn a new forklift at a random pose
    forklift_prim = prims.create_prim(
        prim_path=f"{SCOPE_NAME}/doe_kneader",
        # position=(random.uniform(-20, -2), random.uniform(-1, 3), 0),
        position=(0, 0, 0),
        # orientation=euler_angles_to_quat([0, 0, random.uniform(0, math.pi)]),
        orientation=euler_angles_to_quat([0, 0, 0]),
        scale=(0.3,0.3,0.3),
        usd_path=VENICE_MASK,
        semantic_label="Forklift",
    )

    # Spawn the pallet in front of the forklift with a random offset on the Y axis
    # forklift_tf = omni.usd.get_world_transform_matrix(forklift_prim)
    # person_1_offset_tf = Gf.Matrix4d().SetTranslate(Gf.Vec3d(random.uniform(1, 2),0 , 0))
    # person_1_pos_gf = (person_1_offset_tf * forklift_tf).ExtractTranslation()
    # person_2_offset_tf = Gf.Matrix4d().SetTranslate(Gf.Vec3d(random.uniform(1, 1), 0, 0))
    # person_2_pos_gf = (person_2_offset_tf * forklift_tf).ExtractTranslation()
    # person_3_offset_tf = Gf.Matrix4d().SetTranslate(Gf.Vec3d(0,0,random.uniform(1, 1)))
    # person_3_pos_gf = (person_3_offset_tf * forklift_tf).ExtractTranslation()

    # forklift_quat_gf = forklift_tf.ExtractRotation().GetQuaternion()
    # forklift_quat_xyzw = (forklift_quat_gf.GetReal(), *forklift_quat_gf.GetImaginary())

    # person_prim_1 = prims.create_prim(
    #     prim_path=f"{SCOPE_NAME}/Person",
    #     position=person_1_pos_gf,
    #     orientation=euler_angles_to_quat([0, 0, -90]),
    #     scale=(1.0,1.0,1.0),
    #     usd_path=PATIENT_URL,
    #     semantic_label="Patient",
    # )

    # print(f'Distance(Forklift,Person1) = {person_1_offset_tf}')
    
    # person_prim_2 = prims.create_prim(
    #     prim_path=f"{SCOPE_NAME}/Person2",
    #     position=person_2_pos_gf,
    #     orientation=euler_angles_to_quat([0, 0, -90]),
    #     scale=(1.0,1.0,1.0),
    #     usd_path=PATIENT_URL,
    #     semantic_label="Patient",
    # )

    # person_prim_3 = prims.create_prim(
    #     prim_path=f"{SCOPE_NAME}/Person3",
    #     position=person_3_pos_gf,
    #     orientation=euler_angles_to_quat([0, 0, 90]),
    #     scale=(1.0,1.0,1.0),
    #     usd_path=PATIENT_URL,
    #     semantic_label="Patient",
    # )

    # print(f'Distance(Forklift,Person2) = {person_2_offset_tf}')

    with rep.trigger.on_frame(num_frames=CONFIG["num_frames"]):
        with kinect_cam_1:
            rep.modify.pose(
                position= rep.distribution.sequence(POSITIONS_Y_UP),
                # look_at=str(forklift_prim.GetPrimPath()),
                look_at=(0,0,0),
            )
    run_orchestrator()
    simulation_app.update()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        carb.log_error(f"Exception: {e}")
        import traceback

        traceback.print_exc()
    finally:
        simulation_app.close()