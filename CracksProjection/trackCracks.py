import cv2
import numpy as np
import json
from CracksProjection.boundingBox import convert_bbox
import os
from CracksProjection.movingCracks import going_forward,going_forward_only


def track_cracks(images_dir, p = {}, old_potholes = {}, save_json = "", old_json_path = "", cropped_path = ""):
    if old_json_path is None:
        old_json_path = ""
    # file_path = outputDir + "/potholestrackedCompleteImg.json"
    #P = NEW POTHOLESLIST
    savePath, filename = os.path.split(images_dir)
    file_path = savePath + "/potholestracked.json"

    with open(file_path, 'r') as file:
        p = json.load(file)
    # print("type of python dataStructure : ", type(p))
    # print(p.keys())
    keyHead = "Potholes"

    unique_potholes_dic = {}
    frame_list = sorted(os.listdir(images_dir))
    endFrame = len(frame_list) - 1
    endFrame = frame_list[endFrame]
    duplicate_pothole_list = []


    ################################################################

    if len(old_potholes) > 0:

        tracked_potholesOld = old_potholes
        # tracked_potholesOld = tracked_potholesOld["Potholes"]
        # tracked_potholes = p
        # Oh a json exists
        print("prev batch exists")
        box = "bbox"
        forwardList = "forward_list"
        transformedBox = "transformedBox"
        for pFrame in tracked_potholesOld[keyHead].keys():
            print("pFrame: ", pFrame)
            dicData = tracked_potholesOld[keyHead][pFrame]
            bBoxDic = dicData["PotholesData"]
            matrix = np.array(dicData["tran_matrix"])

            # max_detected_count, max_possible_count, current_m
            if bBoxDic is not None:
                for j in range(0, len(bBoxDic)):
                    # print(bBoxDic[j]['transformedBox:'])
                    if transformedBox in bBoxDic[j]:  # Jth boundingBox retrieved
                        print("True")
                        # Means this pothole was counted up due to frame end.
                        print('old potholes continuing')
                        hasPassed = bBoxDic[j]["hasPassed"]
                        if hasPassed is False:
                            bBox_ij = bBoxDic[j][transformedBox]
                            bBox_ij = convert_bbox(bBox_ij)
                            forward_List = bBoxDic[j][forwardList]
                            startFrame = int(pFrame) + len(forward_List)
                            startFrame = f"{startFrame:08}"
                            max_possible_count = bBoxDic[j]["possible_count"]
                            max_detected_count = bBoxDic[j]["detected_count"]
                            duplicate_pothole_list, score, max_possible_count, detected_count, has_passed, forward_nlist = going_forward_only(
                                bBox_ij, startFrame, p, duplicate_pothole_list, startFrame, endFrame, images_dir, max_detected_count, max_possible_count, matrix)
                            for i in forward_nlist:
                                forward_List.append(i)
                            bBoxDic[j]["possible_count"] = max_possible_count
                            bBoxDic[j]["detected_count"] = detected_count
                            bBoxDic[j]["Score"] = score
                            bBoxDic[j]["forward_list"] = forward_List
                            bBoxDic[j]["hasPassed"] = has_passed
        with open(old_json_path, "w") as json_file:
            json.dump(tracked_potholesOld, json_file, indent=2)

    ################################################################


    startFrame = frame_list[0]

    unique_pothole_list = []

    box = "bbox"
    area = "area"
    pothole_num = "pothole_num"
    pothole_n = 0
    # sendFrame = int(sendFrame)
    print(p[keyHead].keys())
    for nFrame in  p[keyHead].keys():

        if nFrame in p[keyHead].keys():
            print(nFrame)
            filename = nFrame + ".png"
            current_i = int(nFrame)
            next_i = current_i + 1                                      # i + 1
            nextFrame = f"{next_i:08}" + ".png"
            # print("current i", current_i)
            dicData = p[keyHead][nFrame]        #Retrieved the FrameID Data
            perspective_matrices_list = []
            perspective_matrix = np.array(dicData["tran_matrix"])   #Got the i to i + 1 matrix out
            print("perspective before going down: ", perspective_matrix)
            perspective_matrices_list.append(perspective_matrix)
            bBoxDic = dicData["PotholesData"]           #List of Potholes with boundingBox out

            if len(bBoxDic) == 0:
                # print("bbox exists")
                perspective_matrix = perspective_matrix.tolist()
                unique_potholes_dic[nFrame] = {"PotholesData": [], "tran_matrix": perspective_matrix}
                print("no-pothole in frame")
                continue
            if len(bBoxDic) > 0:
                print(bBoxDic)
                if "hasPassed" in bBoxDic[0]:
                    perspective_matrix = perspective_matrix.tolist()
                    unique_potholes_dic[nFrame] = {"PotholesData": bBoxDic, "tran_matrix": perspective_matrix}
                    print("This frame is past one")
                    continue
                image1 = cv2.imread(os.path.join(images_dir, filename))
                current_image = image1.copy()
                img_crop = image1.copy()
                tracked_array = []
                count = 1
                for j in range(0, len(bBoxDic)):

                    bBox_ij = bBoxDic[j][box]  # Jth boundingBox retrieved
                    # print(bBoxDic)[j]
                    cntrArea = bBoxDic[j][area]
                    # if cntrArea < 1500:
                    #     continue
                    #####################################
                    x2, y2, w2, h2 = bBox_ij
                    box_bottom = y2 + h2
                    # if box_bottom >= image1.shape[0]:
                    #     continue

                    ###############################
                    savingBox = list(bBox_ij)
                    # print(savingBox[0])
                    pair = (current_i, bBox_ij)
                    if pair not in duplicate_pothole_list:
                        if pair not in unique_pothole_list:

                            x, y, w, h = bBox_ij
                            color = (0, 255, 0)  # Green color
                            thickness = 2
                            cv2.rectangle(image1, (x, y), (x + w, y + h), color, thickness)
                            print(pair)
                            duplicate_pothole_list, score, max_possible_count, detected_count, has_passed, tranformed_box, forward_list, backward_list = going_forward(bBox_ij, current_image, nFrame, p, current_i,
                                                                   duplicate_pothole_list, startFrame, endFrame, images_dir)

                            # if score < 10:
                            #     continue
                            unique_pothole_list.append(pair)
                            if tranformed_box is not None:
                                # perspective_matrix = perspective_matrix.tolist()#["tran_matrix"])  # Got
                                x1y1_tl, y1_tl, x1y1_br, y1_br = tranformed_box[0][0], tranformed_box[0][1], \
                                tranformed_box[0][2], tranformed_box[0][3]
                                x1_tl = int(x1y1_tl[0])
                                y1_tl = int(x1y1_tl[1])
                                x1_br = int(x1y1_br[0])
                                y1_br = int(x1y1_br[1])
                                tranformed_box = (x1_tl, y1_tl, x1_br, y1_br)
                                tranformed_box = list(tranformed_box)
                                print("transformed box: ", tranformed_box)
                                print(type(tranformed_box))
                            # cropped_image = img_crop[y:y + h, x:x + w]
                            save_name = nFrame + "_" + f"{count}" + ".png"
                            # save_cropped = cropped_path + "/" + save_name
                            # print("Crop Path: ", save_cropped)
                            # print(cropped_path)
                            # cv2.imwrite(save_cropped, cropped_image)
                            t = {"pothole_num": count, "bbox": savingBox, "area": cntrArea, "Score": score, "possible_count": max_possible_count, "detected_count": detected_count
                                 , "hasPassed": has_passed, "transformedBox": tranformed_box, "forward_list": forward_list, "backward_list": backward_list, "cropped_img": save_name}
                            count += 1
                            tracked_array.append(t)

                print(nFrame)
                perspective_matrix = perspective_matrix.tolist()
                print("Perspective Matrix: ", perspective_matrix)
                print("type: ", type(perspective_matrix))
                unique_potholes_dic[nFrame] = {"PotholesData": tracked_array, "tran_matrix": perspective_matrix}

    print("ended")
    confirmed_potholes = {"Unique_Potholes": unique_pothole_list, "Duplicate_Potholes": duplicate_pothole_list}
    savePath2, filename = os.path.split(images_dir)
    savePath2 = save_json + "/testing_potholes.json"
    print(savePath2)
    potholes = unique_potholes_dic
    # potholes["Potholes"] = tracked_potholes
    p = {}
    keyHead = "Potholes"
    p[keyHead] = potholes
    print(p)

    with open(savePath2, "w") as json_file:
        json.dump(p, json_file, indent=2)
    print("saved at: ", savePath2)
