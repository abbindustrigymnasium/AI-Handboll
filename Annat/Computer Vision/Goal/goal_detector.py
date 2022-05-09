"""
@file goal_detector.py
@brief This program is made to find lines of a handball goal and measure angle of photo (POV).
"""

from statistics import median
import string
from time import time
import cv2
from cv2 import minAreaRect
from cv2 import boxPoints
import matplotlib.pyplot as plt
import numpy as np


def sortBoxPoints(boxPoints: list) -> list:
    """
    Returns list with coordinates sorted from top left to bottom left (tl,tr,br,bl) of boxPoint list.
    """
    y_sorted = sorted(boxPoints, key=lambda point: point[1], reverse=True)
    top_right_to_left = sorted(y_sorted[:2], key=lambda p: p[0], reverse=True)
    bottom_left_to_right = sorted(y_sorted[2:], key=lambda p: p[0])
    return np.array(bottom_left_to_right + top_right_to_left)


def averageArea(boxes: list) -> float:
    """
    Returns float of average area of boxes (to be used in sort function)
    """
    sum = 0

    for box in boxes:
        sum += cv2.contourArea(box)
    try:
        result = sum/(len(boxes))
    except ZeroDivisionError as ZDE:
        result = 0
    return result


def medianArea(alignment_boxes: list) -> float:
    """Returns float of median box area (to be used to sort out exceptionally large or exceptionally small boxes)"""
    areas = []

    for align in alignment_boxes:
        for box in align:
            areas.append(cv2.contourArea(box))

    return np.median(np.array(areas))


for f in range(6, 7):
    default_image = f'Annat\Computer Vision\Goal\img\goal{f}.png'
    # default_image = 'Computer Vision/Goal/img/test_line.png'

    img = cv2.imread(default_image)
    img = cv2.resize(img, (1080, 720), interpolation=cv2.INTER_AREA)
    frame_HSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    thresh = cv2.inRange(
        frame_HSV, (0, 0, 183), (180, 78, 255))

    shape = img.shape
    height = shape[0]
    width = shape[1]

    blank = np.zeros((height, width, 3), dtype=np.uint8)

    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    newContours = []

    # Pattern matching (5 vita rutor i höjdled, 7 stycken i sidled)
    # Rutor höjd/bredd ungefär lika med 25.5/9.5 = 2.7 +/- 0.3

    alignment_x = []
    alignment_y = []
    alignment_boxes = {'x': [], 'y': []}

    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)

        points = sortBoxPoints(box)
        midPoint = round((points[0][0]+points[1][0])/2)
        midPoint_y = round((points[2][1] + points[0][1])/2)

        dist_x = abs(points[1][0]-points[0][0])
        dist_y = abs(points[1][1]-points[2][1])

        area = dist_x*dist_y

        box = np.int0(box)

        if dist_x*dist_y == 0:
            continue

        idx = -1
        if 2.1 <= dist_y/dist_x <= 2.9 or 2.1 <= dist_x/dist_y <= 2.9:
            for a in alignment_x:
                if a[0]-0.5*a[1] <= midPoint <= a[0]+0.5*a[1]:
                    idx = alignment_x.index(a)
                    alignment_boxes['x'][idx].append(box)
            if idx == -1:
                alignment_x.append([midPoint, dist_x])
                alignment_boxes['x'].append([box])

        idy = -1
        for a in alignment_y:
            if a[0] - 4*a[1] <= midPoint_y <= a[0] + 4*a[1]:
                if a[2] - 3*a[3] <= midPoint <= a[2] + 3*a[3]:
                    idy = alignment_y.index(a)
                    alignment_boxes['y'][idy].append(box)
        if idy == -1:
            alignment_y.append([midPoint_y, dist_y, midPoint, dist_x])
            # alignment_boxes['y'].append(box])
            alignment_boxes['y'].append([box])

    boxes = {"x": [], "y": []}

    filtered_boxes_x = list(filter(lambda x: len(
        x) > 1 and len(x) <= 7, alignment_boxes['x']))

    filtered_boxes_y = list(filter(lambda x: len(
        x) > 1 and len(x) <= 7, alignment_boxes['y']))

    boxes["x"] = sorted(filtered_boxes_x, key=averageArea, reverse=True)
    boxes["y"] = sorted(filtered_boxes_y, key=averageArea, reverse=True)

    med = medianArea(boxes["x"] + boxes["y"])

    lines = []

    for alx in boxes["x"]:
        # centerPoints = []
        for b in alx:
            if med*0.7 < cv2.contourArea(b) < med*1.6:
                cv2.drawContours(blank, [b], 0, (255, 255, 255), 2)
                cv2.drawContours(img, [b], 0, (0, 255, 0), 2)
                # points = sortBoxPoints(box)
                # centerPoint = (int((points[0][0]+points[1][0])/2),
                #                int((points[1][1]+points[2][1])/2))
                # centerPoints.append(centerPoint)
                # cv2.circle(
                # img, (centerPoint[0], centerPoint[1]), 1, (0, 255, 0), 3, cv2.LINE_AA)

        # centerPoints.sort(key=lambda p: p[1], reverse=True)
        # lines.append([[centerPoints[0][0], centerPoints[0][1],
        #              centerPoints[-1][0], centerPoints[-1][1]]])

        # cv2.line(img, (centerPoints[0][0], centerPoints[0][1]), (
        #     centerPoints[-1][0], centerPoints[-1][0]), (0, 0, 255), 2, cv2.LINE_AA)

    for aly in boxes["y"]:
        # centerPoints = []
        for b in aly:
            if med*0.7 < cv2.contourArea(b) < med*1.6:
                cv2.drawContours(blank, [b], 0, (255, 255, 255), 2)
                cv2.drawContours(img, [b], 0, (0, 255, 0), 2)

                # points = sortBoxPoints(box)
                # centerPoint = (int((points[0][0]+points[1][0])/2),
                #                int((points[1][1]+points[2][1])/2))

                # cv2.circle(
                #     img, (centerPoint[0], centerPoint[1]), 1, (0, 255, 0), 3, cv2.LINE_AA)
                # centerPoints.append(centerPoint)

        # centerPoints.sort(key=lambda p: p[0], reverse=True)
        # lines.append([[centerPoints[0][0], centerPoints[0][1],
        #              centerPoints[-1][0], centerPoints[-1][1]]])

        # cv2.line(img, (centerPoints[0][0], centerPoints[0][1]), (
            # centerPoints[-1][0], centerPoints[-1][1]), (0, 0, 255), 2, cv2.LINE_AA)

    # Edge detection
    dst = cv2.Canny(blank, 100, 200, None, 3)
    cdst = cv2.cvtColor(dst, cv2.COLOR_GRAY2BGR)

    # # # Using probabilistic Hough Line Transform to find lines:
    lines = cv2.HoughLinesP(dst, 1, np.pi/180, 5, None, 5, 50)

    # Equation of line is mx + b, where m = (y_1 - y_0) / (x_1 - x_0) and b is intersection with (0,0)

    slopes = []
    ms = []
    simiLines = []
    x_vertical = []

    for line in lines:
        m = None
        b = line[0][0]
        if line[0][2] - line[0][0] != 0:
            m = ((line[0][3] - line[0][1]) / (line[0][2] - line[0][0]))
            b = line[0][1] - m * line[0][0]
        else:
            m = "VERTICAL"

        l = line[0]

        similar = False
        for slope in slopes:
            if m != "VERTICAL" and slope[0] != "VERTICAL":
                if not 0.8*slope[0] <= m <= 1.2*slope[0] and not slope[1]-25 <= l[0] <= slope[1]+25 and not slope[2]-25 <= l[1] <= slope[2]+25:
                    pass
                else:
                    similar = True
            elif m == "VERTICAL" and slope[0] == "VERTICAL":
                if not slope[1]-25 <= l[0] <= slope[1]+25 and not slope[2]-25 <= l[1] <= slope[2]+25:
                    pass
                else:
                    similar = True

        if not similar:
            slopes.append([m, l[0], l[1], l[2], l[3]])
            if m == "VERTICAL":
                x_vertical.append(l[0])
            simiLines.append(line)

    newSlopes = []
    newSimiLines = []

    for slope in slopes:
        if slope[0] != "VERTICAL":
            if slope[1] not in x_vertical:
                newSlopes.append(slope)
                newSimiLines.append(simiLines[slopes.index(slope)])
        elif slope[0] == "VERTICAL":
            newSlopes.append(slope)
            newSimiLines.append(simiLines[slopes.index(slope)])

    print(x_vertical)

    # for x in x_vertical:
    #     cv2.circle(img, (x[0], x[1]), 3, (255, 0, 0), 1, cv2.LINE_AA)
    slopes = newSlopes
    simiLines = newSimiLines

    if len(simiLines) > 0:
        for i in range(0, len(simiLines)):
            l = simiLines[i][0]
            cv2.line(cdst, (l[0], l[1]), (l[2], l[3]),
                     (0, 0, 255), 2, cv2.LINE_AA)
    else:
        print("Lines empty!")

    # SKA FORTSÄTTA PÅ DENNA SOM SNARAST b = line[0][1] - m * line[0][0] line[0][0] = slope[1]
    # Horisontell linje får inte vara på underdelen av vertikala linjen

    # Horizontal Slopes
    h_slopes = list(filter(lambda s: s[0] != "VERTICAL", slopes))
    # Vertical Slopes
    v_slopes = list(filter(lambda s: s[0] == "VERTICAL", slopes))

    found_goal = False

    for v1 in v_slopes:
        x_v1 = v1[1]
        y_v1 = v1[2]
        for h in h_slopes:
            m_h = h[0]
            b_h = h[2] - m_h * h[2]
            if 0 < m_h * x_v1 + b_h < img.shape[0]:
                x_h = x_v1
                y_h = m_h * x_v1 + b_h
                print("1")
                for v2 in v_slopes:
                    if v1 != v2:
                        x_v2 = v2[1]
                        y_v2 = v2[2]
                        print("2")
                        if 0 < m_h * x_v2 + b_h < img.shape[0]:
                            x_h2 = x_v2
                            y_h2 = m_h * x_v2 + b_h
                            print("3")
                            found_goal = True
                            break
            if found_goal:
                break
        if found_goal:
            break

    # Målets hörn: (x_h, y_h) - -> (x_h2, y_h2)
    # Sen går det ner från de punkterna till  och

    x_h, y_h, x_h2, y_h2, x_v1, y_v1, x_v2, y_v2 = list(map(
        int, [x_h, y_h, x_h2, y_h2, x_v1, y_v1, x_v2, y_v2]))

    cv2.line(img, (x_h, y_h), (x_h2, y_h2), (0, 0, 255), 2, cv2.LINE_AA)
    cv2.line(img, (x_v2, y_v2), (x_h2, y_h2), (0, 0, 255), 2, cv2.LINE_AA)
    cv2.line(img, (x_v1, y_v1), (x_h, y_h), (0, 0, 255), 2, cv2.LINE_AA)

    cv2.line(cdst, (x_h, y_h), (x_h2, y_h2),   (255, 0, 255), 2, cv2.LINE_AA)
    cv2.line(cdst, (x_v2, y_v2), (x_h2, y_h2), (255, 0, 255), 2, cv2.LINE_AA)
    cv2.line(cdst, (x_v1, y_v1), (x_h, y_h),   (255, 0, 255), 2, cv2.LINE_AA)

    cv2.imshow("Result", img)
    cv2.imshow("Contours", cdst)
    cv2.waitKey()
