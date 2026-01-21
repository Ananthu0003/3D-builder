def normalize_lines(lines):
    norm = []
    for x1, y1, x2, y2 in lines:
        if (x2, y2) < (x1, y1):
            norm.append((x2, y2, x1, y1))
        else:
            norm.append((x1, y1, x2, y2))
    return norm
