import cadquery as cq

def export_stl(solids_dict, output_path):
    print("[EXPORT] Merging solids")
    solids = list(solids_dict.values())
    if not solids:
        return

    merged = solids[0]
    for s in solids[1:]:
        merged = merged.union(s)

    cq.exporters.export(merged, output_path)
    print(f"[EXPORT] Merged STL exported to {output_path}")

def export_individual_stls(solids_dict, output_dir):
    print(f"[EXPORT] Saving {len(solids_dict)} individual parts to {output_dir}")
    os.makedirs(output_dir, exist_ok=True)

    for elem_id, solid in solids_dict.items():
        part_path = os.path.join(output_dir, f"{elem_id}.stl")
        cq.exporters.export(solid, part_path)
    
    print("[EXPORT] Individual STLs exported")

import os
