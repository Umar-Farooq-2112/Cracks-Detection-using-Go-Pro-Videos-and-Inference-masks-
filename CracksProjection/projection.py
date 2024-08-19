import numpy as np
import cv2

from CracksProjection.boundingBox import is_bbox_inside_image_backward,is_bbox_inside_image


def forward_projection(bbox, perspective_matrices, image2, isBackward=False):

    x, y, w, h = bbox
    # print("Bbox before converting to array: ", bbox, type(bbox))
    bbox = np.array([[(x, y), (x + w, y), (x + w, y + h), (x, y + h)]], dtype=np.float32)
    # bbox = bbox.transpose((1, 0, 2))
    transformed_bbox = bbox
    # print("Box before forward projection", bbox)
    # print("Shape: ", bbox.shape)
    if isBackward:
        perspective_matrices = [np.linalg.inv(matrix) for matrix in perspective_matrices]

    # Project the bounding box to image 2
    # print("Length of matrices", len(perspective_matrices))
    for matrix in perspective_matrices:
        # print("mat")
        matrix = np.array(matrix)
        transformed_bbox = cv2.perspectiveTransform(transformed_bbox, matrix)
        # print("Transformed bBox", transformed_bbox)
        # print("Its Shape: ", transformed_bbox.shape)
    # Load image 2
    # Draw the transformed bounding box on image 2
    # cv2.polylines(image2, np.int32([transformed_bbox]), True, (0, 255, 0), 2)
    # Visualize the result
    # image2 = cv2.resize(image2, (600,600))
    image_size = (1920, 1080)
    is_Inside = is_bbox_inside_image(transformed_bbox, image_size)
    # cv2.imshow("Image 2 with transformed bounding box", image2)
    # cv2.waitKey(0)
    if isBackward:
        print("transformed box: ", transformed_bbox)
        is_Inside = is_bbox_inside_image_backward(transformed_bbox, image_size)
        print("this transformed box is Inside Ans: ",is_Inside)
        # cv2.imshow("Image 2 with transformed bounding box", image2)
        # cv2.waitKey(0)
    # print("Transformed Bounding Box Coords: ", transformed_bbox)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return is_Inside, transformed_bbox
