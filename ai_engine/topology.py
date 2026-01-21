def split_lines_at_intersections(lines, tol=1.0):
    """
    Splits a set of horizontal and vertical lines at their intersection points.
    """
    horiz = []
    vert = []
    for x1, y1, x2, y2 in lines:
        if abs(y1 - y2) < abs(x1 - x2):
            horiz.append({'x': sorted([x1, x2]), 'y': (y1 + y2) / 2})
        else:
            vert.append({'y': sorted([y1, y2]), 'x': (x1 + x2) / 2})

    new_lines = []
    
    # Split horizontal lines by vertical lines
    for h in horiz:
        splits = [h['x'][0], h['x'][1]]
        for v in vert:
            if h['x'][0] < v['x'] < h['x'][1] and v['y'][0] <= h['y'] <= v['y'][1]:
                splits.append(v['x'])
        splits.sort()
        for i in range(len(splits) - 1):
            if splits[i+1] - splits[i] > tol:
                new_lines.append((splits[i], h['y'], splits[i+1], h['y']))

    # Split vertical lines by horizontal lines
    for v in vert:
        splits = [v['y'][0], v['y'][1]]
        for h in horiz:
            if v['y'][0] < h['y'] < v['y'][1] and h['x'][0] <= v['x'] <= h['x'][1]:
                splits.append(h['y'])
        splits.sort()
        for i in range(len(splits) - 1):
            if splits[i+1] - splits[i] > tol:
                new_lines.append((v['x'], splits[i], v['x'], splits[i+1]))

    return new_lines


def remove_isolated_segments(lines, min_len=5):
    out = []
    for x1, y1, x2, y2 in lines:
        if abs(x2 - x1) + abs(y2 - y1) > min_len:
            out.append((x1, y1, x2, y2))
    return out

def detect_rooms_from_walls(walls):
    """
    Detect rooms (polygons) from a list of wall segments.
    """
    import networkx as nx
    import math

    # 1. Build a graph with snapped nodes
    G = nx.Graph()
    nodes = []
    
    def get_snapped_node(p, tol=1.0):
        for node in nodes:
            if math.hypot(p[0]-node[0], p[1]-node[1]) < tol:
                return node
        nodes.append(p)
        return p

    for wall in walls:
        x1, y1, x2, y2 = wall
        p1 = get_snapped_node((float(x1), float(y1)))
        p2 = get_snapped_node((float(x2), float(y2)))
        if p1 != p2:
            G.add_edge(p1, p2)

    try:
        cycles = nx.minimum_cycle_basis(G)
    except Exception:
        cycles = []
    
    rooms = []
    for cycle_nodes in cycles:
        rooms.append(cycle_nodes)

    return rooms
