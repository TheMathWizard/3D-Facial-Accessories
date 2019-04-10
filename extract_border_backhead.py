import bpy
import bmesh
import pickle

bpy.ops.import_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/backHead2_displaced.ply')
bpy.data.objects['backHead2_displaced'].name = 'backHead2'
obj = bpy.context.editable_objects[0]
me = obj.data
bpy.ops.object.editmode_toggle()
# Get a BMesh representation
bm = bmesh.from_edit_mesh(me)

border_faces = []
with open('/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/border_faces', 'rb') as f:
    border_faces = pickle.load(f)

bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()
bm.faces.ensure_lookup_table()

for f in bm.faces:
    f.select = False

for index in border_faces:
    bm.faces[index].select = True

bpy.ops.mesh.duplicate()
bpy.ops.mesh.separate(type='SELECTED')
bpy.ops.object.editmode_toggle()
bpy.data.objects['backHead2'].select = False
bpy.context.scene.objects.active = bpy.data.objects['backHead2.001']

obj = bpy.context.scene.objects.active
bpy.ops.object.editmode_toggle()
bm = bmesh.from_edit_mesh(obj.data)
for f in bm.faces:
    f.select = True
bpy.ops.mesh.poke()
bpy.ops.mesh.remove_doubles()
bpy.ops.object.editmode_toggle()

bpy.ops.export_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/head_border.ply', use_normals=False, use_uv_coords=False)
