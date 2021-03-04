import bpy
import bpy.context as C
import bpy.data as D
from random import randint

C.scene.render.engine = 'CYCLES'

C.scene.render.resolution_x = 256
C.scene.render.resolution_y = 256

#how many cubes you want to add
count = 1

for c in range(0,count):
    x = randint(-5,5)
    y = randint(-5,5)
    z = randint(-5,5)
    bpy.ops.mesh.primitive_cube_add(location=(x,y,z))