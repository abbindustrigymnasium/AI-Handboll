"""
@file goal_detector.py
@brief This program is made to find lines of a handball goal and measure angle of photo (POV).
"""

import cv2
from cv2 import cvtColor
import matplotlib.pyplot as plt
import numpy as np

for f in range(1, 2):
    default_image = f'Goal\img\goal{f}.png'

    img = cv2.imread(default_image, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (1080, 720), interpolation=cv2.INTER_AREA)
    imgray = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    shape = img.shape
    height = shape[0]
    width = shape[1]

    blank = np.zeros((height, width, 3), dtype=np.uint8)

    ret, thresh = cv2.threshold(img, 127, 255, 0)
    cv2.imshow("bw", thresh)
    cv2.waitKey(0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    sortedContours = sorted(
        contours, key=lambda x: cv2.contourArea(x), reverse=True)[:25]

    # cv2.drawContours(blank, sortedContours, -1, (0, 0, 255), 3)

    # Pattern matching (5 vita rutor i höjdled, 7 stycken i sidled)
    for cnt in sortedContours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(blank, [box], 0, (0, 0, 255), 2)

    # Edge detection
    dst = cv2.Canny(blank, 100, 200, None, 3)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    # # Using probabilistic Hough Line Transform to find lines:
    lines = cv2.HoughLinesP(dst, 1, np.pi/180, 50, None, 100, 10)

    # # Regular Hough Line transform
    # lines = cv2.HoughLines(dst, 1, np.pi/180, 105, None, 0, 0)

    # if lines is not None:
    #     for i in range(0, len(lines)):
    #         rho = lines[i][0][0]
    #         theta = lines[i][0][1]
    #         a = np.cos(theta)
    #         b = np.sin(theta)
    #         x0 = a * rho
    #         y0 = b * rho
    #         pt1 = (int(x0+1000*(-b)), int(y0 + 1000*(a)))
    #         pt2 = (int(x0-1000*(-b)), int(y0 - 1000*(a)))

    #         cv2.line(cdst, pt1, pt2, (0, 255, 255), 1, cv2.LINE_AA)

    if lines is not None:
        for i in range(0, len(lines)):
            l = lines[i][0]
            cv2.line(cdst, (l[0], l[1]), (l[2], l[3]),
                     (0, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow("Detected Lines (yellow)", cdst)
    cv2.waitKey()

    print(lines)

    # !!!
    # FIXA SPAGhETTI
    # Pattern matching/detection
    # !!!
