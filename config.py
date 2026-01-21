import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Input/Output Config
DEFAULT_INPUT_IMAGE = os.path.join(BASE_DIR, "uploads", "blueprints", "bluprnt.png")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
GEOMETRY_JSON_PATH = os.path.join(OUTPUT_DIR, "data", "geometry.json")
MERGED_STL_PATH = os.path.join(OUTPUT_DIR, "stl", "merged.stl")
BLENDER_MODEL_PATH = os.path.join(OUTPUT_DIR, "blender", "model.blend")

# Paths to External Tools
# User's Blender path. Modify this if running on a different machine.
BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"

# Parameters
SCALE = 0.05
THICKNESS = 0.5
HEIGHT = 5.0
