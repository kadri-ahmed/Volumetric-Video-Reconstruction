import omni.replicator.core as rep

DISTANCE = 2.75
HEIGHT = 2.75

POSITIONS = [
    (DISTANCE, -DISTANCE, DISTANCE),        # FORWARD RIGHT TOP CORNER
    (DISTANCE, DISTANCE, DISTANCE),         # FORWARD LEFT TOP CORNER
    (-DISTANCE, -DISTANCE, DISTANCE),       # BACKWARD RIGHT TOP CORNDER
    (-DISTANCE, DISTANCE, DISTANCE),        # BACKWARD LEFT TOP CORNER
    (0, -DISTANCE, DISTANCE),               # SIDE RIGHT TOP CORNER
    (0, DISTANCE, DISTANCE),                # SIDE LEFT TOP CORNER
    (DISTANCE, 0, DISTANCE),                # FRONT TOP CORNER
    (-DISTANCE, 0, DISTANCE)                # BACK TOP CORNER
]

with rep.new_layer():
    camera = rep.create.camera()
    with rep.trigger.on_frame():
        with camera:
            rep.modify.pose(
                position=rep.distribution.sequence(POSITIONS),
                # look_at="/World/Cube",
                look_at=(0,0,0)
            )