"""
@file goal_detector.py
@brief This program is made to find lines of a handball goal and measure angle of photo (POV).
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np


def sortBoxPoints(boxPoints: list) -> list:
    """
    Returns list with coordinates sorted from top left to bottom left (tl,tr,br,bl) of boxPoint list.
    """
    y_sorted = sorted(boxPoints, key=lambda point: point[1], reverse=True)
    top_right_to_left = sorted(y_sorted[:2], key=lambda p: p[0], reverse=True)
    bottom_left_to_right = sorted(y_sorted[2:], key=lambda p: p[0])
    return bottom_left_to_right + top_right_to_left


for f in range(1, 2):
    default_image = f'Computer Vision\Goal\img\goal{f}.png'

    img = cv2.imread(default_image, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (1080, 720), interpolation=cv2.INTER_AREA)
    imgray = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

    shape = img.shape
    height = shape[0]
    width = shape[1]

    blank = np.zeros((height, width, 3), dtype=np.uint8)
    bcop = blank

    ret, thresh = cv2.threshold(img, 150, 255, 0)
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    newContours = []

    # Pattern matching (5 vita rutor i höjdled, 7 stycken i sidled)
    # Rutor höjd/bredd ungefär lika med 25.5/9.5 = 2.7 +/- 0.3

    alignment_x = []
    alignment_boxes = []

    for cnt in contours[2:]:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)

        points = sortBoxPoints(box)
        midPoint = round((points[0][0]+points[1][0])/2)
        midPoint_y = round((points[2][1] + points[0][1])/2)

        dist_x = abs(points[1][0]-points[0][0])
        dist_y = abs(points[1][1]-points[2][1])
        area = dist_x*dist_y

        box = np.int0(box)
        cv2.drawContours(bcop, [box], 0, (255, 255, 255), 2)

        idx = -1
        for a in alignment_x:
            if a[0]-0.2*a[1] <= midPoint <= a[0]+0.2*a[1]:
                # if a[2] * 0.5 <= area <= a[2] * 2 or True:
                idx = alignment_x.index(a)
                alignment_boxes[idx].append(box)
        if idx == -1:
            alignment_x.append([midPoint, dist_x, area])
            alignment_boxes.append([box])

    filter(lambda x: len(x) <= 7, alignment_boxes)
    boxes = sorted(alignment_boxes, key=lambda l: len(l), reverse=True)

    for als in boxes:
        for b in als:
            cv2.drawContours(blank, [b], 0, (255, 255, 255), 2)
    # if 2.1 <= h/w <= 2.9 or 0.29 <= w/h <= 0.45:
    # cv2.rectangle(blank, (x, y), (x+w, y+h), (255, 255, 255), 2)

    # Edge detection
    dst = cv2.Canny(blank, 100, 200, None, 3)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)
    cblank = cv2.Canny(bcop, 100, 200, None, 3)
    ccblank = cv2.cvtColor(cblank, cv2.COLOR_GRAY2BGR)

    # # Using probabilistic Hough Line Transform to find lines:
    # lines = cv2.HoughLinesP(dst, 1, np.pi/180, 50, None, 100, 10)

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

    # # Regular Hough Line transform
    # lines = cv2.HoughLines(dst, 1, np.pi/180, 105, None, 0, 0)

    # if lines is not None:
    #     for i in range(0, len(lines)):
    #         l = lines[i][0]
    #         cv2.line(cdst, (l[0], l[1]), (l[2], l[3]),
    #                  (0, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow("Original", ccblank)
    cv2.imshow("\"Pattern Detection\"", cdst)
    cv2.waitKey()

    # print(lines)

# Gör så att pattern matching faktiskt gör nånting!!
