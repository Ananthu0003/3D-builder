# geometry_engine/builder.py

import cadquery as cq


def build_wall(element):
    pts = element["geometry_2d"]   
    height = element["height"]
    wp = cq.Workplane("XY")
    wp = wp.polyline(pts).close().extrude(height)

    return wp


def build_all_elements(elements):
    solids = []

    for elem in elements:
        if elem["primitive_type"] == "wall":
            solid = build_wall(elem)
            solids.append(solid)

    return solids
