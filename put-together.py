import bpy
from mathutils import Vector
import random
from math import radians
import math

def add_mesh_obj(type, size = None):
    '''
    type: background(wrapper cube), cube, cone, uv_sphere
    size:
    
    leave other params like loc/trans_params to be default by now;
    loc/trans_params will be set by function set_animation(...)
    '''
    if type == "background":
        bpy.ops.mesh.primitive_cube_add(size = size) 
    elif type == "cube":
        bpy.ops.mesh.primitive_cube_add()
    elif type == "uv_sphere":
        bpy.ops.mesh.primitive_uv_sphere_add()
    elif type == "cone":
        bpy.ops.mesh.primitive_cone_add()
    else:
        raise NotImplementedError
    return bpy.context.object

def add_texture(obj, type, params = None):
    '''
    obj: type bpy_types.Object, can be assigned by bpy.context.object
    type/params: texture type/params
        supports modes:
        * ShaderNodeTexVoronoi, dict...
        * ShaderNodeTexMagic, 
        * ShaderNodeTexBrick, 
        * ShaderNodeTexChecker
        * ...
    '''
    mat = bpy.data.materials.new("mat_" + str(obj.name))
    mat.use_nodes = True
    matnodes = mat.node_tree.nodes
    tex = matnodes.new(type)
    if params is not None:
        for name in params:
            tex.inputs[name].default_value = params[name]
    base_color = matnodes['Principled BSDF'].inputs['Base Color']
    mat.node_tree.links.new(base_color, tex.outputs['Color'])
    
    coord = matnodes.new("ShaderNodeTexCoord")
    mat.node_tree.links.new(coord.outputs['UV'], tex.inputs['Vector'])
    
    obj.data.materials.append(mat)
    return mat, tex

def gen_random_obj_with_texture():
    mesh_obj_list = ["cube", "uv_sphere", "cone"]
    obj = add_mesh_obj(random.choice(mesh_obj_list))
    tex_list = ["ShaderNodeTexVoronoi",
                    "ShaderNodeTexMagic",
                    "ShaderNodeTexBrick",
                    "ShaderNodeTexChecker"]
    mat, tex = add_texture(obj, random.choice(tex_list))
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
    scale =    (0.5 + random.random(), 
                0.5 + random.random(), 
                0.5 + random.random())
    return (location, rotation, scale)
                
def gen_random_animation(scene, obj_list, n_frames = 60):
    '''
    scene: bpy.context.scene
    obj_list: contains a list of mesh objects
    n_frames: length of the video
    ---
    gen random partition inside n_frames, 
    e.g. n_frames = 60, partition = [0, 10, 21, 33, 45, 52, 60]
    '''
    for obj in obj_list:
        if obj.name != "background":
    #        partition = get_rand_partition(n_frames) ## NOT IMPLEMENTED YET
            partition = [10*i for i in range(7)]
            for curr_time in partition:
                scene.frame_set(curr_time)
                trans_params = get_rand_trans()
                set_animation(obj, trans_params)
        else:
            partition = [10*i for i in range(7)]
            for curr_time in partition:
                scene.frame_set(curr_time)
                trans_params = get_rand_trans()
                set_animation(obj, trans_params, True)
            
    
def link_file_node(scene, base_path, output_type, format = 'OPEN_EXR', color_depth = '16'):
    '''
    scene: bpy.context.scene
    base_path: output path to store image files
    output_type: 'Vector'/'Depth'/'Image'
    format: 'PNG'/'OPEN_EXR'
    color_depth: default '16' bits for png files and '16' bits half float for OpenExr files
    '''
    scene.use_nodes = True
    nodes = scene.node_tree.nodes
    render_layers = nodes['Render Layers']
    
    ## assure render layer node has property vector
    scene.view_layers["View Layer"].use_pass_vector = True 

    file_node = nodes.new("CompositorNodeOutputFile")
    file_node.base_path = base_path
    file_node.format.file_format = format
    file_node.format.color_depth = color_depth
    
    scene.node_tree.links.new(render_layers.outputs[output_type],file_node.inputs['Image'])
    
if __name__ == '__main__':
    random.seed("qian038")
    
    ''' clear scene '''
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    ''' initialize scene '''
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.render.resolution_x = 64
    scene.render.resolution_y = 64
    scene.cycles.samples = 4096
    scene.cycles.max_bounces = 1
    scene.cycles.filter_width = 0.01 ## turn off anti-aliasing
    scene.frame_end = 60

    ''' add light source '''
    lamp_data = bpy.data.lights.new(name="light", type='POINT')  
    lamp_object = bpy.data.objects.new(name="light_obj", object_data=lamp_data)  
    bpy.context.collection.objects.link(lamp_object)  
    #lamp_object.location = (-3, 0, 7)
    lamp_object.location = (4, 1, 6)
    lamp = bpy.data.lights[lamp_data.name]
    lamp.energy = 10000

    ''' set camera '''
    cam_data = bpy.data.cameras.new(name="cam")  
    cam_ob = bpy.data.objects.new(name="cam_obj", object_data=cam_data)  
    bpy.context.collection.objects.link(cam_ob)  
    #cam_ob.location = (0, 1, 12)  
    cam_ob.location = (7, -7, 5)
    #cam_ob.rotation_euler = (0,0,0.3)  
    cam_ob.rotation_euler = (radians(63.6), 0, radians(46.7))
    cam = bpy.data.cameras[cam_data.name]  
    cam.lens = 100
    scene.camera = cam_ob
    
    ''' add background cube '''
    background = add_mesh_obj("background", 20)
    add_texture(background, "ShaderNodeTexChecker", {"Scale":20, 
                                "Color1":(0.2, 0.2, 0.0, 1)})
    background.name = "background"
    
    ''' test add obj '''
    obj1 = gen_random_obj_with_texture()
    obj2 = gen_random_obj_with_texture()  
    
    obj_list = [background, obj1, obj2]
    gen_random_animation(scene, obj_list)
    
    ''' output '''
    link_file_node(scene, 'Users/qian/Downloads/Image', 'Image')
    link_file_node(scene, 'Users/qian/Downloads/Depth', 'Depth')
    link_file_node(scene, 'Users/qian/Downloads/Vector', 'Vector')
    
#    bpy.ops.render.render(animation = True)