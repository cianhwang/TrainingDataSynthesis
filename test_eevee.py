import bpy
import sys
sys.path.append('/Users/qian/Documents/TrainingDataSynthesis')
from utils import *

def init_scene_eevee():
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_EEVEE'
    scene.eevee.taa_samples = 16
    scene.eevee.taa_samples = 1
    scene.eevee.use_taa_reprojection = False
    scene.render.resolution_x = 512
    scene.render.resolution_y = 512

    
if __name__ == "__main__":
    init_scene_eevee()
    clear_scene(True)
    
    light = bpy.data.lights['Light']
    light.use_shadow = False
    cam = bpy.data.cameras['Camera']
    cam.lens = 5000
    
    for i in range(5):
        obj = add_mesh_obj("cube")
        mat = add_material(obj)
        add_texture(obj, mat, "ShaderNodeTexVoronoi")
        
        add_modifier(obj, level = 4)
        displace_surface(obj, mat, disp_method="BUMP")
        
#    link_file_node("/Users/qian/Downloads/eevee_test", "Image")
#    bpy.ops.render.render(write_still = True)
    
    

    
    

    