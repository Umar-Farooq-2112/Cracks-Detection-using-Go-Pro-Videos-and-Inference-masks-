import os.path
import time

import numpy as np
import json

from CracksDictionaryCreation.track_cracks import track_cracks as track_cracks1
from CracksProjection.track_cracks import track_cracks as track_cracks2
from CracksVisualization import cracksVisualize

if __name__ == '__main__':
    # batchesList = ['testing/projecttest2', '2ndBatchNewInf']
    # for outputDir in batchesList:

    # outputDir = 'testing/1stBatch'
    # # outputDir = 'testing/2ndBatchNewInf'
    # image_dir = outputDir + '/images'
    # mask_dir = outputDir + '/Reconstructions_Inference'
    # new_json = outputDir #Folder path
    # start_time = time.time()  # Record the start time
    # old_json = ""
    # cropped_path = outputDir + "/cropped_images"
    # tracked_potholes, old_tracks = PotholesDictionaryCreation.track_potholes(image_dir, mask_dir, old_json)
    # tracked_potholes = potholesProjection.track_potholes2(image_dir, tracked_potholes, old_tracks, new_json, old_json,
    #                                                       cropped_path)

    # outputDir = 'F:/GH040392/Reconstructions'
    outputDir = 'testing/smallarea'
    # outputDir = 'testing/2ndBatchNewInf'
    image_dir = outputDir + '/images'
    mask_dir = outputDir + '/Reconstructions_Inference'
    new_json = outputDir  # Folder path
    start_time = time.time()  # Record the start time
    # old_json = 'testing/projecttest2'  # Folder path
    old_json = ""
    old_tracks = {}
    tracked_potholes = {}
    cropped_path = outputDir + "/cropped_images"
    print(cropped_path)
    if not os.path.exists(cropped_path):
        os.mkdir(cropped_path)
    tracked_potholes, old_tracks = track_cracks1(image_dir, mask_dir, old_json)
    tracked_potholes = track_cracks2(image_dir, tracked_potholes, old_tracks, new_json, old_json, cropped_path)
    cracksVisualize(image_dir, mask_dir)