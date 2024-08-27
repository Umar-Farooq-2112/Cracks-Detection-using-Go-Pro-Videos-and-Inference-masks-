import os.path

import csv
import json
import time
from CracksProjection.init import init
from CracksDictionaryCreation.trackCracks import track_cracks as track_cracks1
# from CracksProjection.init import track_cracks as track_cracks2 
from CracksProjection.trackCracks import track_cracks as track_cracks2 
from CracksVisualization.cracksVisualize2 import visualize_potholes

def CracksDetection(image_dir,mask_dir,output_dir,old_json=""):
    new_json = outputDir  
    old_tracks = {}
    tracked_potholes = {}
    cropped_path = outputDir + "/cropped_images"
    print(cropped_path)
    if not os.path.exists(cropped_path):
        os.mkdir(cropped_path)
    print("Starting.................................")
    tracked_potholes, old_tracks = track_cracks1(image_dir, mask_dir, old_json)
    tracked_potholes = track_cracks2(image_dir, tracked_potholes, old_tracks, new_json, old_json, cropped_path)
    visualize_potholes(image_dir, mask_dir)
    print("Successful...............................")



if __name__ == '__main__':
    outputDir = 'Testing'
    # outputDir = 'testing/2ndBatchNewInf'
    image_dir = outputDir + '/images'
    mask_dir = outputDir + '/Reconstructions_Inference'
    new_json = outputDir  # Folder path
    old_json = ""
    old_tracks = {}
    tracked_potholes = {}
    cropped_path = outputDir + "/cropped_images"
    # print(cropped_path)
    # if not os.path.exists(cropped_path):
    #     os.mkdir(cropped_path)
    # if not os.path.exists(f"{outputDir}/ResultsAnalysis"):
    #     os.mkdir(f"{outputDir}/ResultsAnalysis")
    if not os.path.exists(f"{outputDir}/TestingResults"):
        os.mkdir(f"{outputDir}/TestingResults")
    if not os.path.exists(f"{outputDir}/TestingResults/Images"):
        os.mkdir(f"{outputDir}/TestingResults/Images")
    if not os.path.exists(f"{outputDir}/TestingResults/Masks"):
        os.mkdir(f"{outputDir}/TestingResults/Masks")
    if not os.path.exists(f"{outputDir}/TestingResults/Filled"):
        os.mkdir(f"{outputDir}/TestingResults/Filled")
    if not os.path.exists(f"{outputDir}/Output"):
        os.mkdir(f"{outputDir}/Output")

    row1 = None
    row2 = None
    row3 = None
    num_images = 65


    start_time = time.time()    
    tracked_potholes, old_tracks = track_cracks1(image_dir, mask_dir, old_json)
    end_time = time.time()
    row1 = ['A',str(num_images),str(int(end_time-start_time))]
    
    # tracked_potholes = json.load(open("Testing/potholestracked.json"))
    
    start_time = time.time()
    init(tracked_potholes,"Testing/")
    end_time = time.time()
    row2 = ['B',str(num_images),str(int(end_time-start_time))]
    
    # start_time = time.time()
    # tracked_potholes = track_cracks2(image_dir, tracked_potholes, old_tracks, new_json, old_json, cropped_path)
    # end_time = time.time()
    # row2 = ['B',str(num_images),str(int(end_time-start_time))]
    
    start_time = time.time()    
    visualize_potholes(image_dir, mask_dir)
    end_time = time.time()
    row3 = ['C',str(num_images),str(int(end_time-start_time))]



    with open('records.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        for i in [row1,row2,row3]:
            if i is not None:
                writer.writerow(i)

    print("Successful...............................")
    