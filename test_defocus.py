import bpy

def add_defocus_node(scene, z_scale = 1):
    scene.use_nodes = True
    nodes = scene.node_tree.nodes
    node_render = nodes['Render Layers']
    
    node_norm = nodes.new(type="CompositorNodeNormalize")
    scene.node_tree.links.new(node_render.outputs['Depth'], 
                        node_norm.inputs['Value'])
    
    node_defocus = nodes.new(type="CompositorNodeDefocus")
    node_defocus.z_scale = z_scale
    scene.node_tree.links.new(node_render.outputs['Image'], 
                        node_defocus.inputs['Image'])
    scene.node_tree.links.new(node_norm.outputs['Value'], 
                        node_defocus.inputs['Z'])
                        
    node_file = nodes.new("CompositorNodeOutputFile")
    node_file.base_path = "/Users/qian/Desktop/"
    node_file.format.file_format = 'PNG'
    node_file.format.color_depth = '8'
    scene.node_tree.links.new(node_defocus.outputs['Image'],node_file.inputs['Image'])


if __name__ == "__main__":
    bpy.context.scene.render.engine = 'CYCLES'
    scene = bpy.context.scene
    add_defocus_node(scene, 10)
    bpy.ops.render.render(write_still = True)
#    for ob in scene.objects:
#        if ob.type == 'MESH':
#            ob.select_set(True)
#        else: 
#            ob.select_set(False)
#    bpy.ops.object.delete()

#    bpy.ops.mesh.primitive_plane_add()
#    obj = bpy.context.object
    