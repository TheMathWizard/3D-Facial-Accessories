import bpy
import bmesh
import pickle
import sys
from scipy.spatial import procrustes
import numpy as np
import os

#########################################################################
# Copy the '<acc>_info.py' file here to assign the corresponding values to the variables
#########################################################################
cwd = os.getcwd()
face_mesh_addr = cwd+'/Models/fully_stitched/'
face_mesh_name = 'full_stitch2'
acc_mesh_addr = cwd+'/Models/cap/'
acc_mesh_name = 'red_cap'

#desc = [right temple, right back, front right, front left, left back, left temple,]
head_ids = [148279, 150845, 23262, 24628, 150820, 148133] 
#red_cap
acc_ids = [336, 90, 467, 256, 75, 541]
#correction matrix
T_b_edit = [[ 1.31757583e+00, -5.51603913e-08,  2.11748545e-08,  0.00000000e+00], [ 4.54939619e-07,  1.31757617e+00, -1.05771165e-07, -3.55271368e-15], [-1.30586080e-07, -8.02016839e-08,  1.31757587e+00, 0.00000000e+00], [ 1.55399330e-03, -3.79501733e-02,  2.15527018e-02,  1.00000000e+00]]

#########################################################################

bpy.ops.import_mesh.ply(filepath = acc_mesh_addr + acc_mesh_name + '.ply')
bpy.ops.import_mesh.ply(filepath = face_mesh_addr + face_mesh_name + '.ply')

face_ob = bpy.data.objects[face_mesh_name]
face_me = face_ob.data

acc_ob = bpy.data.objects[acc_mesh_name]
acc_me = acc_ob.data

print('vertices: ')

A = []
for i in head_ids:
    A.append((face_ob.matrix_world * face_me.vertices[i].co).to_tuple())

A = np.array(A)

B = []
for i in acc_ids:
    B.append((acc_ob.matrix_world * acc_me.vertices[i].co).to_tuple())

B = np.array(B)

def transformObj(obj, mat):
    for vert in obj.data.vertices:
        vert_4d = vert.co.to_4d() * mat
        for i in range(3):
            vert.co[i] = vert_4d[i] / vert_4d[3]
        	
mtx1_o, mtx2_o, disparity = procrustes(A, B)
w = np.array([[1], [1], [1], [1]])
a = A[0:4]
b = B[0:4]
mtx1 = mtx1_o[0:4]
mtx2 = mtx2_o[0:4]
aw = np.append(a, w, axis=1)
bw = np.append(b, w, axis=1)
mtx1w = np.append(mtx1, w, axis=1)
mtx2w = np.append(mtx2, w, axis=1)

T_a = np.matmul(np.linalg.inv(aw), mtx1w)
T_b = np.matmul(np.linalg.inv(bw), mtx2w)

transformObj(face_ob, Matrix(T_a))
transformObj(acc_ob, Matrix(T_b))

# Correction matrix
transformObj(acc_ob, Matrix(T_b_edit))

# Save as .blend file
bpy.ops.wm.save_as_mainfile(filepath=cwd+'/pysaved.blend')
