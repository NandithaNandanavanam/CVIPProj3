import cv2

def capture_image():
    cam = cv2.VideoCapture(0)
    cv2.namedWindow("test")
    img_counter = 0
    
    while True:
        ret, frame = cam.read()
        if not ret:
            print("failed to grab frame")
            break      
        cv2.imshow("test", frame)
        img_counter=img_counter+1
     
        if img_counter==100:
            print("Image Captured")
            break
       
    cam.release()
    cv2.destroyAllWindows()

    return frame
