import bpy
import bmesh
import pickle
import sys

def wrt_base(mesh_index):
    # Get the active mesh
    obj = bpy.context.editable_objects[mesh_index]
    me = obj.data

    bpy.ops.object.editmode_toggle()
    # Get a BMesh representation
    bm = bmesh.from_edit_mesh(me)

    bm.faces.active = None

    bm.verts.ensure_lookup_table()

    maxx = minx = bm.verts[0].co.x 
    maxy = miny = bm.verts[0].co.y
    maxz = minz = bm.verts[0].co.z

    # Modify the BMesh, can do anything here...
    for v in bm.verts:
        if(v.co.x > maxx):
            maxx = v.co.x
        elif(v.co.x < minx):
            minx = v.co.x
        if(v.co.y > maxy):
            maxy = v.co.y
        elif(v.co.y < miny):
            miny = v.co.y
        if(v.co.z > maxz):
            maxz = v.co.z
        elif(v.co.z < minz):
            minz = v.co.z
            
    res = (maxx, minx, maxy, miny, maxz, minz)
    rx = maxx-minx
    ry = maxy-miny
    rz = maxz-minz
     
    with open('/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/base_stats', 'rb') as fp:
        base = pickle.load(fp)
        
    bmaxx, bminx, bmaxy, bminy, bmaxz, bminz = base
    brx = bmaxx-bminx
    bry = bmaxy-bminy
    brz = bmaxz-bminz

    #print(rx, brx)
    #print(ry, bry)
    #print(rz, brz)

    sx = rx/brx
    sy = ry/bry
    sz = (sx+sy)/2

    print(sx, sy, sz)
    #print(minz, bminz)
    scale = (sx, sy, sz)
    zdisp = max(bminz-minz, 0) + (60 * (sz-1))
    bpy.ops.object.editmode_toggle()
  
    return scale, zdisp


mesh = 'femface'
#mesh = 'face1-texture'

bpy.ops.import_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/backHead2.ply')
bpy.ops.import_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/'+mesh+'.ply')

index = -1
for i, obj in enumerate(bpy.context.editable_objects):
    if(obj.name==mesh):
        index = i
        break

scale, zdisp = wrt_base(index)

print(zdisp)

bpy.data.objects['backHead2'].scale = scale
bpy.data.objects['backHead2'].location[2] = -zdisp

for obj in bpy.context.editable_objects:
	bpy.data.objects[obj.name].select = False

bpy.data.objects['backHead2'].select = True
bpy.context.scene.objects.active = bpy.data.objects['backHead2']
bpy.ops.export_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/backHead2_displaced.ply', use_normals=False, use_uv_coords=False)
