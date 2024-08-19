import cv2
import numpy as np
from CracksDictionaryCreation.basic_function import filter_color
# from basic_function import filter_color
# from basic_function import filter_color

def detect_cracks(image, mask, nFrame):
    mask = filter_color(mask)
    # mask = ~mask
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
    # temp = np.zeros_like(mask)
    # cv2.drawContours(temp,contours,-1,255,2)
    # cv2.imshow("temp",cv2.resize(temp,(800,600)))
    # cv2.waitKey(0)
    
    
    # Check if contours are found
    if contours:
        return contours
    else:
        return None

if __name__ == "__main__":
    
    outputDir = 'Testing'
    image_dir = outputDir + '/images'
    mask_dir = outputDir + '/Reconstructions_Inference'
    
    
    image = cv2.imread(f"{image_dir}/00000015.png")
    mask = cv2.imread(f"{mask_dir}/00000015.png")
    temp = np.zeros(mask.shape[:2])
    
    contours = detect_cracks(image,mask,0)
    if contours is not None:
        for contour in contours:
            bBox = cv2.boundingRect(contour)
            x, y, w, h = bBox
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color, 2 px thickness
            cv2.rectangle(mask, (x, y), (x + w, y + h), (0, 255, 0), 2)  # Green color, 2 px thickness
            # cv2.rectangle(temp, (x, y), (x + w, y + h), (255), 2)  # Green color, 2 px thickness
    cv2.drawContours(temp,contours,-1,255,1)
    cv2.imshow("image",cv2.resize(image,(800,600)))
    cv2.imshow("mask",cv2.resize(mask,(800,600)))
    cv2.imshow("temp",cv2.resize(temp,(800,600)))
    print(len(contours))
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    