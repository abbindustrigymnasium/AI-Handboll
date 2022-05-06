import torch
import cv2
import time
import PoseModule as pm
from PoseModule import poseDetector
import os

# Use the Yolo model to detect the goal int the image
def detectGoal(img):
    res = yolo_model(img, size=640)
    res.print()
    return res

# Crop the image, so there is less disturbance in the image
def cropImage(img, results):
    xmin = int(results.pandas().xyxy[0]['xmin'])
    ymin = int(results.pandas().xyxy[0]['ymin'])
    xmax = int(results.pandas().xyxy[0]['xmax'])
    ymax = int(results.pandas().xyxy[0]['ymax'])

    new_xmax = int((xmax - xmin)/2) + int(((ymax - ymin)/2)*(16/9)) + xmin
    new_xmin = int((xmax - xmin)/2) - int(((ymax - ymin)/2)*(16/9)) + xmin

    
    cropped_image = img[ymin:ymax, new_xmin:new_xmax]
    return cropped_image

# Scale the image to 1080 height
def scaleImage(img):
    dsize = (1920, 1080)
    scaledImage = cv2.resize(img, dsize)
    return scaledImage



# Some variables
frame_rate = 10
prev = 0
count = 0

# Capture the video 
vidcap = cv2.VideoCapture('./Yolo/Video till AI/Bra exempel 9m/Bra 9m/Video 2018-07-24 18 48 02.mov')
success, image = vidcap.read()


while success:
    time_elapsed = time.time() - prev
    if time_elapsed > 1./frame_rate:
        success, image = vidcap.read()
        print(count)
        cv2.imwrite('TempFrames/frame%d.jpg' % count, image)
        prev = time.time()
        count += 1
    


# Load the Yolo model
yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)

# Declare poseDetector
detector = pm.poseDetector()


# for filename in os.listdir("Temp/"):
#     if filename.endswith(".jpg"): 
#         # Detecting goal
#         results = detectGoal(filename)
#         # If no goal detected break the loop
#         if results.pandas().xyxy[0].empty:
#             print("No goal detected!")
#             break

#         # Croping and scaling the image
#         cropedImage = cropImage(filename, results)
#         scaledImage = scaleImage(cropedImage)

#         # Finding the goalkeepers position
#         findImage = detector.findPose(scaledImage)
#         lmList = detector.findPosition(findImage)

#         # ---------------------------------------
#         # Här kan du placera din algoritm William
#         # ---------------------------------------

#         cv2.imshow("image", findImage)   
#         continue
    