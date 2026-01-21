import bpy
import os
import sys

# Argument parsing for Blender
# sys.argv will contain ["blender", "--background", ..., "--python", "script.py", "--", "arg1", "arg2"]
# We need to find "--" and take arguments after it
try:
    args_start = sys.argv.index("--") + 1
    script_args = sys.argv[args_start:]
except ValueError:
    script_args = []

if len(script_args) < 2:
    print("[BLENDER][ERROR] Usage: blender ... -- <stl_path> <blend_out_path>")
    sys.exit(1)

STL_PATH = os.path.abspath(script_args[0])
BLEND_OUT = os.path.abspath(script_args[1])

print("[BLENDER] STL:", STL_PATH)
print("[BLENDER] BLEND OUT:", BLEND_OUT)

# Hard fail if STL missing
if not os.path.exists(STL_PATH):
    print(f"[BLENDER][ERROR] STL not found: {STL_PATH}")
    sys.exit(1)

# Ensure output directory exists
os.makedirs(os.path.dirname(BLEND_OUT), exist_ok=True)

# Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Import STL file
bpy.ops.wm.stl_import(filepath=STL_PATH)

objs = bpy.context.selected_objects
if not objs:
    print("[BLENDER][ERROR] STL import returned no objects")
    sys.exit(1)

# Ensure object is linked
scene = bpy.context.scene
for obj in objs:
    if obj.name not in scene.objects:
        scene.collection.objects.link(obj)

# Set active
bpy.context.view_layer.objects.active = objs[0]

# Save blend
bpy.ops.wm.save_as_mainfile(filepath=BLEND_OUT)

print("[BLENDER] Blend saved successfully")
