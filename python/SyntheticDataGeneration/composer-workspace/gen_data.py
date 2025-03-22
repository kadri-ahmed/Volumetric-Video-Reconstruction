from omni.isaac.kit import SimulationApp
import os

# Set rendering parameters and create an instance of kit
CONFIG = {"renderer": "RayTracedLighting", "headless": True, "width": 1024, "height": 1024, "num_frames": 10}
simulation_app = SimulationApp(launch_config=CONFIG)

ENV_URL = "/Isaac/Environments/Simple_Warehouse/full_warehouse.usd"
FORKLIFT_URL = "/Isaac/Props/Forklift/forklift.usd"
PALLET_URL = "/Isaac/Environments/Simple_Warehouse/Props/SM_PaletteA_01.usd"
CARDBOX_URL = "/Isaac/Environments/Simple_Warehouse/Props/SM_CardBoxD_04.usd"
CONE_URL = "/Isaac/Environments/Simple_Warehouse/Props/S_TrafficCone.usd"
SCOPE_NAME = "/Narvis"

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
from omni.isaac.core.utils.stage import get_current_stage, open_stage
from omni.isaac.core.utils.rotations import euler_angles_to_quat, quat_to_euler_angles, lookat_to_quatf
from omni.isaac.core.utils.bounds import compute_combined_aabb, create_bbox_cache

import omni.replicator.core as rep

def main():
    # Open the environment in a new stage
    print(f"Loading Stage {ENV_URL}")
    open_stage(prefix_with_isaac_asset_server(ENV_URL))

    driver_cam_prim = prims.create_prim(
        prim_path=f"{SCOPE_NAME}/Camera",
        prim_type="Camera",
        position=driver_cam_pos_gf,
        orientation=look_at_pallet_xyzw,
        attributes={"focusDistance": 400, "focalLength": 20, "clippingRange": (0.1, 100)}
    )

    driver_cam_node = rep.get.prim_at_path(str(driver_cam_prim.GetPath()))

    # Camera looking at the pallet
    pall