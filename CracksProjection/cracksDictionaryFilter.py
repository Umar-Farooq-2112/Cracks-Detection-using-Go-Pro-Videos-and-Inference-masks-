import numpy as np
import cv2
import pandas as pd
import json


### bBox = [x,y,w,h]
### shape_of_image (the 2nd image) [h,w]
### next_image_cracks: Cracks Dictionary that have stored all the cracks of the 
###    2nd image to whom the above bBox would be compared having pothole_num,bbox,area 
### trans_matrix: transformation matrix to convert from bBox to next_image_cracks Bounding Boxes
### area = actual area of the crack



def removeExtraCracks(bBox,shape_of_image,next_image_cracks,trans_matrix,area=None,lengths_threshold = 20,area_threshold = 50):
    x,y,w,h = bBox
    trans_matrix - np.array(trans_matrix)
    point = np.array([(x,y),(x+w,y),(x+w,y+h),(x,y+h)],dtype=np.float32)
    point = point.reshape((-1, 1, 2))
    point = cv2.perspectiveTransform(point,trans_matrix)
    
    x,y = int(point[0][0][0]),int(point[0][0][1])
    w,h = (int(point[1][0][0]-x),int(point[2][0][1]-y))

    x1,y1 = max(int(x - (shape_of_image[1]*lengths_threshold/100)),0),max(int(y - (shape_of_image[0]*lengths_threshold/100)),0)
    x2,y2 = min(int(x + w + (shape_of_image[1]*lengths_threshold/100)),shape_of_image[1]),min(int(y + h + (shape_of_image[0]*lengths_threshold/100)),shape_of_image[0])

    df = pd.DataFrame(next_image_cracks)
    df[['x', 'y', 'w', 'h']] = pd.DataFrame(df['bbox'].tolist(), index=df.index)
    
    detected = df[(df['x']>x1) & (df['y'] > y1) & (df['x']+df['w']<x2) & (df['y']+df['h']<y2)]
    if area is not None:
        area_threshold = area_threshold/100
        detected = detected[(detected["area"]>(1-area_threshold)*area)&(detected["area"]<(1+area_threshold)*area)]
    
    detected = detected.drop(columns=["x","y","w","h"])
    
    # print(len(df))
    # print(len(detected))
    # print(df.head())
    # print(detected.head())
    
    detected = detected.to_dict(orient="index")
    return detected


if __name__ == "__main__":
    tracked_potholes = json.load(open("Testing/potholestracked.json"))
    lengths_threshold = 100
    image = np.zeros((1920,1080),dtype=np.uint8)

    bbox = tracked_potholes["Potholes"]["00000015"]["PotholesData"][3]["bbox"]
    area = tracked_potholes["Potholes"]["00000015"]["PotholesData"][3]["area"]
    cracks = tracked_potholes["Potholes"]["00000016"]["PotholesData"]
    trans_matrix = np.array(tracked_potholes["Potholes"]["00000015"]["tran_matrix"])
    removeExtraCracks(bbox,image,cracks,trans_matrix,None,)
