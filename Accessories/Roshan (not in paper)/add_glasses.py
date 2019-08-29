import bpy
import bmesh
import pickle
import os

cwd = os.getcwd()

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
     
    with open(cwd+'/base_stats', 'rb') as fp:
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
    zdisp = max(bminz-minz, 0) + 60 * (sz-1)
    bpy.ops.object.editmode_toggle()
    
    return scale, zdisp


mesh = 'face1-texture'

bpy.ops.import_mesh.ply(filepath=cwd+'/backHead2.ply')
bpy.ops.import_mesh.ply(filepath=cwd+'/'+mesh+'.ply')

index = -1
for i, obj in enumerate(bpy.context.editable_objects):
    if(obj.name==mesh):
        index = i
        break

scale, zdisp = wrt_base(index)

print(zdisp)

bpy.data.objects['backHead2'].scale = scale
bpy.data.objects['backHead2'].location[2] = -zdisp

bpy.ops.object.join()
obj = bpy.context.editable_objects[0]
me = obj.data

bpy.ops.object.editmode_toggle()
# Get a BMesh representation
bm = bmesh.from_edit_mesh(me)

bm.faces.active = None

with open(cwd+'/edge_loops', 'rb') as f:
     toBeSelected = pickle.load(f)
     
with open(cwd+'/border_verts', 'rb') as f:
     toBeSelectedVerts = pickle.load(f)

bm.verts.ensure_lookup_table()
bm.edges.ensure_lookup_table()

lst = []
# Modify the BMesh, can do anything here...
for v in bm.verts:
    v.select = False
    
for e in bm.edges:
    e.select = False
    
for index in toBeSelectedVerts:
    bm.verts[index].select = True
    
for index in toBeSelected:
    bm.edges[index].select = True

# Show the updates in the viewport
# and recalculate n-gon tessellation.
bmesh.update_edit_mesh(me, True)

bpy.ops.mesh.bridge_edge_loops()
bpy.ops.mesh.remove_doubles()
bpy.ops.object.mode_set(mode="OBJECT")
bpy.ops.object.shade_smooth()

bpy.ops.export_mesh.ply(filepath=cwd+'/'+mesh+'_full.ply', use_normals=False, use_uv_coords=False)

glass_folder = 'glasses_black'

bpy.ops.import_scene.gltf(filepath=cwd+'/align_gltf/all gltf/'+glass_folder+'_align/scene.gltf')
#bpy.ops.import_mesh.ply(filepath='/Users/Roshan/Documents/Academics/BTP/Blenders/face_stitch/'+mesh+'_full.ply')

for i, obj in enumerate(bpy.context.editable_objects):
    if(obj.name.find('roshan')!=-1):
        obj.scale = scale

bpy.ops.export_scene.gltf(filepath=cwd+'/align_gltf/all gltf/'+glass_folder+'_total/scene.gltf')

