import cv2
import numpy as np

def detect_wall_lines(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)

    # Preprocessing
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Use adaptive thresholding to handle lighting variations
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 15, 4
    )

    # Morphological operations to merge wall segments and remove noise
    # Using a 2x2 kernel to be less aggressive, preserving thin internal walls
    kernel = np.ones((2,2), np.uint8)
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Find contours - switched to RETR_CCOMP to handle hierarchy
    # This helps distinguish between outer boundaries and inner holes/walls
    contours, hierarchy = cv2.findContours(closed, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    result = []
    if hierarchy is None: return result
    
    hier = hierarchy[0]
    for i, cnt in enumerate(contours):
        # Filter by area to remove small noise (text, symbols, tiny dimension ticks)
        if cv2.contourArea(cnt) < 100:
            continue
            
        # Approximate contour to simplify it while preserving curves
        epsilon = 0.005 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        
        # Convert polygon segments into line segments
        for j in range(len(approx)):
            p1 = approx[j][0]
            p2 = approx[(j+1)%len(approx)][0]
            
            # Filter out very short segments which are likely part of annotations or noise
            if np.hypot(p2[0] - p1[0], p2[1] - p1[1]) > 25:
                result.append((int(p1[0]), int(p1[1]), int(p2[0]), int(p2[1])))

    return result

def is_solid_line(edge_img, x1, y1, x2, y2, threshold=0.8):
    # Kept for backward compatibility if needed, though replaced by contour logic
    length = np.hypot(x2 - x1, y2 - y1)
    if length == 0: return False
    num_samples = int(length)
    if num_samples < 2: return True
    x_values = np.linspace(x1, x2, num_samples).astype(int)
    y_values = np.linspace(y1, y2, num_samples).astype(int)
    hits = 0
    height, width = edge_img.shape
    for i in range(num_samples):
        px, py = x_values[i], y_values[i]
        if 0 <= px < width and 0 <= py < height:
             patch = edge_img[max(0, py-1):min(height, py+2), max(0, px-1):min(width, px+2)]
             if np.any(patch > 0): hits += 1
    return (hits / num_samples) >= threshold
