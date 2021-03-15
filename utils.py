import bpy
from math import radians
import random

def init_scene(res = 4096, n_frames = 240, use_gpu = False, render_region=True, render_params = None):
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.device = 'GPU' if use_gpu else 'CPU'
    scene.render.resolution_x = res
    scene.render.resolution_y = res
    scene.cycles.samples = 4096
    scene.cycles.preview_samples = 1
    scene.cycles.max_bounces = 1
    scene.cycles.filter_width = 0.7 ## turn off anti-aliasing
    scene.frame_end = n_frames
    if render_region:
        scene.render.use_border = True
        scene.render.use_crop_to_border = True
        x1, x2, y1, y2 = render_params
        scene.render.border_min_x = x1/scene.render.resolution_x
        scene.render.border_max_x = x2/scene.render.resolution_x
        scene.render.border_min_y = y1/scene.render.resolution_y
        scene.render.border_max_y = y2/scene.render.resolution_y
    
def clear_scene(clear_mesh_only = False):
    data = bpy.data
    for ob in data.objects:
        if ob.type == 'MESH':
            data.objects.remove(data.objects[ob.name], do_unlink = True)
    if clear_mesh_only is False:
        for ob in data.cameras:
            data.cameras.remove(data.cameras[ob.name], do_unlink = True)
        for ob in data.lights:
            data.lights.remove(data.lights[ob.name], do_unlink = True)
    
def add_light(loc, energy = 10000):
    '''
    loc: 3-element tuple
    '''
    lamp_data = bpy.data.lights.new(name="light", type='POINT')  
    lamp_object = bpy.data.objects.new(name="light_obj", object_data=lamp_data)  
    bpy.context.collection.objects.link(lamp_object)  
    #lamp_object.location = (-3, 0, 7)
    lamp_object.location = loc
    lamp = bpy.data.lights[lamp_data.name]
    lamp.energy = energy
    
def add_camera(loc, rot, lens = 100):
    '''
    loc: 3-element tuple
    rot: 3-element tuple in radians
    '''
    cam_data = bpy.data.cameras.new(name="camera")  
    cam_ob = bpy.data.objects.new(name="camera_obj", object_data=cam_data)  
    bpy.context.collection.objects.link(cam_ob)   
    cam_ob.location = loc 
    cam_ob.rotation_euler = rot
    cam = bpy.data.cameras[cam_data.name]  
    cam.lens = lens
    bpy.context.scene.camera = cam_ob
    
def add_mesh_obj(type, params = {}, is_modifier = True):
    '''                                                               
    type: plane, cube, cylinder, cone, uv_sphere, torus             
    params: dict                                                           
    '''
    if type == "plane":
        bpy.ops.mesh.primitive_plane_add(**params)
    elif type == "cube":
        bpy.ops.mesh.primitive_cube_add(**params)
    elif type == "uv_sphere":
        bpy.ops.mesh.primitive_uv_sphere_add(**params)
    elif type == "cylinder":
        bpy.ops.mesh.primitive_cylinder_add(**params)
    elif type == "cone":
        bpy.ops.mesh.primitive_cone_add(**params)
    elif type == "torus":
        bpy.ops.mesh.primitive_torus_add(**params)
    else:
        raise NotImplementedError
    obj = bpy.context.object
    return obj

def add_modifier(obj, level = 2):
    subsurf_mod = obj.modifiers.new(name = "Subdivision",type='SUBSUR\
F')
    subsurf_mod.subdivision_type = 'SIMPLE'
    subsurf_mod.show_only_control_edges = False
    subsurf_mod.levels = level
    subsurf_mod.render_levels = level

def add_material(obj):
    mat = bpy.data.materials.new("mat_" + str(obj.name))
    mat.use_nodes = True
    obj.data.materials.append(mat)
    return mat

def add_texture(obj, mat, type, params = None):
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

def tex_random_params(type):
    params = {}
    if type == "ShaderNodeTexVoronoi":
        params['Scale'] = 10 + 20 * random.random()
        params['W'] = random.randint(-100, 100) * 0.2
    elif type == "ShaderNodeTexMagic":
        params['Scale'] = 10 + 20 * random.random()
        params['Distortion'] = 0.5 + 2.5 * random.random()
    elif type == "ShaderNodeTexBrick":
        params['Scale'] = 10 + 20 * random.random()
        params['Color1'] = (random.random(),random.random(),random.random(),1)
        params['Color2'] = (random.random(),random.random(),random.random(),1)
        params['Mortar'] = (random.random(),random.random(),random.random(),1)
        params['Mortar Size'] = random.random() * 0.1
    elif type == "ShaderNodeTexChecker":
        params['Scale'] = 40 + 20 * random.random()
        params['Color1'] = (random.random(),random.random(),random.random(),1)
        params['Color2'] = (random.random(),random.random(),random.random(),1)
    else:
        raise NotImplementedError
    return params

def displace_surface(obj, mat, type = "ShaderNodeTexMusgrave", 
                        params = None, disp_method = "BOTH"):                                                     
    matnodes = mat.node_tree.nodes
    dispnode = matnodes.new("ShaderNodeDisplacement")
    if disp_method == "BOTH":
        dispnode.inputs["Scale"].default_value = 0.3 * random.random()
    disp = matnodes['Material Output'].inputs['Displacement']
    mat.node_tree.links.new(disp, dispnode.outputs['Displacement'])

    ## ShaderNodeTexNoise["Fac"]                                              
    ## ShaderNodeTexMusgrave[0]                                               
    tex = matnodes.new(type)
    if type == "ShaderNodeTexMusgrave":
        tex.musgrave_dimensions = '4D'
    elif type == "ShaderNodeTexNoise":
        tex.noise_dimensions = '4D'
    else:
        raise NotImplementedError
    if params is not None:
        for name in params:
            tex.inputs[name].default_value = params[name]
    mat.node_tree.links.new(tex.outputs[0], dispnode.inputs['Height'])

    coord = matnodes.new("ShaderNodeTexCoord")
    mat.node_tree.links.new(coord.outputs['Object'], tex.inputs['Vector'])
    mat.cycles.displacement_method = disp_method
    
def surface_random_params(type = "ShaderNodeTexMusgrave"):
    params = {}
    if type == "ShaderNodeTexNoise":
        params['W'] = random.randint(-100, 100) * 0.2
        params['Scale'] = 10 + 20 * random.random()
        params['Detail'] = 1 + 2 * random.random()
        params['Distortion'] = -5 + 10 * random.random()
    elif type == "ShaderNodeTexMusgrave":
        params['W'] = random.randint(-100, 100) * 0.2
        params['Scale'] = 10 + 20 * random.random()
        params['Detail'] = 1 + 2 * random.random()
        params['Lacunarity'] = 5 * random.random()
    else:
        raise NotImplementedError
    return params

def link_file_node(base_path, output_type, 
                    format = 'OPEN_EXR', color_depth = '16'):
    '''                                                                       
    scene: bpy.context.scene                                                  
    base_path: output path to store image files                               
    output_type: 'Vector'/'Depth'/'Image'                                     
    format: 'PNG'/'OPEN_EXR'                                                  
    color_depth: default '16' bits for png files and '16' bits half float for\
 OpenExr files                                                                
    '''
    scene = bpy.context.scene
    scene.use_nodes = True
    nodes = scene.node_tree.nodes
    render_layers = nodes['Render Layers']
    ## assure render layer node has property vector                           
    scene.view_layers["View Layer"].use_pass_vector = True

    file_node = nodes.new("CompositorNodeOutputFile")
    file_node.base_path = base_path
    file_node.format.file_format = format
    file_node.format.color_depth = color_depth
    scene.node_tree.links.new(render_layers.outputs[output_type],
                            file_node.inputs['Image'])
                            
def clear_output_nodes():
    scene = bpy.context.scene
    nodes = scene.node_tree.nodes
    for node in nodes:
        if 'File Output' in node.name:
            nodes.remove(node)

if __name__ == "__main__":
#    random.seed("0038")
    init_scene()
    clear_scene()
    add_light((-3, 0, 7))
    add_camera((7, -7, 5), (radians(63.6), 0, radians(46.7)))
    obj = add_mesh_obj("uv_sphere", {})
    add_modifier(obj, 4)
    mat = add_material(obj)
    add_texture(obj, mat, "ShaderNodeTexBrick", 
                        tex_random_params("ShaderNodeTexChecker"))
    displace_surface(obj, mat, "ShaderNodeTexMusgrave",
                        surface_random_params("ShaderNodeTexMusgrave"))
    link_file_node('./', 'Image')
    link_file_node('./', 'Depth')
    clear_output_nodes()
