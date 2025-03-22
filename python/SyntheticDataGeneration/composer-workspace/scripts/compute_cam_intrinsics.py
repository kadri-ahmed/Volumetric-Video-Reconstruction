import omni
import math
stage = omni.usd.get_context().get_stage()
viewport = omni.kit.viewport.get_viewport_interface()
# acquire the viewport window
viewport_handle = viewport.get_instance("Viewport")
viewport_window = viewport.get_viewport_window(viewport_handle)
width = 1280
height = 720
aspect_ratio = width / height
# get camera prim attached to viewport
camera = stage.GetPrimAtPath(viewport_window.get_active_camera())
focal_length = camera.GetAttribute("focalLength").Get()
horiz_aperture = camera.GetAttribute("horizontalAperture").Get()
# Pixels are square so we can do:
vert_aperture = height/width * horiz_aperture
near, far = camera.GetAttribute("clippingRange").Get()
fov = 2 * math.atan(horiz_aperture / (2 * focal_length))

# compute focal point and center
focal_x = height * focal_length / vert_aperture
focal_y = width * focal_length / horiz_aperture
center_x = height * 0.5
center_y = width * 0.5