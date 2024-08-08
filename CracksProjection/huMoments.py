import cv2

import numpy as np

def compare_hu_moments(contour1, contour2):
    moments1 = cv2.moments(contour1)
    moments2 = cv2.moments(contour2)
    
    hu_moments1 = cv2.HuMoments(moments1).flatten()
    hu_moments2 = cv2.HuMoments(moments2).flatten()

    # Log transform to deal with very small values
    hu_moments1 = -np.sign(hu_moments1) * np.log10(np.abs(hu_moments1))
    hu_moments2 = -np.sign(hu_moments2) * np.log10(np.abs(hu_moments2))

    # Calculate similarity
    diff = np.sum(np.abs(hu_moments1 - hu_moments2))
    return diff
