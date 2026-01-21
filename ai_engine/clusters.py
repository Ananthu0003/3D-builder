def cluster_lines(lines, pos_tol=12, gap_tol=40):
    horizontal = []
    vertical = []
    
    for x1, y1, x2, y2 in lines:
        if abs(y2 - y1) <= abs(x2 - x1): # Horizontal
            y_avg = (y1 + y2) / 2
            horizontal.append((min(x1, x2), y_avg, max(x1, x2), y_avg))
        else: # Vertical
            x_avg = (x1 + x2) / 2
            vertical.append((x_avg, min(y1, y2), x_avg, max(y1, y2)))

    clusters = []
    
    # Cluster horizontal
    placed_h = [False] * len(horizontal)
    for i in range(len(horizontal)):
        if placed_h[i]: continue
        c = [horizontal[i]]
        placed_h[i] = True
        
        changed = True
        while changed:
            changed = False
            for j in range(len(horizontal)):
                if placed_h[j]: continue
                h2 = horizontal[j]
                match = False
                for h1 in c:
                    if abs(h1[1] - h2[1]) < pos_tol: # Close Y
                        if not (h2[2] < h1[0] - gap_tol or h2[0] > h1[2] + gap_tol):
                            match = True
                            break
                if match:
                    c.append(h2)
                    placed_h[j] = True
                    changed = True
        clusters.append(c)

    # Cluster vertical
    placed_v = [False] * len(vertical)
    for i in range(len(vertical)):
        if placed_v[i]: continue
        c = [vertical[i]]
        placed_v[i] = True
        
        changed = True
        while changed:
            changed = False
            for j in range(len(vertical)):
                if placed_v[j]: continue
                v2 = vertical[j]
                match = False
                for v1 in c:
                    if abs(v1[0] - v2[0]) < pos_tol: # Close X
                        if not (v2[3] < v1[1] - gap_tol or v2[1] > v1[3] + gap_tol):
                            match = True
                            break
                if match:
                    c.append(v2)
                    placed_v[j] = True
                    changed = True
        clusters.append(c)

    return clusters
