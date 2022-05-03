import torch
import cv2
import time
import PoseModule as pm


def detectGoal(img):
    res = yolo_model(img, size=640)
    res.print()
    return res


def cropImage(img, results):
    xmin = int(results.pandas().xyxy[0]['xmin'])
    ymin = int(results.pandas().xyxy[0]['ymin'])
    xmax = int(results.pandas().xyxy[0]['xmax'])
    ymax = int(results.pandas().xyxy[0]['ymax'])

    cropped_image = image[ymin:ymax, xmin:xmax]

    

    return cropped_image

def scaleImage(img, results):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dsize = (width, height)

    scaledImage = cv2.resize(img, dsize)

    return scaledImage


yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
detector = pm.poseDetector()




frame_rate = 10
prev = 0
scale_percent = 200


vidcap = cv2.VideoCapture('./Yolo/Video till AI/Bra exempel 9m/Bra 9m/Video 2018-07-24 18 48 02.mov')
success, image = vidcap.read()

while success:

    time_elapsed = time.time() - prev
    success, image = vidcap.read()

    if time_elapsed > 1./frame_rate:
        prev = time.time()
        # Do something with your image here.
        results = detectGoal(image)
        if results.pandas().xyxy[0].empty:
            break
        image = cropImage(image, results)
        image = scaleImage(image, results)
        image = detector.findPose(image)
        lmList = detector.findPosition(image)

    cv2.imshow("image", image)   
    cv2.waitKey(1)
