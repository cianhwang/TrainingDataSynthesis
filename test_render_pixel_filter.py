import bpy

bpy.context.scene.render.engine = 'CYCLES'
scene = bpy.context.scene
for ob in scene.objects:
    if ob.type == 'MESH':
        ob.select_set(True)
    else: 
        ob.select_set(False)
bpy.ops.object.delete()

bpy.ops.mesh.primitive_uv_sphere_add()
obj = bpy.context.object

