import cv2
vidcap = cv2.VideoCapture('./Video till AI/Sämre exempel 9m/sen i redo/vid6.mp4')
success,image = vidcap.read()
count = 606
i = 0

while success:

    if i >= 19:
        cv2.imwrite("Frames/frame%d.jpg" % count, image)
        i = 0
        count += 1
    elif i != 19:
        i += 1

    success,image = vidcap.read()
    
    