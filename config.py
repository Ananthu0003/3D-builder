import os

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Input/Output Config
DEFAULT_INPUT_IMAGE = os.path.join(BASE_DIR, "uploads", "blueprints", "floor.jpg")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
GEOMETRY_JSON_PATH = os.path.join(OUTPUT_DIR, "data", "geometry.json")
MERGED_STL_PATH = os.path.join(OUTPUT_DIR, "stl", "merged.stl")

# Viewer Config
VIEWER_MODEL_PATH = "output/stl/merged.stl"

# Parameters
SCALE = 0.05
THICKNESS = 0.5
HEIGHT = 5.0
PLATE_HEIGHT = 0.2
