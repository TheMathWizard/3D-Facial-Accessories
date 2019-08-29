import bpy
import bmesh
import pickle
import os

cwd = os.getcwd()
bpy.ops.import_mesh.ply(filepath=cwd+'/backHead2_displaced.ply')
bpy.ops.import_mesh.ply(filepath=cwd+'/extendedFace.ply')

bpy.ops.object.join()
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.remove_doubles()
bpy.ops.mesh.normals_make_consistent()
bpy.ops.object.editmode_toggle()
bpy.ops.export_mesh.ply(filepath=cwd+'/full_stitched.ply', use_normals=False, use_uv_coords=False)
