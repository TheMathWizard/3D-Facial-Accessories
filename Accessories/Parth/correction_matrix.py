 // Correction Matrix
// run the following code after manually adjusting the accessory.
B_edit = []
for i in acc_ids:
    B_edit.append((acc_ob.matrix_world * acc_me.vertices[i].co).to_tuple())

B_edit = np.array(B_edit)
b_edit = B_edit[0:4]
bw_edit = np.append(b_edit, w, axis=1)

T_b_edit = np.matmul(np.linalg.inv(mtx2w), bw_edit)

print (repr(T_b_edit))
