import json
import os

import cv2
import json


keyHead = "Potholes"
box = "bbox"
Unique_Potholes = "Unique_Potholes"

def visualize_potholes(images_dir, masks_dir):
    # file_path = outputDir + '/testing_potholesComplete.json'
    savePath, filename = os.path.split(images_dir)
    file_path = savePath + '/ProcessedCracks.json'
    print(file_path)
    score_list = []
    with open(file_path, 'r') as file:
        p = json.load(file)

    iterator = 0

    for frame_id, frame_data in p["Potholes"].items():
        # print(frame_id)
        iterator += 1
        nFrame = frame_id + ".png"
        img = cv2.imread((os.path.join(images_dir, nFrame)))
        mask = cv2.imread((os.path.join(masks_dir, nFrame)))
        temp_img = img.copy()
        
        save = False
        for pothole_data in frame_data["PotholesData"]:
            save = False
            print("Frame: ", frame_id, " Pothole Number:", pothole_data["pothole_num"])
            bbox = pothole_data["bbox"]
            pothole_num = pothole_data["pothole_num"]

            if True:
                area  = pothole_data["area"]
                save = True
                print("Pothole Data:")
                print("  Pothole Number:", pothole_data["pothole_num"])
                print("  Bounding Box:", pothole_data["bbox"])
                print("  Detected Area:", pothole_data["area"])
                x, y, w, h = bbox
                color = (0, 0, 255)  # Red color
                thickness = 3
                imgToSave = img.copy()
                cv2.rectangle(imgToSave, (x, y), (x + w, y + h), color, thickness)
                cv2.rectangle(temp_img, (x, y), (x + w, y + h), color, thickness)
                cv2.rectangle(mask, (x, y), (x + w, y + h), (255,0,0), thickness)
                if save:
                    print("Save TRUE")
                    savePath, filename = os.path.split(images_dir)
                    save_img = savePath + '/TestingResults'
                    print(save_img)
                    if not os.path.exists(save_img):
                        print("mkdir exec")
                        os.mkdir(save_img)
                    # print(nFrame)
                    # save_img = save_img + '/' + frame_id + '_'  + f"{pothole_num}.png"
                    # print("Saving: ", save_img)
                    # cv2.imwrite(save_img, temp_img)
                    # cv2.imwrite(save_img + '/' + frame_id + '_'  + f"{pothole_num}.png", mask)

            savePath, filename = os.path.split(images_dir)
            save_img = savePath + '/TestingResults'
            if not os.path.exists(save_img):
                os.mkdir(save_img)
            # save_img = save_img + '/' + frame_id + '_cracks.png'
            # print("Saving: ", save_img)
            cv2.imwrite(save_img + '/Images/' + frame_id + '_image.png', temp_img)
            cv2.imwrite(save_img + '/Masks/' + frame_id + '_mask.png', mask)
            
            
            
    # average = sum(score_list) / len(score_list)

    # Calculate min and max
    # minimum = min(score_list)
    # maximum = max(score_list)

    # print("Average:", average)
    # print("Minimum:", minimum)
    # print("Maximum:", maximum)

    return None
#
#
# if __name__ == '__main__':
#     outputDir = 'testing/Reconstructions_GH040388'
#
#     images_dir = outputDir + '/images'
#     masks_dir = outputDir + '/Reconstructions_Inference'
#
#     start_time = time.time()  # Record the start time
#     # images_dir = outputDir + '/images'
#     # masks_dir = outputDir + '/Reconstructions_Inference'
#     log_path = outputDir + '/log.txt'
#     # sys.stdout = open(log_path, 'w')
#     tracked_potholes = visualize_potholes(images_dir, masks_dir)
#     end_time = time.time()  # Record the end time
#
#     execution_time = end_time - start_time
#     print("Execution time:", execution_time, "seconds")
#     # sys.stdout.close()
