README: Blender Alignment by Roshan (no Procrustus)

CONTENTS:
(1) add_glasses.py
(2) backHead2.ply
(3) face1-texture.ply
(4) Data files : base_stats, border_verts, edge_loops
(5) align_gltf


(1) add_glasses.py

This is script aligns the face mesh and the accessory mesh in blender. The input files are (2) backHead2.ply, (3) face1-texture.ply, (4) Data files and any particular spectacle from (5)

Algorithm brief : The code stitches (2) with (3) using a primitive Blender edge loop algorithm and then aligns the chosen gltf from align_gltf  with the stitched model. For that we first use a properly (pre-aligned) glass model that was aligned with a base face. Then with the input (3) we compare it with the base face and scale the input proportionately until the glasses fit on it.


(2) backHead2.ply 

This is the back-head model which required to complete the 3D of Scalismo generated face (3)

(3) face1-texture.ply

This is the textured 3D face model that is generated from Scalismo.

(4) align_gltf

This contains five different 3D spectacles for testing. It also has their corresponding version with a base face 3D model and the with input 3D model (3) 

