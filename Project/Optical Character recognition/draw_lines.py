import cv2
import sys

img = cv2.imread(sys.argv[1])

vertices1 = (100,100)
vertices2 = (300,300)
cv2.line(img, vertices1, vertices2, (0, 255, 0), thickness=3, lineType=8)

cv2.imwrite("result"+sys.argv[1],img)

