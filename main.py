import os.path

import csv
import json
import time
from CracksDictionaryCreation.trackCracks import track_cracks as track_cracks1
from CracksProjection.init import init
from CracksVisualization.cracksVisualize2 import visualize_potholes



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
    num_images = 17


    ### Start the Cracks Dictionary conataining every cracks either unique or duplication 
    tracked_potholes, old_tracks = track_cracks1(image_dir, mask_dir, old_json)
    
    #### IF you Hva ealready stored the cracks in the a JSON File, you can just load by executing the 
    #### line below and commenting the line above this comment calling the fucntion track_cracks1()
    tracked_potholes = json.load(open(f"{outputDir}/potholestracked.json"))
    
    
    ### Starts the Cracks Filtering 
    init(tracked_potholes,outputDir + "/")
    
    ### Start labelling the resulting unique cracks on the images and masks
    visualize_potholes(image_dir, mask_dir)


    print("Successful...............................")
    