import json
import cv2
import numpy as np
import os
# from CracksDictionaryCreation.perspectiveMatrixTransform import find_features
from CracksDictionaryCreation.cracks_detection import detect_cracks
from CracksDictionaryCreation.HomographyCalculation import getSIFTkeypoints


def track_cracks(images_dir, masks_dir,  load_json):
    if load_json is None:
        load_json = ""
    tracked_potholes = {}
    tracked_potholes_old = {}
    # iteration = 0
    final_length = sorted(os.listdir(images_dir))
    final_length = final_length[len(final_length) - 2]
    print(final_length)
    final_length = int(final_length[:-4])
    stored_matrices = []
    # savePath, filename = os.path.split(images_dir)
    save_json = load_json #+ "/testing_potholes.json"
    # print
    if os.path.exists(save_json):
        # Oh a json exists
        print("prev batch exists")
        # print(save_json)
        with open(save_json, "r") as file:
            tracked_potholes_old = json.load(file)
            # tracked_potholes_old["Potholes"] = tracked_potholes_old
            # print(save_json)
        print(tracked_potholes_old["Potholes"].keys())

#Step 1: Put all Frames and Masks and get boundingboxes
    for filename in sorted(os.listdir(images_dir)):
        nFrame = filename[:-4]  # Basically the Duplicate Frame (prev batch last frame)
        if len(tracked_potholes_old) > 0:

            if nFrame in tracked_potholes_old["Potholes"].keys():
                # print("true")
                continue
        print("nFrame: ", nFrame)
        tracked_array = []
        image = cv2.imread(os.path.join(images_dir, filename))
        mask = cv2.imread(os.path.join(masks_dir, filename))
        nextFrame = int(nFrame) + 1
        save_json, filenames = os.path.split(images_dir)
        save_json = save_json + "/testing_potholes.json"
        filename2 = f"{nextFrame:08}" + ".png"
        print("filename2: ", filename2)
        imgcopy = image.copy()
        print(masks_dir , filename)
        potholeMask = cv2.imread(os.path.join(masks_dir, filename))
        potholeMask = cv2.resize(potholeMask, (1920, 1080))
        temp_image = image.copy()
        temp_mask = mask.copy()

        contours = detect_cracks(image, potholeMask, f"{masks_dir}/output/{filename}")

        if contours:
            count = 1
            tracked_array = []
            for contour in contours:
                bBox = cv2.boundingRect(contour) #+ '_' + nFrame
                x, y, w, h = bBox
                bBox = str(bBox) #+ '_' + nFrame
                bBox = tuple(map(int, bBox.strip("()").split(", ")))
                bBox = list(bBox)
                area = cv2.contourArea(contour)
                t = {"pothole_num": count, "bbox": bBox, "area": area}
                tracked_array.append(t)
                # tracked_array.append(tracked_p)
                cv2.rectangle(temp_image, (x, y), (x + w, y + h), (0, 0, 0), 2)  # Green color, 2 px thickness
                cv2.rectangle(temp_mask, (x, y), (x + w, y + h), (0, 0, 0), 2)  # Green color, 2 px thickness

                count += 1
                
        iteration = int(nFrame)

        cv2.imwrite(f"Testing/Output/{nFrame}_image.png",temp_image)
        cv2.imwrite(f"Testing/Output/{nFrame}_mask.png",temp_mask)

        if iteration <= final_length:
            image2 = cv2.imread(os.path.join(images_dir, filename2))
            # current_to_next_perspective = find_features(image_0=imgcopy, image_1=image2)
            current_to_next_perspective = getSIFTkeypoints(imgcopy, image2)
            print(current_to_next_perspective)
            stored_matrices.append(current_to_next_perspective)

                # t = {"next_tran": current_to_next_perspective}
                # tracked_array.append(t)
            matrix = current_to_next_perspective.tolist()
            tracked_potholes[nFrame] = {"PotholesData": tracked_array, "tran_matrix": matrix}

#Step1.b: Get the dataStructure with imageName, pothole1,2,3,4 and its bounding-boxes
        if iteration == final_length:
            print("Yes going to save json")
            matrix_array = np.array(stored_matrices)
            # np.save(outputDir + '/transform_matrices.npy', matrix_array)

            potholes = tracked_potholes
            # potholes["Potholes"] = tracked_potholes
            p = {}
            keyHead = "Potholes"
            p[keyHead] = potholes
            # Path to save the JSON file
            savePath, filename = os.path.split(images_dir)
            file_path = savePath + "/potholestracked.json"
            #
            # # Write filtered dictionary to JSON file
            with open(file_path, "w") as json_file:
                json.dump(p, json_file, indent=2)
            # print("saved at: ", file_path)

            return p, tracked_potholes_old
