def split_lines_at_intersections(lines):
    return lines  


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

    # 1. Build a graph where nodes are endpoints and edges are walls
    G = nx.Graph()
    for wall in walls:
        x1, y1, x2, y2 = wall
        G.add_edge((x1, y1), (x2, y2))

    # 2. Find cycles (these are the room boundaries)
    # 2. Find cycles (these are the room boundaries)
    # Use minimum_cycle_basis to find the faces (rooms)
    # This returns a list of cycles, where each cycle is a list of nodes.
    try:
        cycles = nx.minimum_cycle_basis(G)
    except Exception:
        cycles = []
    
    rooms = []
    for cycle_nodes in cycles:
        rooms.append(cycle_nodes)

    return rooms
