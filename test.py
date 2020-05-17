from tkinter import *
import capture
import speech_recognition as sr
import numpy as np
import cv2
import face_recognition
import logging
import time
import face_reg
import google_ocr
import ner
import os
import config
global user
root = Tk()
printout = Text(root)
root.title("Face enabled Time clock")
root.attributes("-zoomed",True)

S = Scrollbar(root)
T = Text(root, height=4, width=50)
S.pack(side=RIGHT, fill=Y)
T.pack(side=LEFT, fill=Y)
S.config(command=T.yview)

photo=PhotoImage(file='test_ub.png')
canvas=Canvas(root,width=1000,height=400)
canvas.pack()
canvas.create_image(20,10,anchor=NW, image=photo)
label = Label(root, text= "Welcome!")
label.pack()    


def action(text):
    global user
    T.insert(END,"You want to :{}\n".format(text)) 
    name = user
    print("Name",name)
    logger=logging.getLogger(__name__) 
    logger.setLevel(logging.INFO)
    log_file = "{}.log".format(config.LOG+name)
    log_format = "[%(message)s] :--[%(asctime)s]"
    formatter = logging.Formatter(log_format)
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    print("hi")
    if text == "login":
        logger.info("Log in Time")
        T.insert(END,"{} : {} Successful\n".format(name, text))
    if text == "logout" or text == "log out":
        logger.info("Log Out Time") 
        T.insert(END,"{} : {} Successful\n".format(name, text))

   

def detect():
    global user
    video_capture = cv2.VideoCapture(0)
    known_face_encodings = []
    known_face_names = []
    for enc in os.listdir('encoded_image'):
        known_face_names.append(enc.split('.')[0])
        known_face_encodings.append(np.fromfile('encoded_image/'+enc))
    
    print(known_face_names)
    print(known_face_encodings)
    data = 0
    if known_face_names and known_face_encodings:
        data = 1
    else:
        T.insert(END, "Empty! please say Start to fill you data!\n")
    #print('Learned encoding for', len(known_face_encodings), 'images.')

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    Unknown_count = 0
    name = "Unknown"
    user = name
    while Unknown_count < 100 and name == "Unknown" and data:
        print(name)
        print(Unknown_count)
        Unknown_count += 1
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"

                # # If a match was found in known_face_encodings, just use the first one.
                # if True in matches:
                #     first_match_index = matches.index(True)
                #     name = known_face_names[first_match_index]

                # Or instead, use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
               
                face_names.append(name)

        process_this_frame = not process_this_frame


        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (100,200)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2
        # Display the resulting image
        cv2.putText(frame,str(Unknown_count), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
        # Display the resulting image
        cv2.imshow('Video', frame)
        
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) and 0xFF == ord('q'):
            break
        
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    if name is not "Unknown":
        T.insert(END, "Welcome:{}\n".format(name))
        T.insert(END, "Please say login or logout!\n")
        print("Welcome:{}\n".format(name))
        user = name
    elif Unknown_count > 5:
        captureimage()
    

def captureimage():
    video_capture = cv2.VideoCapture(0)

    # Initialize some variables
    face_locations = []
    count = 30
    while True and count > 0 :
        count -= 1
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Resize frame of video to 1/4 size for faster face detection processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(small_frame, model="cnn")

        # Display the results
        for top, right, bottom, left in face_locations:
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Extract the region of the image that contains the face
            frame = frame[top:bottom, left:right]

            # Blur the face image
            #face_image = cv2.GaussianBlur(face_image, (99, 99), 30)
            #face_image = cv2.rectangle( face_image, (left,top), (right, bottom), (255,0,0))
            # Put the blurred face region back into the frame image
            #frame[top:bottom, left:right] = face_image
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (0,30)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2
        # Display the resulting image
        cv2.putText(frame,str(count), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
        cv2.imshow('Video', frame)
        # Display the resulting image
        #cv2.imshow('Face detect', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    face_frame = frame
    video_capture.release()
    cv2.destroyAllWindows()
    video_capture = cv2.VideoCapture(0)
    # Initialize some variables
    count = 100
    while True and count>0:
        count -= 1
        # Grab a single frame of video
        ret, frame = video_capture.read()

        cv2.rectangle(frame,(100,100), (600,400), (0,0,255),3)
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (80,80)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2
        # Display the resulting image
        cv2.putText(frame,str(count), 
        bottomLeftCornerOfText, 
        font, 
        fontScale,
        fontColor,
        lineType)
        # Display the resulting image
        cv2.imshow('document', frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cv2.imwrite("document.jpg",frame[100:400,100:600])
    result = google_ocr.detect_text("document.jpg")
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()

    T.insert(END, "Is this your name?: {}\n".format(result["PERSON"][0]))
    print(result["PERSON"][0])
    print(face_frame)
    if result["PERSON"][0]:
        new_face_image = config.IMAGE_PATH+result["PERSON"][0]+".jpg"
        cv2.imwrite(new_face_image,face_frame)
        image = face_recognition.load_image_file(new_face_image)
        face_encoding = face_recognition.face_encodings(image)[0]
        face_encoding.tofile(config.ENCODED_IMAGE+result["PERSON"][0]+".enc")
    T.insert(END, "We have recorded you!\n")

def task():
    r = sr.Recognizer()
    with sr.Microphone() as source: 
        audio = r.listen(source)
        try:
            voice = r.recognize_google(audio)
            print(voice)
            text = voice.split()
            #label = Label(root, text=  "You said : {}".format(text))
            #label.pack() 
            print("You said : {}".format(text))
            T.insert(END, "You said : {}\n".format(voice))
            if "stop" in text or "quit" in text or "thank" in text or "bye" in text:
                root.destroy()
            elif "start" in text or "enter" in text:
                captureimage()
            elif "hi" in text or "yes" in text:
                detect()
            elif ("log" in text and "in" in text) or "login" in text:
                action("login")
            elif ("log" in text and "out" in text) or "logout" in text:
                action("logout")
        except:
            #T.insert(END,"Sorry could not recognize what you said\n")
            T.insert(END, "Speak Now!\n")
    root.after(1000, task)  # reschedule event in 2 seconds


T.insert(END, "Hi! I'm Victor How Can I help you!\n")
root.after(1000, task)
root.mainloop()