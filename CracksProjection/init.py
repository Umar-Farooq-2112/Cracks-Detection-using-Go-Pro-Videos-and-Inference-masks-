import cv2
import numpy as np
import json
import pandas as pd
# from CracksProjection.boundingBox import convert_bbox
import os
# from CracksProjection.movingCracks import going_forward,going_forward_only
from CracksProjection.intersectionOverUnion import calculate_iou
# from intersectionOverUnion import calculate_iou


def is_bbox_inside_image_backward(bbox_coords, image_size):
    width, height = image_size


    for coord in bbox_coords:
        c = coord[0]
        x, y = c[0], c[1]
        if  y < 0  or y >= height or x<0 or x>= width:
            return False
    return True



def tranformBboxToCoordinates(box):
    x,y,w,h = box
    return [(x,y),(x+w,y),(x+w,y+h),(x,y+h)]
def tranfromCoordinatesToBBox(coor):
    a,b,c,d = coor
    x,y = a
    w = c[0]-x
    h = c[1]-y
    return [x,y,w,h]
def transformCoordinatesToMaxCoordinates(coor):
    a,_,c,_ = coor
    return [a[0],a[1],c[0],c[1]]
        
def compare_two_images(cracks1,cracks2 ,shape_of_image = (1920,1080)):
    
    trans_matrix = np.array(cracks1['tran_matrix'])
    
    
    for crack in cracks1['PotholesData']:
        bBox = crack['bbox']        
        coordinates = tranformBboxToCoordinates(bBox)
        transformed_box = np.array(coordinates,dtype=np.float32)
        transformed_box = transformed_box.reshape((-1,1,2))
        transformed_box = cv2.perspectiveTransform(transformed_box,trans_matrix)
        if not 'parent' in crack:
            crack['parent'] = None
        # if not is_bbox_inside_image_backward(transformed_box,shape_of_image):
        #     continue
        transformed_box = transformed_box.reshape((-1,2))
        transformed_box = transformCoordinatesToMaxCoordinates(transformed_box)
        
        for item in cracks2['PotholesData']:
            if not 'parent' in item:
                item['parent'] = None
            bBox2 = transformCoordinatesToMaxCoordinates(tranformBboxToCoordinates(item['bbox']))
            iou = calculate_iou(transformed_box,bBox2)*100
            if iou > 0:
                if crack['area']>=item['area']:
                    item['parent'] = f"{crack['pothole_num']}"
                else:
                    crack['parent'] = f"{crack['pothole_num']}"
            
    return cracks1,cracks2


def processingCrackFiltering(tracked_cracks):
    print("Started Cracks Filtering......................................")
    length = len(tracked_cracks['Potholes'])
    count = 0
    for item1 in tracked_cracks['Potholes']:
        count+=1
        if count==length:
            break
        item2 = str(int(item1)+1)
        item2 = (len(item1)-len(item2))*'0'+item2
                
        print(f"Filtering Image {item1} and {item2}....................." )
        tracked_cracks['Potholes'][item1],tracked_cracks['Potholes'][item2] = compare_two_images(tracked_cracks['Potholes'][item1],tracked_cracks['Potholes'][item2])
    print("Done With Filtering..........................")
    with open(f'Testing/tracked_parents.json', 'w') as json_file:
       json.dump(tracked_cracks, json_file, indent=4)
    return tracked_cracks

def getUniqueCracks(tracked_cracks):
    for item in tracked_cracks['Potholes']:
        # print("Image number: " + item)
        if len(tracked_cracks['Potholes'][item]['PotholesData'])>0:
            df = pd.DataFrame(tracked_cracks['Potholes'][item]['PotholesData'])

            df = df[df['parent'].isnull()]
            tracked_cracks['Potholes'][item]['PotholesData'] = df.to_dict(orient="records")
    print("Filtering Unique Cracks Successful............................")
    return tracked_cracks    



def init(tracked_cracks,result_dir):
    result_dir = os.path.join(result_dir,'ProcessedCracks.json')
    
    tracked_cracks = processingCrackFiltering(tracked_cracks)
    tracked_cracks = getUniqueCracks(tracked_cracks)
    
    with open(result_dir, 'w') as file:
        json.dump(tracked_cracks, file,indent=4)
    print("Successful...................................................")

if __name__ == "__main__":
    json_file= json.load(open("Testing/potholestracked.json"))

    masks_dir = "Testing/Reconstructions_Inference"
    result_dir = "Testing"
    # tracked = processingCrackFiltering(json_file)
    init(json_file,"Testing/")

    
    
    # df1 = pd.DataFrame(c1['PotholesData'])
    # df2 = pd.DataFrame(c2['PotholesData'])
    
    # print(df1.head())
    # print(df2.head())
