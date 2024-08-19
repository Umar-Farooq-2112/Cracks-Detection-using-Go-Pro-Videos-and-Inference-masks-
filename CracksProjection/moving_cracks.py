import cv2
import numpy as np
import os
from CracksProjection.projection import forward_projection
from CracksProjection.iou import calculate_iou,calculate_iou_backwards


keyHead = "Potholes"
box = "bbox"


def going_forward_only(bbox_ij,  nFrame, p, duplicate_list_original, startFrame, endFrame, images_dir, max_detected_count, max_possible_count, current_m):
    duplicate_list = []
    hasPassed = False
    keyHead = "Potholes"
    transformed_box = []
    forward_list = []
    # print("Starting forward projection.............")
    # print("bbox ij: ", bbox_ij)
    # detected_count = 0
    frameData = p[keyHead][nFrame]
    n = int(endFrame[:-4])
    # print("Length of directory: ", len(images_dir))

    # print(os.listdir(images_dir))
    matrices = []
    matrices.append(current_m)
    # print("Forward Projection Started")
    k = int(startFrame)
    while k < n:    #Forward Projection
        next_i = k + 1
        nextFrame = f"{next_i:08}" + ".png"
        # print(images_dir + '/' + nextFrame)
        img2 = cv2.imread(os.path.join(images_dir, nextFrame))
        nextFrame = nextFrame[:-4]
        image2 = img2.copy()
        is_inside, transformed_bbox = forward_projection(bbox_ij, matrices, image2)
        transformed_box = transformed_bbox
        if not is_inside:
            print("Not Inside")
            hasPassed = True
            transformed_box = None
            # print("Not Inside anymore")
            break
        else:
            max_possible_count += 1
            # print("Going to check")
            k += 1
            # print("nextFrame: ", nextFrame)
            if nextFrame in p[keyHead].keys():
                # print("TRUE")
                nextFrameData = p[keyHead][nextFrame]
                cntrBoxes = nextFrameData["PotholesData"]
                if cntrBoxes is not None:
                    max_adder = False
                    for b in range(0, len(cntrBoxes)):
                        current_box = cntrBoxes[b][box] #xywh
                        print("Comparing with: ", nextFrame, " ", current_box)
                        # print(int(nextFrame))

                        iou = calculate_iou(transformed_bbox, current_box, image2, image2)

                        if iou * 100 >= 33:
                            print("IOU: ", iou * 100)
                            # max_detected_count += 1
                            duplicate_pair = (next_i, current_box)
                            duplicate_list.append(duplicate_pair)
                            max_adder = True
                    if max_adder == True:
                        max_detected_count += 1
                        forward_list.append(1)
                    else:

                        forward_list.append(0)
                else:
                    forward_list.append(0)
            else:
                forward_list.append(0)


                next_m = np.array(nextFrameData["tran_matrix"])
                matrices.append(next_m)
                ####

    matrices = []
    current_m = np.array(frameData["tran_matrix"])
    matrices.append(current_m)

    print("Max Updated detected count: ", max_detected_count)
    print("Max Updated possible count: ", max_possible_count)
    # print("my List: ", final_list)
    score = max_detected_count / max_possible_count
    # print("Score is: ", score)
    print("Score: ", score * 100)
    score = score * 100
    if score > 0:
        for duplicate in duplicate_list:
            duplicate_list_original.append(duplicate)

    return duplicate_list_original, score, max_possible_count, max_detected_count, hasPassed,  forward_list

def going_forward(bbox_ij, img, nFrame, p,  i, duplicate_list_original, startFrame, endFrame, images_dir):
    duplicate_list = []
    max_detected_count = 1
    max_possible_count = 1
    hasPassed = False
    final_list = []
    transformed_box = []
    forward_list = []
    backward_list = []
    final_list.append(nFrame)
    adder = 0
    print("Starting forward projection............." , nFrame)
    # print("bbox ij: ", bbox_ij)
    image1 = img.copy()
    # detected_count = 0
    frameData = p[keyHead][nFrame]
    n = int(endFrame[:-4])
    # print("Length of directory: ", len(images_dir))

    # print(os.listdir(images_dir))
    matrices = []
    current_m = np.array(frameData["tran_matrix"])
    matrices.append(current_m)
    # print("Forward Projection Started")
    k = i
    while k < n:    #Forward Projection
        next_i = k + 1
        nextFrame = f"{next_i:08}" + ".png"
        # print(images_dir + '/' + nextFrame)
        img2 = cv2.imread(os.path.join(images_dir, nextFrame))
        prevImg = img2.copy()
        nextFrame = nextFrame[:-4]
        image2 = img2.copy()
        height, width = image1.shape[:2]
        is_inside, transformed_bbox = forward_projection(bbox_ij, matrices, image2)
        print("is Inside: ", is_inside)
        transformed_box = list(transformed_bbox)
        #transformed_box: tl, tr, bl, br
        if not is_inside:
            hasPassed = True
            transformed_box = None

            # print("Not Inside anymore")
            break
        else:
            max_possible_count += 1
            # print("Going to check")
            k += 1
            # print("nextFrame: ", nextFrame)
            if nextFrame in p[keyHead].keys():
                # print("TRUE")
                nextFrameData = p[keyHead][nextFrame]
                cntrBoxes = nextFrameData["PotholesData"]
                if cntrBoxes is not None:
                    max_adder = False
                    for b in range(0, len(cntrBoxes)):
                        current_box = cntrBoxes[b][box] #xywh
                        print("Comparing with: ", nextFrame, " ", current_box)

                        if int(nextFrame) == 415 and current_box == [1046, 308, 23, 19]:
                            iou = calculate_iou(transformed_bbox, current_box, image2, image2)
                        else:
                            iou = calculate_iou(transformed_bbox, current_box, image2, image2)
                        print("IOU : ", iou)
                        # print("Box1: ", bbox_ij)
                        # print("Box2: ", current_box)
                        if iou * 100 > 33:
                            print("IOU: ", iou * 100)
                            # max_detected_count += 1
                            duplicate_pair = (next_i, current_box)
                            duplicate_list.append(duplicate_pair)
                            max_adder = True
                    if max_adder == True:
                        max_detected_count += 1
                        final_list.append(1)
                        forward_list.append(1)
                    else:

                        final_list.append(0)
                        forward_list.append(0)
                else:
                    forward_list.append(0)
                    final_list.append(0)

                next_m = np.array(nextFrameData["tran_matrix"])
                matrices.append(next_m)
                ####
            else:
                forward_list.append(0)

    matrices = []
    current_m = np.array(frameData["tran_matrix"])
    matrices.append(current_m)
    k = i
    startFrame = int(startFrame[:-4])
    # print("StartFrame: ", startFrame)
    print("Going backward Projection..................", nFrame)
    while k >= startFrame + 1: #Backward Projection
        prev_i = k - 1
        prevFrame = f"{prev_i:08}" + ".png"
        print("prevFrame: ", prevFrame)
        img2 = cv2.imread(os.path.join(images_dir, prevFrame))
        prevImg = img2.copy()
        prevFrame = prevFrame[:-4]
        image2 = img2.copy()
        height, width = image1.shape[:2]
        is_inside, transformed_bbox = forward_projection(bbox_ij, matrices, image2, True)
        # transformed_box: tl, tr, bl, br
        if not is_inside:
            # print("Not Inside anymore")
            break
        else:
            k -= 1
            max_possible_count += 1
            if prevFrame in p[keyHead].keys():
                # print("TRUE")
                prevFrameData = p[keyHead][prevFrame]
                cntrBoxes = prevFrameData["PotholesData"]

                if cntrBoxes is not None:
                    max_adder = False
                    for b in range(0, len(cntrBoxes)):
                        current_box = cntrBoxes[b][box]  # xywh
                        print("current_box: ", current_box)
                        iou = calculate_iou_backwards(transformed_bbox, current_box, image2, image2)
                        print("Iou: ", iou)
                        if iou * 100 > 33:
                            # print("IOU: ", iou * 100)
                            # max_detected_count += 1
                            duplicate_pair = (prev_i, current_box)
                            if duplicate_pair not in duplicate_list_original:
                                duplicate_list.append(duplicate_pair)
                                max_adder = True
                    if max_adder == True:
                        max_detected_count += 1
                        final_list.insert(0, 1)
                        backward_list.append(1)
                    else:
                        backward_list.append(0)
                        final_list.insert(0, 0)
                else:
                    final_list.insert(0,0)
                    backward_list.append(0)


                prev_m = np.array(prevFrameData["tran_matrix"])
                matrices.append(prev_m)


    # print("Backward projection Ended")
    print("Max detected count: ", max_detected_count)
    print("Max possible count: ", max_possible_count)
    print("my List: ", final_list)
    score = max_detected_count / max_possible_count
    # print("Score is: ", score)
    print("Score: ", score * 100)
    score = score * 100
    if score > 0:
        for duplicate in duplicate_list:
            duplicate_list_original.append(duplicate)

    return duplicate_list_original, score, max_possible_count, max_detected_count, hasPassed, transformed_box, forward_list, backward_list
