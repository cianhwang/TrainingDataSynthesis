import bpy

def scene_initialize(scene):
    scene.render.engine = 'CYCLES'
    #scene.cycles.device = 'GPU'
    scene.render.resolution_x = 4096
    scene.render.resolution_y = 4096
    scene.cycles.samples = 4096
    scene.cycles.max_bounces = 1
    scene.cycles.filter_width = 0.7 ## turn off anti-aliasing
    scene.frame_end = 10
    scene.render.use_border = True
    scene.render.use_crop_to_border = True
    scene.render.border_min_x = 900/4096
    scene.render.border_max_x = 964/4096
    scene.render.border_min_y = 500/4096
    scene.render.border_max_y = 564/4096

if __name__ == "__main__":
    scene = bpy.context.scene
    scene_initialize(scene)
