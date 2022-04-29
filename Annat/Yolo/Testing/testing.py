import torch
import cv2


def detectGoal(model_name, img):
    yolo_model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_name, force_reload=True)
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
    cv2.imshow("cropped", cropped_image)
    cv2.waitKey(0)

    return cropped_image



results = detectGoal('best.pt', './Frames/frame1.jpg')

image = cropImage(results)