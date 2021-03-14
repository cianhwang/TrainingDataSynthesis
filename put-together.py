import bpy
from mathutils import Vector
import random
from math import radians
import math

def add_obj_modifier(obj):
    subsurf_mod = obj.modifiers.new(name = "Subdivision",type='SUBSURF')
    subsurf_mod.subdivision_type = 'SIMPLE'
    subsurf_mod.show_only_control_edges = False
    subsurf_mod.levels = 2

def add_mesh_obj(type, size = None, is_modifier = True):
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
        
    obj = bpy.context.object
    if is_modifier:
        add_obj_modifier(obj)
    return obj

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
    if type == "ShaderNodeTexVoronoi":
        tex.voronoi_dimensions = '4D'
    if type == "ShaderNodeTexMagic":
        tex.turbulence_depth = random.randint(1, 5)
    if params is not None:
        for name in params:
            tex.inputs[name].default_value = params[name]
    base_color = matnodes['Principled BSDF'].inputs['Base Color']
    mat.node_tree.links.new(base_color, tex.outputs['Color'])
    
    coord = matnodes.new("ShaderNodeTexCoord")
    mat.node_tree.links.new(coord.outputs['UV'], tex.inputs['Vector'])
    
    obj.data.materials.append(mat)
    return mat, tex

def make_uneven_surface(obj, mat, type = "ShaderNodeTexMusgrave", params = None, 
                        disp_method = "BOTH"):
#    mat = bpy.data.materials.new("mat_" + str(obj.name))
#    mat.use_nodes = True
    matnodes = mat.node_tree.nodes
    dispnode = matnodes.new("ShaderNodeDisplacement")
    if disp_method == "BOTH":
        dispnode.inputs["Scale"].default_value = 0.3
    disp = matnodes['Material Output'].inputs['Displacement']
    mat.node_tree.links.new(disp, dispnode.outputs['Displacement'])
    
    ## ShaderNodeTexNoise["Fac"]
    ## ShaderNodeTexMusgrave[0]
    tex = matnodes.new(type)
    if type == "ShaderNodeTexMusgrave":
        tex.musgrave_dimensions = '4D'
    elif type == "ShaderNodeTexNoise":
        tex.noise_dimensions = '4D'
    else
        raise NotImplementedError
    if params is not None:
        for name in params:
            tex.inputs[name].default_value = params[name]
    mat.node_tree.links.new(tex.outputs[0], dispnode.inputs['Height'])
    
    coord = matnodes.new("ShaderNodeTexCoord")
    mat.node_tree.links.new(coord.outputs['Object'], tex.inputs['Vector'])
    
    mat.cycles.displacement_method = disp_method
#    obj.data.materials.append(mat)

def tex_random_params(type):
    params = {}
    if type == "ShaderNodeTexVoronoi":
        params['Scale'] = random.randint(4, 6)
        params['W'] = random.randint(0, 10)
    elif type == "ShaderNodeTexMagic":
        params['Scale'] = random.randint(4, 6)
        params['Distortion'] = 1 + random.random()
    elif type == "ShaderNodeTexBrick":
        params['Scale'] = random.randint(2, 4)
        params['Color1'] = (random.random(), random.random(), random.random(), 1)
        params['Color2'] = (random.random(), random.random(), random.random(), 1)
    elif type == "ShaderNodeTexChecker":
        params['Scale'] = random.randint(6, 10)
        params['Color1'] = (random.random(), random.random(), random.random(), 1)
        params['Color2'] = (random.random(), random.random(), random.random(), 1)
    else:
        raise NotImplementedError
    return params

def surface_tex_random_params(type = "ShaderNodeTexMusgrave"):
    params = {}
    if type == "ShaderNodeTexMusgrave" or type == "ShaderNodeTexNoise":
        params['W'] = random.randint(0, 10)
        params['Scale'] = random.randint(2, 6)
        params['Detail'] = 1 + 2 * random.random()
    else:
        raise NotImplementedError
    return params

def gen_random_obj_with_texture():
    mesh_obj_list = ["cube", "uv_sphere", "cone"]
    obj = add_mesh_obj(random.choice(mesh_obj_list))
    tex_list = ["ShaderNodeTexVoronoi",
                    "ShaderNodeTexMagic",
                    "ShaderNodeTexBrick",
                    "ShaderNodeTexChecker"]
    type = random.choice(tex_list)
    mat, tex = add_texture(obj, type, tex_random_params(type))
    surface_list = ["ShaderNodeTexMusgrave", "ShaderNodeTexNoise"]
    surface_type = random.choice(surface_list)
    make_uneven_surface(obj, mat, 
                    params = surface_tex_random_params(surface_type))
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
                
def gen_random_animation(scene, obj_list, n_frames = 240, patition_len = 7):
    '''
    scene: bpy.context.scene
    obj_list: contains a list of mesh objects
    n_frames: length of the video
    ---
    gen random partition inside n_frames, 
    e.g. n_frames = 60, partition = [0, 10, 21, 33, 45, 52, 60]
    '''
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
    
    ''' initialize scene '''
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    #scene.cycles.device = 'GPU'
    scene.render.resolution_x = 4096
    scene.render.resolution_y = 4096
    scene.cycles.samples = 4096
    scene.cycles.max_bounces = 1
    scene.cycles.filter_width = 0.7 ## turn off anti-aliasing
    scene.frame_end = 6
#    
#    scene.render.use_border = True
#    scene.render.use_crop_to_border = True
#    scene.render.border_min_x = 900/scene.render.resolution_x
#    scene.render.border_max_x = 964/scene.render.resolution_x
#    scene.render.border_min_y = 500/scene.render.resolution_y
#    scene.render.border_max_y = 564/scene.render.resolution_y
    
    n_scenes = 1
    
    for scene_idx in range(n_scenes):
        ''' clear scene '''
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

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
    #    add_texture(background, "ShaderNodeTexChecker", {"Scale":20, 
    #                                "Color1":(0.2, 0.2, 0.0, 1)})
        mat, _ = add_texture(background, "ShaderNodeTexMagic", {"Scale": 20, "Distortion": 1.5})
        make_uneven_surface(background, mat, params = {"Scale": 1.0}, disp_method='BUMP')
        background.name = "background"
        
        ''' add objs '''
        n_obj = 20 #random.randint(1, 3)
        obj_list = [background]
        for i in range(n_obj):
            obj_list.append(gen_random_obj_with_texture())

        gen_random_animation(scene, obj_list, scene.frame_end)
        
#        ''' output '''
#        link_file_node(scene, 
#                    '/Users/qian/Downloads/blender_collection/scene{:02d}/Image'.format(scene_idx), 
#                    'Image')
#        link_file_node(scene, 
#                    '/Users/qian/Downloads/blender_collection/scene{:02d}/Depth'.format(scene_idx), 
#                    'Depth')
#        link_file_node(scene, 
#                    '/Users/qian/Downloads/blender_collection/scene{:02d}/Vector'.format(scene_idx), 
#                    'Vector')
#        
#        bpy.ops.render.render(animation = True)
#        
#        nodes = scene.node_tree.nodes
#        for i in range(3):
#            nodes.remove(nodes[-1])
