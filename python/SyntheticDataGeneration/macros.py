import math

# CAMERA PARAMETERS 
HEIGHT = 567
WIDTH = 640
FOCAL_LENGTH = 20 # in mm 
HORIZ_APERTURE = 20
VERT_APERTURE = 18
FIELD_OF_VIEW = 2 * math.atan(HORIZ_APERTURE/ (2 * FOCAL_LENGTH))

# Compute focal point and center
FX_DEPTH = HEIGHT * FOCAL_LENGTH / VERT_APERTURE
FY_DEPTH = WIDTH * FOCAL_LENGTH / HORIZ_APERTURE
CX_DEPTH = HEIGHT * 0.5
CY_DEPTH = WIDTH * 0.5 

# Objects captured
FORKLIFT_NAME="Forklift"
PERSON_NAME="Person"
BED_NAME="Bed"
PALLET_NAME="Pallet"
SORBOT_NAME="SorbotHousing"


# Data
ONE_VIEW_STRYKER_SCENE_RAW = "C:/Users/ahmed/Documents/vvreconstruction/testdata/PC_DENOISE/PDFLOW_DENOISED/Stryker/oneview_stryker.xyz"
ONE_VIEW_STRYKER_SCENE_NOISY = "C:/Users/ahmed/Documents/vvreconstruction/testdata/PC_DENOISE/PDFLOW_DENOISED/Stryker/oneview_stryker_noise_along_z_axis_0,03.xyz"
ONE_VIEW_STRYKER_SCENE_DENOISED_NF = "C:/Users/ahmed/Documents/vvreconstruction/testdata/PC_DENOISE/PDFLOW_DENOISED/Stryker/oneview_stryker_denoised_NF.xyz"


AIRPLANE_CLEAN = "C:/Users/ahmed/Documents/vvreconstruction/testdata/PC_DENOISE/PDFLOW_DENOISED/Airplane/airplane_clean.xyz"
AIRPLANE_NOISY = "C:/Users/ahmed/Documents/vvreconstruction/testdata/PC_DENOISE/PDFLOW_DENOISED/Airplane/airplane_noise_along_z_axis_0.03.xyz"
AIRPLANE_DENOISED = "C:/Users/ahmed/Documents/vvreconstruction/testdata/PC_DENOISE/PDFLOW_DENOISED/Airplane/airplane_denoised_NF.xyz"

SCALE = 1
DISTANCE = 3 * SCALE
# DISTANCE = 8 * SCALE
# DISTANCE = 11 * SCALE
HEIGHT = 5
POSITIONS_Z = [
    (0,0, DISTANCE),
    (0,0, DISTANCE+1),
    (0,0, DISTANCE+2),
    (0,0, DISTANCE+3),
    (0,0, DISTANCE+4),
    (0,0, DISTANCE+5),
]

POSITIONS_Y = [
    (0,DISTANCE,0), 
    (0,DISTANCE+1,0), 
    (0,DISTANCE+2,HEIGHT), 
    (0,DISTANCE+3,HEIGHT), 
    (0,DISTANCE+4,HEIGHT), 
    (0,DISTANCE+5,HEIGHT), 
]

POSITIONS_X = [
    (DISTANCE,0,HEIGHT), 
    (DISTANCE+1,0,HEIGHT), 
    (DISTANCE+2,0,HEIGHT), 
    (DISTANCE+3,0,HEIGHT), 
    (DISTANCE+4,0,HEIGHT), 
    (DISTANCE+5,0,HEIGHT), 
]

POSITIONS_Y_UP = [
    (DISTANCE, -DISTANCE, DISTANCE),        # FORWARD RIGHT TOP CORNER
    (DISTANCE, DISTANCE, DISTANCE),         # FORWARD LEFT TOP CORNER
    (-DISTANCE, -DISTANCE, DISTANCE),       # BACKWARD RIGHT TOP CORNDER
    (-DISTANCE, DISTANCE, DISTANCE),        # BACKWARD LEFT TOP CORNER
    (0, -DISTANCE, DISTANCE),               # SIDE RIGHT TOP CORNER
    (0, DISTANCE, DISTANCE),                # SIDE LEFT TOP CORNER
    (DISTANCE, 0, DISTANCE),                # FRONT TOP CORNER
    (-DISTANCE, 0, DISTANCE)                # BACK TOP CORNER
]

POSITIONS_Z_UP = [
    (DISTANCE, -DISTANCE, HEIGHT),        # FORWARD RIGHT TOP CORNER
    (DISTANCE, DISTANCE, HEIGHT),         # FORWARD LEFT TOP CORNER
    (-DISTANCE, -DISTANCE, HEIGHT),       # BACKWARD RIGHT TOP CORNDER
    (-DISTANCE, DISTANCE, HEIGHT),        # BACKWARD LEFT TOP CORNER
    (0, -DISTANCE, HEIGHT),               # SIDE RIGHT TOP CORNER
    (0, DISTANCE, HEIGHT),                # SIDE LEFT TOP CORNER
    (DISTANCE, 0, HEIGHT),                # FRONT TOP CORNER
    (-DISTANCE, 0, HEIGHT)                # BACK TOP CORNER
]

# POSITIONS_Z_UP = [
#     (0, 0, -HEIGHT),
#     (-HEIGHT, 0, 0),
#     (0, -HEIGHT, 0),
#     (0, DISTANCE, HEIGHT),
#     (DISTANCE, 0, 0),
#     (-DISTANCE, 0, 8),
# ]

# points = [
#     [0.0,0,0,1],
#     [0,0,2,1],
#     [0,0,2.5,1],
#     [0,0,3,1],
#     [0,0,3.5,1],
#     [0,3,0,1],
#     [0,3.5,0,1],
#     [0,4,0,1],
#     [0,4.5,0,1],
#     [0,5,0,1],
#     [0.5,0,0,1],
#     [1,0,0,1],
#     [1.5,0,0,1]
# ]
# for i,vec in enumerate(points):
#     [U,V,W,_] = Transform @ vec
#     pcd.append([U,V,W])