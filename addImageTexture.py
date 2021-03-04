#https://blender.stackexchange.com/questions/168056/connecting-a-texture-node-to-a-material-node-via-the-blender-python-api-for-blen
import bpy
from bpy import data as D
from bpy import context as C
from mathutils import *
from math import *

C = bpy.context
D = bpy.data

mat = bpy.data.materials.new('mat')
mat.use_nodes = True
matnodes = mat.node_tree.nodes

bpy.context.view_layer.objects.active.material_slots[0].material = mat

tex = matnodes.new('ShaderNodeTexVoronoi')
base_color = matnodes['Principled BSDF'].inputs['Base Color']
mat.node_tree.links.new(base_color, tex.outputs['Color'])
print(list(matnodes))
matnodes["Voronoi Texture"].inputs["Scale"].default_value = 9.5
