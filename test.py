import bpy
import random
from math import radians
import math
import sys
sys.path.append("C:\\Users\\qh38\\Desktop")
from utils import *

mesh_obj_list = ["plane", "cube", "uv_sphere", "cylinder", "cone", "torus"]
tex_list = ["ShaderNodeTexVoronoi",
                    "ShaderNodeTexMagic",
                    "ShaderNodeTexBrick",
                    "ShaderNodeTexChecker"]
surface_list = ["ShaderNodeTexMusgrave", "ShaderNodeTexNoise"]

def rand():
    return random.random()*2-1

if __name__ == '__main__':
#    add_array_cameras(
#        locs = [(0, 0, 0), (0, 0, 0), (0.04, 0, 0), (0.04, 0, 0.04), (0, 0, 0.04)],
#        rots = [(math.pi/2, 0, 0)] * 5,
#        fs = [12, 12, 8, 8, 8],
#        sensor_widths = [3.84] * 5,
#        track_to=False
#    )
#    sy = random.random()*1
#    ly = sy + 1 + random.random()*8.5
#    sx, sz = random.random()*(ly-sy)*0.07, random.random()*(ly-sy)*0.07
#    lx, lz = rand()*(ly-sy)*0.15, rand()*(ly-sy)*0.1
#    rx, ry, rz = rand()*math.pi/10, rand()*math.pi, rand()*math.pi/10
#    obj = add_mesh_obj('cube')
#    obj.location = (lx, ly, lz)
#    obj.scale = (sx, sy, sz)
#    obj.rotation_euler = (rx, ry, rz)

#    add_light((0, 5, 2), energy = 1000, light_type = 'AREA', light_color=(1.0, 1.0, 1.0), size = 10, size_y = 10)

#    obj = add_mesh_obj('cube')
#    obj = set_rand_pos(obj)

#    background = add_mesh_obj('plane')
#    background.location = (0, 10, 0)
#    background.rotation_euler = (math.pi/2, 0, 0)
#    background.scale = (3, 2, 1)