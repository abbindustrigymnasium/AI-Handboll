import torch
import cv2
import time
# import PoseModule as pm


def detectGoal(img):
    res = yolo_model(img, size=640)
    res.print()
    return res


def cropImage(img, results):
    xmin = int(results.pandas().xyxy[0]['xmin'])
    ymin = int(results.pandas().xyxy[0]['ymin'])
    xmax = int(results.pandas().xyxy[0]['xmax'])
    ymax = int(results.pandas().xyxy[0]['ymax'])

    image = cv2.imread(img)

    cropped_image = image[ymin:ymax, xmin:xmax]
    # cv2.imshow("cropped", cropped_image)
    # cv2.waitKey(0)

    return cropped_image

yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path='best.pt', force_reload=True)
# detector = pm.poseDetector()

frame_rate = 10
prev = 0


vidcap = cv2.VideoCapture('./Video till AI/Sämre exempel 9m/Sämre 9m/nov52021-925fm-eeHazm.MOV')
success,image = vidcap.read()

while True:

    time_elapsed = time.time() - prev
    success, image = vidcap.read()

    if time_elapsed > 1./frame_rate:
        prev = time.time()
        # Do something with your image here.
        results = detectGoal(image)
        image = cropImage(image, results)
        # image = detector.findPose(image)
        # lmList = detector.findPosition(image)
    
    cv2.imshow("image", image)
    cv2.waitKey(1)






# results = detectGoal('best.pt', './Frames/frame1.jpg')

# image = cropImage(results)