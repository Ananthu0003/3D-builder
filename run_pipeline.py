import math
import subprocess

from ai_engine.detector import detect_wall_lines
from ai_engine.walls import filter_axis_aligned, filter_short_lines
from ai_engine.clusters import cluster_lines
from ai_engine.normalize import normalize_lines
from ai_engine.deduplicate import deduplicate_lines
from ai_engine.skeleton import build_skeleton
from ai_engine.snap import snap_wall_endpoints
from ai_engine.topology import split_lines_at_intersections, remove_isolated_segments, detect_rooms_from_walls
from ai_engine.postprocess import geometry_from_polylines, save_geometry_json, plates_from_rooms
from geometry_engine.main import generate_stl
import cv2

import argparse
import os
import sys

# Import Configuration
import config

def centerline_to_polyline(line, thickness):
    x1, y1, x2, y2 = line
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy)
    if L < 1e-3:
        return None
    nx, ny = -dy / L, dx / L
    t = thickness / 2
    return [
        (x1 + nx*t, y1 + ny*t),
        (x2 + nx*t, y2 + ny*t),
        (x2 - nx*t, y2 - ny*t),
        (x1 - nx*t, y1 - ny*t),
    ]

def main():
    parser = argparse.ArgumentParser(description="Ship Builder Pipeline")
    parser.add_argument("--image", type=str, default=config.DEFAULT_INPUT_IMAGE, help="Path to blueprint image")
    args = parser.parse_args()

    INPUT_IMAGE = args.image
    if not os.path.exists(INPUT_IMAGE):
        print(f"[ERROR] Input image not found: {INPUT_IMAGE}")
        sys.exit(1)

    print(f"[PIPELINE] Processing: {INPUT_IMAGE}")

    # ---- AI ENGINE ----
    lines = detect_wall_lines(INPUT_IMAGE)
    
    # DEBUG: Visualization of raw detection
    debug_img = cv2.imread(INPUT_IMAGE)
    if debug_img is not None:
        for x1, y1, x2, y2 in lines:
            cv2.line(debug_img, (x1, y1), (x2, y2), (0, 0, 255), 2)
        debug_out_path = os.path.join(os.path.dirname(config.DEFAULT_INPUT_IMAGE), "debug_detected_lines.png")
        cv2.imwrite(debug_out_path, debug_img)
        print(f"[DEBUG] Saved detection debug image to: {debug_out_path}")

    lines = filter_axis_aligned(lines)
    lines = filter_short_lines(lines)
    lines = normalize_lines(lines)
    lines = deduplicate_lines(lines)

    clusters = cluster_lines(lines)
    skeleton = build_skeleton(clusters)
    skeleton = snap_wall_endpoints(skeleton)
    skeleton = split_lines_at_intersections(skeleton)
    skeleton = remove_isolated_segments(skeleton)
    
    # DEBUG: Visualization of final skeleton
    debug_skeleton_img = cv2.imread(INPUT_IMAGE)
    if debug_skeleton_img is not None:
        for x1, y1, x2, y2 in skeleton:
            # Use a different color (green) for the skeleton
            cv2.line(debug_skeleton_img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
        debug_out_path = os.path.join(os.path.dirname(config.DEFAULT_INPUT_IMAGE), "debug_skeleton.png")
        cv2.imwrite(debug_out_path, debug_skeleton_img)
        print(f"[DEBUG] Saved skeleton debug image to: {debug_out_path}")

    # scale
    skeleton = [(x1*config.SCALE, y1*config.SCALE, x2*config.SCALE, y2*config.SCALE) for x1,y1,x2,y2 in skeleton]

    polylines = []
    for l in skeleton:
        poly = centerline_to_polyline(l, config.THICKNESS)
        if poly:
            polylines.append(poly)

    # ---- TOPOLOGY ENGINE (Detect Rooms/Plates) ----
    print("[PIPELINE] Detecting rooms...")
    rooms = detect_rooms_from_walls(skeleton)
    print(f"[TOPOLOGY] Found {len(rooms)} rooms.")
    plates = plates_from_rooms(rooms, plate_thickness=config.PLATE_HEIGHT)

    # ---- POST-PROCESS ----
    geometry = geometry_from_polylines(polylines, plates=plates, height=config.HEIGHT, thickness=config.THICKNESS)
    
    # Ensure output dirs
    os.makedirs(os.path.dirname(config.GEOMETRY_JSON_PATH), exist_ok=True)
    save_geometry_json(geometry, config.GEOMETRY_JSON_PATH)

    # Save rooms metadata for debugging
    import json
    rooms_data = [{"id": f"room_{i}", "polygon": room} for i, room in enumerate(rooms)]
    rooms_json_path = os.path.join(os.path.dirname(config.GEOMETRY_JSON_PATH), "rooms.json")
    with open(rooms_json_path, 'w') as f:
        json.dump(rooms_data, f, indent=2)
    print(f"[TOPOLOGY] Saved rooms metadata to: {rooms_json_path}")
    

    # ---- GEOMETRY ENGINE ----
    print("[PIPELINE] Running Geometry Engine...")
    generate_stl(config.GEOMETRY_JSON_PATH, config.MERGED_STL_PATH)

    # ---- BLENDER PIPELINE ----
    print("[PIPELINE] Running Blender...")
    blender_script = os.path.join(config.BASE_DIR, "blender_pipeline", "import_stl.py")
    
    cmd = [
        config.BLENDER_PATH,
        "--background",
        "--factory-startup",
        "--python", blender_script,
        "--", # Separator for script args
        config.MERGED_STL_PATH,
        config.BLENDER_MODEL_PATH
    ]
    
    try:
        subprocess.run(cmd, check=True)
    except FileNotFoundError:
        print(f"[ERROR] Blender not found at: {config.BLENDER_PATH}")
        print("Please update config.py with your Blender path.")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Blender process failed with code {e.returncode}")

    print("[PIPELINE] DONE")

if __name__ == "__main__":
    main()


    
