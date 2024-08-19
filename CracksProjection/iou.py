import cv2
import numpy as np



def calculate_iou(box1, box2, image1, image2, show=False):

    print("box1: ", box1)
    print("box2: ", box2)
    #x1, y1, w1, h1 = box1

    x2, y2, w2, h2 = box2
    # print("Box1: ", box1)

    # Calculate the coordinates of the bounding boxes
    #x1_tl, y1_tl, x1_br, y1_br = x1, y1, x1 + w1, y1 + h1
    # print("box1 0: ", box1[0])
    # print("box1 01: ", box1[0][3])
    # tL, tR, bR, bL = box1[0][0], box1[0][1], box1[0][2], box1[0][3]

    # x1y1_tl, x1y1_br = box1[0][0], box1[0][2]
    x1y1_tl, y1_tl, x1y1_br, y1_br = box1[0][0], box1[0][1], box1[0][2], box1[0][3]
    x1_tl = int(x1y1_tl[0])
    y1_tl = int(x1y1_tl[1])
    x1_br = int(x1y1_br[0])
    y1_br = int(x1y1_br[1])
    box1 = (x1_tl, y1_tl, x1_br, y1_br)
    print("Box1 Coords: ", box1)
    if y1_tl < 0:
        y1_br = 0


    x2_tl, y2_tl, x2_br, y2_br = x2, y2, x2 + w2, y2 + h2
    # print("Box2 Data: ", box2)
    # print("Box1 Tranformed: ", box1)
    intersection_mask = np.zeros_like(image1.copy())

    # Calculate the coordinates of the intersection rectangle
    x_intersection_tl = max(x1_tl, x2_tl)
    y_intersection_tl = max(y1_tl, y2_tl)
    x_intersection_br = min(x1_br, x2_br)
    y_intersection_br = min(y1_br, y2_br)

    # Calculate the area of intersection rectangle
    intersection_area = max(0, x_intersection_br - x_intersection_tl + 1) * max(0, y_intersection_br - y_intersection_tl + 1)

    # Calculate the area of both bounding boxes
    print("x1_br: ", x1_br, " x1_tl: ", x1_tl)
    print("y1_br: ", y1_br, " y1_tl: ", y1_tl)
    area_box1 = (x1_br - x1_tl + 1) * (y1_br - y1_tl + 1)
    area_box2 = (x2_br - x2_tl + 1) * (y2_br - y2_tl + 1)

    # Calculate the area of the union
    union_area = area_box1 + area_box2 - intersection_area
    if show:
        img1_with_boxes = image1.copy()
        # img2_with_boxes = image2.copy()
        # x1y1_br, y1_br
        cv2.rectangle(img1_with_boxes, (x1_tl, y1_tl), (x1_br, y1_br), (0, 255, 0), 2)
        cv2.rectangle(img1_with_boxes, (x2_tl, y2_tl), (x2_br, y2_br), (255, 0, 0), 2)
        # cv2.rectangle(img1_with_boxes, (box1[0], box1[1]), (box1[0] + box1[2], box1[1] + box1[3]), (123, 255, 123), 2)
        # cv2.rectangle(img2_with_boxes, (box2[0], box2[1]), (box2[0] + box2[2], box2[1] + box2[3]), (255, 0, 0), 2)
        # cv2.polylines(image2, np.int32([box1]), True, (0, 255, 0), 2)
        # cv2.polylines(image2, np.int32([box2]), True, (255, 0, 0), 2)
        cv2.imshow("Image 2 with transformed bounding box", cv2.resize(img1_with_boxes, (600, 600)))
        cv2.waitKey(0)

    # Calculate IoU
    print("Union area: ", union_area)
    print("Area box1: ", area_box1)
    print(area_box2)
    try:
        iou = intersection_area / union_area
    except:
        iou = 0
    # print("IOU", iou * 100)
    # if iou * 100 > 33:
    #     print("IOU IN FUNCTION: ", iou)
    #     img1_with_boxes = image1.copy()
    #     img2_with_boxes = image2.copy()
        # x1y1_br, y1_br
        # cv2.rectangle(img1_with_boxes, (x1_tl, y1_tl), (x1_br, y1_br), (0, 255, 0), 2)
        # cv2.rectangle(img2_with_boxes, (x2_tl, y2_tl), (x2_br, y2_br), (0, 255, 0), 2)
        # cv2.rectangle(img1_with_boxes, (box1[0], box1[1]), (box1[0] + box1[2], box1[1] + box1[3]), (123, 255, 123), 2)
        # cv2.rectangle(img2_with_boxes, (box2[0], box2[1]), (box2[0] + box2[2], box2[1] + box2[3]), (255, 0, 0), 2)

        # intersection_mask = np.zeros_like(img1_with_boxes)
        # intersection_tl = (max(box1[0], box2[0]), max(box1[1], box2[1]))
        # intersection_br = (min(box1[2], box2[2]), min(box1[3], box2[3]))
        # cv2.rectangle(intersection_mask, intersection_tl, intersection_br, (255, 255, 255), -1)
        # mask = cv2.resize(intersection_mask, (600, 600))
        # cv2.imshow("mask", mask)
        # cv2.waitKey(0)
        # cv2.imshow("Image 1", cv2.resize(img1_with_boxes, (600, 600)))
        # cv2.imshow("Image 2", cv2.resize(img2_with_boxes, (600, 600)))
        # cv2.waitKey(0)
        # # return iou, mask
        # return iou
    # else:
        # return iou, None
    return iou

def calculate_iou_backwards(box1, box2, image1, image2):
    # print("box1: ", box1)
    # print("Type", box1.shape)

    x2, y2, w2, h2 = box2
    top_left = (x2, y2)
    top_right = (x2 + w2, y2)
    bottom_right = (x2 + w2, y2 + h2)
    bottom_left = (x2, y2 + h2)
    box2 = np.array([[top_left, top_right, bottom_right, bottom_left]])
    # print("box2Shape: ", box2.shape)
    # Calculate the coordinates of the bounding boxes
    #x1_tl, y1_tl, x1_br, y1_br = x1, y1, x1 + w1, y1 + h1
    # print("box1 0: ", box1[0])
    # print("box1 01: ", box1[0][3])
    x1y1_tl, y1_tl, x1y1_br, y1_br = box1[0][0], box1[0][1], box1[0][2], box1[0][3]
    x1_tl = int(x1y1_tl[0])
    y1_tl = int(x1y1_tl[1])
    x1_br = int(x1y1_br[0])
    y1_br = int(x1y1_br[1])
    box1 = (x1_tl, y1_tl, x1_br, y1_br)

    # x2_tl, y2_tl, x2_br, y2_br = x2, y2, x2 + w2, y2 + h2


    ##############
    xy2_tl, y2_tl, xy2_br, y2_br = box2[0][0], box2[0][1], box2[0][2], box2[0][3]
    x2_tl = int(xy2_tl[0])
    y2_tl = int(xy2_tl[1])
    x2_br = int(xy2_br[0])
    y2_br = int(xy2_br[1])
    box2 = (x2_tl, y2_tl, x2_br, y2_br)
    # print("imgWidth: ", image2.shape[1])
    # print("imgHeight: ", image2.shape[0])
    # print("Bottom Right: ", y1_br)
    if y1_br > image2.shape[0]:
        y1_br = image2.shape[0]
        # x1_br = x2_br
    ##################
    # print("Box2 Data: ", x2_tl, y2_tl, x2_br, y2_br)
    # print("Box1 Data: ", x1_tl, y1_tl, x1_br, y1_br )
    # intersection_mask = np.zeros_like(image1.copy())

    # Calculate the coordinates of the intersection rectangle
    x_intersection_tl = max(x1_tl, x2_tl)
    y_intersection_tl = max(y1_tl, y2_tl)
    x_intersection_br = min(x1_br, x2_br)
    y_intersection_br = min(y1_br, y2_br)

    # Calculate the area of intersection rectangle
    intersection_area = max(0, x_intersection_br - x_intersection_tl + 1) * max(0, y_intersection_br - y_intersection_tl + 1)

    # Calculate the area of both bounding boxes
    area_box1 = (x1_br - x1_tl + 1) * (y1_br - y1_tl + 1)
    area_box2 = (x2_br - x2_tl + 1) * (y2_br - y2_tl + 1)

    # Calculate the area of the union
    union_area = area_box1 + area_box2 - intersection_area

    # Calculate IoU
    try:
        iou = intersection_area / union_area
    except:
        iou = 0
    # print("IO")
    # if iou >= 0:
    #     print("IOU Backwards: ", iou * 100)
        # img1_with_boxes = image1.copy()
        # img2_with_boxes = image2.copy()
        #
        # cv2.rectangle(img1_with_boxes, (x1_tl, y1_tl), (x1_br, y1_br), (0, 255, 0), 2)
        # cv2.rectangle(img2_with_boxes, (x2_tl, y2_tl), (x2_br, y2_br), (0, 0, 255), 2)
        # # cv2.rectangle(img1_with_boxes, (box1[0], box1[1]), (box1[0] + box1[2], box1[1] + box1[3]), (123, 255, 123), 2)
        # # cv2.rectangle(img2_with_boxes, (box2[0], box2[1]), (box2[0] + box2[2], box2[1] + box2[3]), (255, 0, 0), 2)
        #
        # intersection_mask = np.zeros_like(img1_with_boxes)
        # intersection_tl = (max(box1[0], box2[0]), max(box1[1], box2[1]))
        # intersection_br = (min(box1[2], box2[2]), min(box1[3], box2[3]))
        # cv2.rectangle(intersection_mask, intersection_tl, intersection_br, (255, 255, 255), -1)
        # mask = cv2.resize(intersection_mask, (600, 600))
        # cv2.imshow("mask", mask)
        # # cv2.waitKey(0)
        # cv2.imshow("Image 1_IOU", cv2.resize(img1_with_boxes, (600, 600)))
        # cv2.imshow("Image 2_IOU", cv2.resize(img2_with_boxes, (600, 600)))
        # cv2.waitKey(0)
        # return iou, mask
    #     return iou
    # else:
        # return iou, None
    return iou
