def apply_boolean_operations(solids, elements):
    for elem in elements:
        ops = elem.get("operations", [])
        source_id = elem["id"]

        for op in ops:
            target_id = op["target_id"]
            op_type = op["type"]

            if op_type == "cut":
                solids[target_id] = solids[target_id].cut(solids[source_id])

            elif op_type == "union":
                solids[target_id] = solids[target_id].union(solids[source_id])

    return solids
