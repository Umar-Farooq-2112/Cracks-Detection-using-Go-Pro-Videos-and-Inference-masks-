import cv2
import numpy as np
from basic_function import *

def detect_cracks(mask):
    mask = filter_color(mask)
    mask = ~mask
    binary_mask = mask.copy()    
    # blurred = cv2.GaussianBlur(mask, (5, 5), 0)
    # _, binary_mask = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY)

    # Apply morphological opening (erosion followed by dilation)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
    # dilated_mask = cv2.dilate(mask, kernel, iterations=2)
    # mask = cv2.erode(dilated_mask, kernel, iterations=2)
    # maskcopy = cv2.resize(mask, (600, 600))
    # cv2.imshow("cleaned mask", maskcopy)
    # cv2.waitKey(0)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Check if contours are found
    if contours:
        return contours
    else:
        return None
