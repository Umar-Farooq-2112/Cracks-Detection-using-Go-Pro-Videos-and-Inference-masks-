import numpy as np
import cv2
import json



def resize_image(image, scale_percent=50):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)    


class Crack:
    def __init__(self,crack_no,bbox,area):
        self.no = crack_no
        self.bBox = bbox
        self.area = area
    def getBoundingBoxCoordinates(self):
        x,y,w,h = self.bBox
        return np.array([[x,y],[x+w,y],[x+w,y+h],[x,y+h]],np.int32)
    def getPoints(self):
        x,y,w,h = self.bBox
        return np.array([[x,y],[x+w,y+h]],np.int32)
    
    
img1= "00000006"
img2= "00000007"

if int(img1)>int(img2):
    img1,img2=img2,img1


parent = "Testing"
json_path = "Testing/potholestracked.json"
image1 = parent+"/images/"+img1+".png"
image2 = parent+"/images/"+img2+".png"
mask1 = parent+"/Reconstructions_Inference/"+img1+".png"
mask2 = parent+"/Reconstructions_Inference/"+img2+".png"

image1 = cv2.imread(image1)
image2 = cv2.imread(image2)
mask1 = cv2.imread(mask1)
mask2 = cv2.imread(mask2)


# def init(json_path,images_dir,masks_dir):
tracked_potholes = json.load(open(json_path))
trans_matrix = np.array(tracked_potholes["Potholes"][img1]["tran_matrix"])    
cracks = tracked_potholes["Potholes"][img1]["PotholesData"]    


# String all the cracks as Objects of class Crack
all_cracks = []
for item in cracks:
    all_cracks.append(Crack(item["pothole_num"],np.array(item["bbox"]),item["area"]))

# Getting transformed cracks bounding boxes from trans matrix and previous image cracks
transformed_cracks = []
for item in all_cracks[:]:
    point = np.array(item.getBoundingBoxCoordinates(),dtype=np.float32)
    point = point.reshape((-1, 1, 2))
    res = cv2.perspectiveTransform(point,trans_matrix)
    transformed_cracks.append(res)

#  Plotting the transformed bounding boxes
for i,item in enumerate(transformed_cracks):
    points = np.array(item,np.int32)
    cv2.polylines(mask1, [all_cracks[i].getBoundingBoxCoordinates()], isClosed=True, color=(0, 0, 0), thickness=2)
    cv2.polylines(mask2, [points], isClosed=True, color=(0, 0, 0), thickness=2)
    cv2.putText(mask1, str(i), all_cracks[i].getBoundingBoxCoordinates()[0], cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
    cv2.putText(mask2, str(i), points[0][0], cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)


cv2.imshow("Mask1",resize_image(mask1,70))
cv2.imshow("Mask2",resize_image(mask2,70))
cv2.waitKey(0)
cv2.destroyAllWindows()