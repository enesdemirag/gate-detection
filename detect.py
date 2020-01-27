# Gate Finder with OpenCV in Python

import cv2
import numpy as np
import operator

def main(img):
    # Resize
    img = cv2.resize(img, (640, 360), interpolation = cv2.INTER_CUBIC)
    # Change Colorspace
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Mask
    masked = cv2.inRange(img, np.array([5, 5, 55]), np.array([40, 40, 250]))
    # Erosion
    eroded = cv2.morphologyEx(masked, cv2.MORPH_CLOSE, np.ones((5,5), np.uint8))

    # Find Contours
    img2, contours, hierarchy = cv2.findContours(eroded, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(img, contours, -1, (0, 255, 0), 1) # Draw Borders

    # Find the biggest area and draw a rectangle
    areas = {cv2.contourArea(n): n for n in contours}

    # Sort
    sorted_areas = sorted(areas.items(), key=operator.itemgetter(0))

    i = 0
    legs = []
    for area in reversed(sorted_areas):
        if i < 2:
            x, y, w, h = cv2.boundingRect(area[1])
            if (w*1.5 >= h):
                continue
            i += 1
            legs.append([x, y, w, h])
        else:
            break

    # Save Image
    for leg in legs:
        cv2.rectangle(img, (leg[0], leg[1]), (leg[0]+leg[2], leg[1]+leg[3]), (0,0,0), 3)

    # cv2.imwrite("output.png", img)
    cv2.imshow("Output", img)

# Import Image
cap = cv2.VideoCapture('test.mp4')

while(cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:
        main(frame)
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break

cv2.destroyAllWindows()
