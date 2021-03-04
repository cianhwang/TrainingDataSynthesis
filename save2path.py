import bpy

bpy.context.scene.render.engine = 'CYCLES'
bpy.context.scene.render.resolution_x = 64
bpy.context.scene.render.resolution_y = 64


scene = bpy.context.scene
scene.use_nodes = True
nodes = scene.node_tree.nodes

bpy.context.scene.view_layers["View Layer"].use_pass_vector = True

render_layers = nodes['Render Layers']
output_file = nodes.new("CompositorNodeOutputFile")
output_file.base_path = "/Users/qian/Desktop/Vector"
output_file.format.file_format = 'OPEN_EXR'

scene.node_tree.links.new(
    render_layers.outputs['Vector'],
    output_file.inputs['Image']
)

output_file = nodes.new("CompositorNodeOutputFile")
output_file.base_path = "/Users/qian/Desktop/Depth"
output_file.format.file_format = 'OPEN_EXR'

scene.node_tree.links.new(
    render_layers.outputs['Depth'],
    output_file.inputs['Image']
)

output_file = nodes.new("CompositorNodeOutputFile")
output_file.base_path = "/Users/qian/Desktop/Image"
output_file.format.color_depth = '16'

scene.node_tree.links.new(
    render_layers.outputs['Image'],
    output_file.inputs['Image']
)

bpy.ops.render.render(write_still = True)