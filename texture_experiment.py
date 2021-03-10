import bpy

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

def make_uneven_surface(obj):
    mat = bpy.data.materials.new("mat_" + str(obj.name))
    mat.use_nodes = True
    matnodes = mat.node_tree.nodes
    dispnode = matnodes.new("ShaderNodeDisplacement")
    disp = matnodes['Material Output'].inputs['Displacement']
    mat.node_tree.links.new(disp, dispnode.outputs['Displacement'])
    
    ## ShaderNodeTexVoronoi["Distance"]
    ## ShaderNodeTexMagic["Fac"]
    ## ShaderNodeTexMusgrave[0]
    tex = matnodes.new("ShaderNodeTexMusgrave")
    mat.node_tree.links.new(tex.outputs[0], dispnode.inputs['Height'])
    obj.data.materials.append(mat)

class BrickTexture:
    def __init__(self):
        self.name = "ShaderNodeTexBrick"
        self.Color1 = None
        self.Color2 = None
        self.Scale = 3

class CheckerTexture:
    def __init__(self):
        self.name = "ShaderNodeTexChecker"
        self.Color1 = None
        self.Color2 = None
        self.Scale = 8
        
class MagicTexture:
    def __init__(self):
        self.name = "ShaderNodeTexMagic"
        self.Scale = 5
        self.Depth = 1 # 1~5
        
class VoronoiTexture:
    def __init__(self):
        self.name = "ShaderNodeTexVoronoi"
        self.voronoi_dimensions = '4D' # 2D, 3D, 4D
        self.W = 1 # float, 0.1 difference will reflect on the colors


if __name__ == '__main__':
    obj = bpy.context.object
    obj.data.materials.clear()
#    ### ShaderNodeTexBrick: params
#    add_texture(obj, "ShaderNodeTexMagic")
    make_uneven_surface(obj)
    