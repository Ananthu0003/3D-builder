
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
        
        if dx >= dy:
            # horizontal wall
            # Use the average Y of all endpoints to find the centerline
            y_center = sum(ys) / len(ys)
            skeleton.append((min_x, y_center, max_x, y_center))
        else:
            # vertical wall
            # Use the average X of all endpoints to find the centerline
            x_center = sum(xs) / len(xs)
            skeleton.append((x_center, min_y, x_center, max_y))

    return skeleton
