import bpy
import random
from math import radians
import math
import sys
sys.path.append("/Users/qian/Documents/TrainingDataSynthesis")
from utils import *

mesh_obj_list = ["plane", "cube", "uv_sphere", "cylinder", "cone", "torus"]
tex_list = ["ShaderNodeTexVoronoi",
                    "ShaderNodeTexMagic",
                    "ShaderNodeTexBrick",
                    "ShaderNodeTexChecker"]
surface_list = ["ShaderNodeTexMusgrave", "ShaderNodeTexNoise"]

def gen_random_obj_with_texture(mesh_type = None):

    if mesh_type is None:
        mesh_type = random.choice(mesh_obj_list)
    obj = add_mesh_obj(mesh_type)
    if "Plane" in obj.name or "Cube" in obj.name:
        add_modifier(obj, 4)
    mat = add_material(obj)

    tex_type = random.choice(tex_list)
    add_texture(obj, mat, tex_type, tex_random_params(tex_type))
    
    surface_type = random.choice(surface_list)
    displace_surface(obj, mat, surface_type, surface_random_params(surface_type))
    return obj

def set_animation(obj, trans_params, is_background = False):
    if is_background is not True:
        obj.location, obj.rotation_euler, obj.scale = trans_params
    else:
        obj.location, _, _ = trans_params
    obj.keyframe_insert(data_path="location", index=-1)
    if is_background is not True:
        obj.keyframe_insert(data_path="rotation_euler", index=-1)
        obj.keyframe_insert(data_path="scale", index=-1)
    
def get_rand_trans():
    location = (random.random() * 4 - 2, 
                    random.random() * 4 - 2, 
                    random.random() * 4 - 2)
    rotation = (random.random() * math.pi * 2, 
                random.random() * math.pi * 2, 
                random.random() * math.pi * 2)
    scale =    (0.1 + 1.9 * random.random(), 
                0.1 + 1.9 * random.random(), 
                0.1 + 1.9 * random.random())
    return (location, rotation, scale)
                
def gen_random_animation(obj_list, patition_len = 7):
    '''
    obj_list: contains a list of mesh objects
    ---
    gen random partition inside n_frames, 
    e.g. n_frames = 60, partition = [0, 10, 21, 33, 45, 52, 60]
    '''
    scene = bpy.context.scene
    n_frames = scene.frame_end
    interval = int(n_frames/(patition_len - 1))
    for obj in obj_list:
        if obj.name != "background":
            partition = [interval*i for i in range(patition_len)] ## equally distributed
            for curr_time in partition:
                scene.frame_set(curr_time)
                trans_params = get_rand_trans()
                set_animation(obj, trans_params)
        else:
            partition = [interval*i for i in range(patition_len)]
            for curr_time in partition:
                scene.frame_set(curr_time)
                trans_params = get_rand_trans()
                set_animation(obj, trans_params, True)
    
if __name__ == '__main__':
#    random.seed("qian038")
    ''' initialize scene '''
    init_scene(n_frames = 6, render_region = True, 
                render_params = (2016, 2080, 2016, 2080))
    
    n_scenes = 1
    
    for scene_idx in range(n_scenes):
        ''' clear scene '''
        clear_scene()

        ''' add light source '''
        add_light((-3, 0, 7))

        ''' set camera '''
        add_camera((7, -7, 5), (radians(63.6), 0, radians(46.7)))
        
        ''' add background cube '''
#        background = add_mesh_obj("cube", {"size":20})
#        add_modifier(background, 4)
#        mat = add_material(background)
#        
#        add_texture(background, mat, random.choice(tex_list), 
#                    {"Scale": 20})
#        displace_surface(background, mat, type = random.choice(surface_list), 
#                        params = {"Scale": 1.0}, disp_method='BUMP')
        background = gen_random_obj_with_texture("cube")
        background.dimensions = (20, 20, 20)
        background.name = "background"
        
        ''' add objs '''
        n_obj = random.randint(10, 20)
        obj_list = [background]
        for i in range(n_obj):
            obj_list.append(gen_random_obj_with_texture())

        gen_random_animation(obj_list)
        
        ''' output '''
        path = '/Users/qian/Downloads/blender_collection/scene{:02d}/'.format(scene_idx)
        link_file_node(path + 'Image', 'Image')
        link_file_node(path + 'Depth', 'Depth')
        link_file_node(path + 'Vector', 'Vector')
        
        bpy.ops.render.render(animation = True)
        clear_output_nodes()
