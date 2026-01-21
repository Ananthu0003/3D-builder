def snap_wall_endpoints(lines, snap_dist=10):
    snapped = []
    for x1, y1, x2, y2 in lines:
        for sx1, sy1, sx2, sy2 in lines:
            if abs(x1 - sx1) < snap_dist:
                x1 = sx1
            if abs(y1 - sy1) < snap_dist:
                y1 = sy1
            if abs(x2 - sx2) < snap_dist:
                x2 = sx2
            if abs(y2 - sy2) < snap_dist:
                y2 = sy2
        snapped.append((x1, y1, x2, y2))
    return snapped
