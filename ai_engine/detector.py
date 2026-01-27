import cv2
import numpy as np

def detect_wall_lines(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150)

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi / 180,
        threshold=120,
        minLineLength=40,
        maxLineGap=10
    )

    result = []
    if lines is not None:
        for l in lines:
            x1, y1, x2, y2 = l[0]
            if is_solid_line(edges, x1, y1, x2, y2):
                result.append((x1, y1, x2, y2))

    return result

def is_solid_line(edge_img, x1, y1, x2, y2, threshold=0.8):
    """
    Checks if a line segment is 'solid' enough in the edge image.
    Dotted lines will have a lower ratio of edge pixels.
    """
    length = np.hypot(x2 - x1, y2 - y1)
    if length == 0:
        return False

    # Sample points along the line
    num_samples = int(length)
    if num_samples < 2:
        return True
        
    x_values = np.linspace(x1, x2, num_samples).astype(int)
    y_values = np.linspace(y1, y2, num_samples).astype(int)
    
    # Check pixel values at these coordinates in the edge image
    # We use a small kernel/margin because the line might be slightly offset
    hits = 0
    height, width = edge_img.shape
    
    for i in range(num_samples):
        px, py = x_values[i], y_values[i]
        
        # Check 3x3 neighborhood for any edge pixel
        if 0 <= px < width and 0 <= py < height:
             # simple check: is there any edge pixel nearby?
             patch = edge_img[max(0, py-1):min(height, py+2), max(0, px-1):min(width, px+2)]
             if np.any(patch > 0):
                 hits += 1

    ratio = hits / num_samples
    return ratio >= threshold
