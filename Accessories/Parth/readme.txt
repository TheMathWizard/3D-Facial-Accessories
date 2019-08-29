README: Blender Alignment

CONTENTS:
(1) blender_align.py
(2) correction_matrix.py 
(3) <acc>_info.py
(4) selectVert.py


(1) blender_align.py

This is script aligns the face mesh and the accessory mesh in blender. The input file is (3) <acc>_info.py 
If <acc>_info.py has been generated then all we need to do is to run this script. 

(2) correction_matrix.py 

If we are creating (3) for the first time, then we'll need to provide the feature points first and run (1) until the last line (where it uses 'T_b_edit' AKA correction matrix). The alginment will be performed without correcion matrix. After this step, do any manual adjustments to the accessory. Once the manual adjustment is complete, run correction_matrix.py to get 'T_b_edit'. This value can be added to '<acc>_info.py' after which our input is complete and we can run (1).

(3) <acc>_info.py

This file contains the input information for (1) in the form of variable values. These are variables are:

- file name of face mesh and it's location
- file name of accessory mesh and it's location
- feature points of face mesh
- feature points of accesssory mesh
- correction matrix

(4) selectVert.py

This is just a utility function to display a list of points on the 3D view of blender. 


