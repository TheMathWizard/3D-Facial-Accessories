import bpy
import bmesh
import pickle

bpy.ops.import_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/backHead2_displaced.ply')
bpy.ops.import_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/extendedFace.ply')

bpy.ops.object.join()
bpy.ops.object.editmode_toggle()
bpy.ops.mesh.remove_doubles()
bpy.ops.mesh.normals_make_consistent()
bpy.ops.object.editmode_toggle()
bpy.ops.export_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/full_stitched.ply', use_normals=False, use_uv_coords=False)
