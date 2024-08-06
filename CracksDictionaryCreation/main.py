# import cv2
# import numpy as np
import os
from track_cracks import track_cracks

if __name__ == "__main__":
    print("Starting...............")


    outputDir = 'Testing'
    image_dir = outputDir + '/images'
    mask_dir = outputDir + '/Reconstructions_Inference'
    new_json = outputDir  # Folder path


    old_json = ""
    old_tracks = {}

    tracked_potholes = {}
    cropped_path = outputDir + "/cropped_images"
    print(cropped_path)
    if not os.path.exists(cropped_path):
        os.mkdir(cropped_path)
    tracked_potholes, old_tracks = track_cracks(image_dir, mask_dir, old_json)
    
    print(type(tracked_potholes))
    print(type(old_tracks))
    
    