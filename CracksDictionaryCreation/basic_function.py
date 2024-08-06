import cv2
import numpy as np


def filter_color(mask, color=(0, 0, 255)):
    lower_bound = np.array([max(0, color[0] - 5), max(0, color[1] - 5), max(0, color[2] - 5)])
    upper_bound = np.array([min(255, color[0] + 5), min(255, color[1] + 5), min(255, color[2] + 5)])

    res = cv2.inRange(mask, lower_bound, upper_bound)
    res = cv2.dilate(res, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5)), iterations=2)

    # cv2.imshow("mask", resize_image(mask))
    # cv2.imshow("res", resize_image(res))
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # print(res.shape)
    
    return res

def apply_mask(image, mask):
    """Apply mask to the image."""

    if len(mask.shape) == 3:
        # print("True")
        mask = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
    # print("image Shape: ", image.shape)
    # print("Mask Shape: ", mask.shape)
    masked_image = cv2.bitwise_and(image, image, mask=mask)
    return masked_image
