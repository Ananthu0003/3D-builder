import cadquery as cq

def export_stl(solids, output_path):
    print("[EXPORT] Merging solids")

    merged = solids[0]
    for s in solids[1:]:
        merged = merged.union(s)

    # 🔥 MOVE GEOMETRY TO ORIGIN
    # bb = merged.val().BoundingBox()
    # cx = (bb.xmin + bb.xmax) / 2
    # cy = (bb.ymin + bb.ymax) / 2
    # cz = (bb.zmin + bb.zmax) / 2

    # merged = merged.translate((-cx, -cy, -cz))

    cq.exporters.export(merged, output_path)
    print("[EXPORT] STL exported and centered")
