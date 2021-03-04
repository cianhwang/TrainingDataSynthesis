## http://danielhnyk.cz/creating-animation-blender-using-python/

import bpy  
from mathutils import Vector

## useful shortcut
scene = bpy.context.scene
scene.render.engine = 'CYCLES'
scene.render.resolution_x = 64
scene.render.resolution_y = 64
scene.cycles.samples = 512
bpy.context.scene.cycles.filter_width = 0.01 ## turn off anti-aliasing


## this shows you all objects in scene
#scene.objects.keys()

## when you start default Blender project, first object in scene is a Cube
#kostka = scene.objects[0]

## you can change location of object simply by setting the values
#kostka.location = (1,2,0)

## same with rotation
#kostka.rotation_euler = (45,0,0)

## this will make object cease from current scene
#bpy.context.collection.objects.unlink(kostka)

## clear everything for now
#scene.camera = None  
#for obj in scene.objects:  
#    bpy.context.collection.objects.unlink(obj)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# create sphere and make it smooth
bpy.ops.mesh.primitive_uv_sphere_add(radius = 3, location = (2,1,2))  
#bpy.ops.object.shade_smooth()  
kule = bpy.context.object

# create new cube
bpy.ops.mesh.primitive_cube_add(size = 4, location = (-2,1,2))  
kostka = bpy.context.object

# create plane 
bpy.ops.mesh.primitive_plane_add(location=(0,0,0))  
plane = bpy.context.object  
plane.dimensions = (20,20,0)

## for every object add material - here represented just as color
#for scale, ob in zip([3, 5, 7], [kule, kostka, plane]):  
#    mat = bpy.data.materials.new("mat_" + str(ob.name))
#    mat.use_nodes = True
#    matnodes = mat.node_tree.nodes
#    tex = matnodes.new('ShaderNodeTexVoronoi')
#    base_color = matnodes['Principled BSDF'].inputs['Base Color']
#    mat.node_tree.links.new(base_color, tex.outputs['Color'])
#    matnodes["Voronoi Texture"].inputs["Scale"].default_value = scale
#    ob.data.materials.append(mat)

ob = kule
mat = bpy.data.materials.new("mat_" + str(ob.name))
mat.use_nodes = True
matnodes = mat.node_tree.nodes
tex = matnodes.new('ShaderNodeTexVoronoi')
base_color = matnodes['Principled BSDF'].inputs['Base Color']
mat.node_tree.links.new(base_color, tex.outputs['Color'])
ob.data.materials.append(mat)

ob = kostka
mat = bpy.data.materials.new("mat_" + str(ob.name))
mat.use_nodes = True
matnodes = mat.node_tree.nodes
tex = matnodes.new('ShaderNodeTexMagic')
tex.inputs['Scale'].default_value = 1
tex.inputs['Distortion'].default_value = 5
base_color = matnodes['Principled BSDF'].inputs['Base Color']
mat.node_tree.links.new(base_color, tex.outputs['Color'])
ob.data.materials.append(mat)

ob = plane
mat = bpy.data.materials.new("mat_" + str(ob.name))
mat.use_nodes = True
matnodes = mat.node_tree.nodes
tex = matnodes.new('ShaderNodeTexBrick')
base_color = matnodes['Principled BSDF'].inputs['Base Color']
mat.node_tree.links.new(base_color, tex.outputs['Color'])
ob.data.materials.append(mat)

# now add some light
lamp_data = bpy.data.lights.new(name="lampa", type='POINT')  
lamp_object = bpy.data.objects.new(name="Lampicka", object_data=lamp_data)  
bpy.context.collection.objects.link(lamp_object)  
lamp_object.location = (-3, 0, 7)
lamp = bpy.data.lights[lamp_data.name]
lamp.energy = 1000

# and now set the camera
cam_data = bpy.data.cameras.new(name="cam")  
cam_ob = bpy.data.objects.new(name="Kamerka", object_data=cam_data)  
bpy.context.collection.objects.link(cam_ob)  
cam_ob.location = (0, 1, 12)  
cam_ob.rotation_euler = (0,0,0.3)  
cam = bpy.data.cameras[cam_data.name]  
cam.lens = 25
scene.camera = cam_ob


### animation
positions = (0,0,2),(0,1,2),(3,2,1),(3,4,1),(1,2,1)

# start with frame 0
number_of_frame = 0  
bpy.context.scene.frame_end = 4
bpy.context.scene.render.fps = 1

for pozice in positions:

    # now we will describe frame with number $number_of_frame
    scene.frame_set(number_of_frame)

    # set new location for sphere $kule and new rotation for cube $kostka
    kule.location = pozice
    kule.keyframe_insert(data_path="location", index=-1)

    kostka.rotation_euler = pozice
    kostka.keyframe_insert(data_path="rotation_euler", index=-1)

    plane.location += Vector(pozice)/5
    plane.keyframe_insert(data_path="location", index=-1)
    # move next 10 frames forward - Blender will figure out what to do between this time
    number_of_frame += 1
    
    
### ---------- save file -------------
scene.use_nodes = True
nodes = scene.node_tree.nodes

bpy.context.scene.view_layers["View Layer"].use_pass_vector = True

render_layers = nodes['Render Layers']


def create_file_node(nodes, base_path, 
                        format = 'OPEN_EXR', color_depth = '16'):
    file_node = nodes.new("CompositorNodeOutputFile")
    file_node.base_path = base_path
    file_node.format.file_format = format
    file_node.format.color_depth = color_depth
    return file_node
    
    


output_file = nodes.new("CompositorNodeOutputFile")
output_file.base_path = "/Users/qian/Desktop/Vector"
output_file.format.file_format = 'OPEN_EXR'
output_file.format.color_depth = '16'

scene.node_tree.links.new(
    render_layers.outputs['Vector'],
    output_file.inputs['Image']
)

output_file = nodes.new("CompositorNodeOutputFile")
output_file.base_path = "/Users/qian/Desktop/Depth"
output_file.format.file_format = 'OPEN_EXR'
output_file.format.color_depth = '16'

scene.node_tree.links.new(
    render_layers.outputs['Depth'],
    output_file.inputs['Image']
)

output_file = nodes.new("CompositorNodeOutputFile")
output_file.base_path = "/Users/qian/Desktop/Image"
output_file.format.color_depth = '16'
output_file.format.color_depth = '16'

scene.node_tree.links.new(
    render_layers.outputs['Image'],
    output_file.inputs['Image']
)

bpy.ops.render.render(animation = True)