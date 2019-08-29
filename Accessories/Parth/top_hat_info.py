import os

cwd = os.getcwd()
face_mesh_addr = cwd+'/Models/fully_stitched/'
face_mesh_name = 'full_coloured_2'
acc_mesh_addr = cwd+'/Models/cap/'
acc_mesh_name = 'top_hat'
	
#desc = [right temple, right back, front right, front left, left back, left temple,]
head_ids = [39254, 173076, 23620, 24241, 50796, 62272] 
#top_hat
acc_ids = [15085, 13699, 14109, 14208, 13614, 15544]

T_b_edit = [[ 9.99999898e-01, -2.22862204e-07,  1.58594335e-07,
        -1.77635684e-15],
       [-2.48622493e-06,  9.99997486e-01,  1.98566740e-06,
        -4.26325641e-14],
       [ 4.90412216e-10,  2.20107941e-09,  9.99999949e-01,
         5.55111512e-17],
       [-1.18319325e-08, -2.67216049e-02,  1.23219736e-08,
         1.00000000e+00]]