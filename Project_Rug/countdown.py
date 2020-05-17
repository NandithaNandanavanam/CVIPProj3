import numpy as np
import cv2
import time
def draw_text(frame, text, x, y, color=(255,0,0), thickness=4, size=3):
            if x is not None and y is not None:
                cv2.putText(frame, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)


    #timeout = time.time() + 11   # 10 seconds from now
cap = cv2.VideoCapture(0)
init_time = time.time()
test_timeout = init_time+6
final_timeout = init_time+17
counter_timeout_text = init_time+1
counter_timeout = init_time+1
counter = 5
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        center_x = int(frame.shape[0]/2)
        center_y = int(frame.shape[0]/2)
        if (time.time() > counter_timeout_text and time.time() < test_timeout):
            draw_text(frame, str(counter), center_x, center_y)
            counter_timeout_text+=0.03333
        if (time.time() > counter_timeout and time.time() < test_timeout):
            counter-=1
            counter_timeout+=1
        if counter == 0:
            break
        cv2.imshow('frame', frame)
        if (cv2.waitKey(1) & 0xFF == ord('q')) or (time.time() > final_timeout):
            break
    else:
        break
# Release everything if job is finished
img_name = "example.png"
cv2.imwrite(img_name, frame)
print("{} written!".format(img_name))
cap.release()
cv2.destroyAllWindows()