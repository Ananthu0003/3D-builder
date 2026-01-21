def geometry_from_polylines(polylines, plates=None, height=5.0, thickness=0.5):
    elements = []

    # WALLS
    for i, poly in enumerate(polylines):
        elements.append({
            "id": f"wall_{i}",
            "primitive_type": "wall",
            "geometry_2d": poly,   
            "height": height,
            "thickness": thickness
        })

    # PLATES (optional)
    if plates:
        elements.extend(plates)

    return {
        "elements": elements
    }

def plates_from_rooms(rooms, plate_thickness=0.1):
    plates = []
    for i, room_poly in enumerate(rooms):
        plates.append({
            "id": f"plate_{i}",
            "primitive_type": "plate",
            "geometry_2d": room_poly,
            "height": plate_thickness,
            "thickness": 0 # Not used for plates
        })
    return plates

def save_geometry_json(geometry, filepath):
    import json
    with open(filepath, "w") as f:
        json.dump(geometry, f, indent=2)
        