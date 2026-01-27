import numpy as np

def build_skeleton(clusters):
    """
    Build one clean centerline per cluster.
    Each cluster is assumed to contain roughly collinear lines.
    """
    skeleton = []

    for cluster in clusters:
        xs, ys = [], []
        for x1, y1, x2, y2 in cluster:
            xs.extend([x1, x2])
            ys.extend([y1, y2])

        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        # Decide orientation based on the span of the cluster
        dx = max_x - min_x
        dy = max_y - min_y
        
        # Calculate overall angle of the cluster
        # Use first and last point of the group to check general direction
        # (This works because diagonal clusters only have one segment right now)
        is_rectilinear = False
        if len(cluster) == 1:
            x1, y1, x2, y2 = cluster[0]
            angle = abs(np.degrees(np.arctan2(y2 - y1, x2 - x1)))
            if angle < 15 or abs(angle - 90) < 15 or abs(angle - 180) < 15:
                is_rectilinear = True
            else:
                # Keep as is
                skeleton.append((x1, y1, x2, y2))
                continue

        if not is_rectilinear and len(cluster) > 1:
            # For complex clusters, default to span-based orientation
            is_rectilinear = True

        if is_rectilinear:
            if dx >= dy:
                # horizontal wall
                y_center = sum(ys) / len(ys)
                skeleton.append((min_x, y_center, max_x, y_center))
            else:
                # vertical wall
                x_center = sum(xs) / len(xs)
                skeleton.append((x_center, min_y, x_center, max_y))

    return skeleton
