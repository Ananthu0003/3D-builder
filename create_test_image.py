import cv2
import numpy as np
import os

def create_test_blueprint(path):
    img = np.zeros((600, 800, 3), dtype=np.uint8)
    cv2.rectangle(img, (100, 100), (700, 500), (255, 255, 255), 10)
    cv2.line(img, (300, 100), (300, 500), (255, 255, 255), 10)
    cv2.line(img, (500, 100), (500, 500), (255, 255, 255), 10)
    cv2.line(img, (100, 300), (700, 300), (255, 255, 255), 10)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cv2.imwrite(path, img)
    print(f"Created test blueprint at: {path}")

if __name__ == "__main__":
    create_test_blueprint("uploads/blueprints/bluprnt.png")
