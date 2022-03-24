import cv2
import time
import PoseModule as pm


cap = cv2.VideoCapture(0)
pTime = 0
detector = pm.poseDetector()


def calcFPS(img, pTime):
    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50),
                cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    return img


while True:
    success, img = cap.read()
    img = detector.findPose(img)
    lmList = detector.findPosition(img)
    # print(lmList[14])    //Specific Datapoint
    print(lmList)  # All points

    img = calcFPS(img, pTime)
    cv2.imshow("image", img)
    cv2.waitKey(1)
