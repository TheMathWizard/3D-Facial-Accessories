import subprocess

subprocess.run(["/Applications/Blender/blender.app/Contents/MacOS/blender", "--background", "--python", "adjust_backhead.py"]) #need mesh input
subprocess.run(["/Applications/Blender/blender.app/Contents/MacOS/blender", "--background","--python", "extract_border_backhead.py"])
subprocess.run(["python3", "meshing.py"]) #need mesh input
subprocess.run(["/Applications/Blender/blender.app/Contents/MacOS/blender", "--background","--python", "stitched_with_head.py"])
subprocess.run(["python3", "color_full_model.py"])

#/Applications/Blender/blender.app/Contents/MacOS/blender --python adjust_backhead.py
#/Applications/Blender/blender.app/Contents/MacOS/blender --python extract_border_backhead.py

