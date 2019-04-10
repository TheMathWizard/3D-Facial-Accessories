import subprocess
Blender_Path = "/Applications/Blender/blender.app/Contents/MacOS/blender"
subprocess.run([Blender_Path, "--background", "--python", "adjust_backhead.py"])
subprocess.run([Blender_Path, "--background","--python", "extract_border_backhead.py"])
subprocess.run(["python3", "meshing.py"])
subprocess.run([Blender_Path, "--background","--python", "stitched_with_head.py"])
subprocess.run(["python3", "color_full_model.py"])

#/Applications/Blender/blender.app/Contents/MacOS/blender --python adjust_backhead.py
#/Applications/Blender/blender.app/Contents/MacOS/blender --python extract_border_backhead.py

