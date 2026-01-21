import numpy as np

def filter_axis_aligned(lines, angle_tol=20):
    out = []
    for x1, y1, x2, y2 in lines:
        dx, dy = x2 - x1, y2 - y1
        angle = abs(np.degrees(np.arctan2(dy, dx)))
        if angle < angle_tol or abs(angle - 90) < angle_tol:
            out.append((x1, y1, x2, y2))
    return out


def filter_short_lines(lines, min_length=10):
    out = []
    for x1, y1, x2, y2 in lines:
        if np.hypot(x2 - x1, y2 - y1) >= min_length:
            out.append((x1, y1, x2, y2))
    return out
