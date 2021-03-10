import bpy

def make_uneven_surface(obj):
    mat = bpy.data.materials.new("mat_" + str(obj.name))
    mat.use_nodes = True
    matnodes = mat.node_tree.nodes
    dispnode = matnodes.new("ShaderNodeDisplacement")
    disp = matnodes['Material Output'].inputs['Displacement']
    dispnode.inputs["Scale"].default_value = 0.3
    mat.node_tree.links.new(disp, dispnode.outputs['Displacement'])
    
    ## ShaderNodeTexVoronoi["Distance"]
    ## ShaderNodeTexMagic["Fac"]
    ## ShaderNodeTexMusgrave[0]
    tex = matnodes.new("ShaderNodeTexMusgrave")
    mat.node_tree.links.new(tex.outputs[0], dispnode.inputs['Height'])
    obj.data.materials.append(mat)

bpy.context.scene.render.engine = 'CYCLES'

obj = bpy.context.object

subsurf_mod = obj.modifiers.new(name = "Subdivision",type='SUBSURF')
subsurf_mod.subdivision_type = 'SIMPLE'
subsurf_mod.show_only_control_edges = False
subsurf_mod.levels = 2
make_uneven_surface(obj)
obj.data.materials[0].cycles.displacement_method = 'BOTH'
    






