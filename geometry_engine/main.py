from geometry_engine.builder import build_all_elements
from geometry_engine.exporter import export_stl
import json
import os

def generate_stl(json_path: str, stl_output_path: str):
    """
    Reads geometry JSON and generates an STL file.
    """
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"Geometry JSON not found at: {json_path}")

    with open(json_path, "r") as f:
        data = json.load(f)

    print(f"[GEOMETRY] Building {len(data['elements'])} elements...")
    solids = build_all_elements(data["elements"])

    # Ensure output directory exists
    os.makedirs(os.path.dirname(stl_output_path), exist_ok=True)

    print(f"[GEOMETRY] Exporting to {stl_output_path}...")
    export_stl(solids, stl_output_path)

if __name__ == "__main__":
    # Default behavior for standalone execution (for backward compatibility or testing)
    # Assumes run from root or with specific relative paths, but using config is preferred.
    import sys
    
    # Simple fallback if no args provided, mostly for testing
    input_json = "geometry.json"
    output_stl = "output/stl/merged.stl"
    
    generate_stl(input_json, output_stl)
