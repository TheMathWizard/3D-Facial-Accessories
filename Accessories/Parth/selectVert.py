def selectVert(indices, obj):
    obj = bpy.context.object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    vertices = [e for e in bm.verts]
    oa = bpy.context.active_object
    for vert in vertices:
        if vert.index in indices:
            vert.select = True
        else:
            vert.select = False
    bmesh.update_edit_mesh(me, True)