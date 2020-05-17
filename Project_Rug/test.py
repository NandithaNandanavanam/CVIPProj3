from tkinter import *
import capture
import speech_recognition as sr
import numpy as np
import cv2
import face_recognition
import time
import face_reg
import google_ocr
import ner
import os
import config
import logging
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
global name 

def detect():
    global name 
    video_capture = cv2.VideoCapture(0)
    known_face_encodings = []
    known_face_names = []
    for enc in os.listdir('encoded_image'):
        known_face_names.append(enc.split('.')[0])
        known_face_encodings.append(np.fromfile('encoded_image/'+enc))
    
    print(known_face_names)
    print(known_face_encodings)
    #print('Learned encoding for', len(known_face_encodings), 'images.')

    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    Unknown_count = 0
    name = "Unknown"
    while Unknown_count < 1000 and name == "Unknown":
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
        T.insert(END,"Please Say Login or Logout")
        print("Welcome:{}\n".format(name)) 
    elif Unknown_count > 5:
        captureimage()

def action(text):
    global name
    T.insert(END,"You want to :{}\n".format(text)) 
    name = name
    print("Name",name)
    logger=logging.getLogger(__name__) 
    logger.setLevel(logging.INFO)
    log_file = "{}.log".format(name)
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
        T.insert(END,"{} : {} Successful".format(name, text))

def draw_text(frame, text, x, y, color=(255,0,0), thickness=4, size=3):
            if x is not None and y is not None:
                cv2.putText(frame, text, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, size, color, thickness)

def captureimage():
    video_capture = cv2.VideoCapture(0)
    init_time = time.time()
    test_timeout = init_time+6
    final_timeout = init_time+17
    counter_timeout_text = init_time+1
    counter_timeout = init_time+1
    counter = 10
    face_locations = []

    while(video_capture.isOpened()):
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        face_locations = face_recognition.face_locations(small_frame, model="cnn")
        for top, right, bottom, left in face_locations:
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            frame = frame[top:bottom, left:right]
        if ret==True:
            center_x = int(small_frame.shape[0]/2)
            center_y = int(small_frame.shape[0]/2)
            if (time.time() > counter_timeout_text and time.time() < test_timeout):
                draw_text(small_frame, str(counter), center_x, center_y)
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
    # img_name = "example.png"
    # cv2.imwrite(img_name, small_frame)
    # print("{} written!".format(img_name))
    face_frame = frame
    # Initialize some variables
    while(video_capture.isOpened()):
        ret, frame = video_capture.read()
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
            cv2.rectangle(frame,(100,100), (600,400), (0,0,255),3)
            cv2.imshow('frame', frame)
            if (cv2.waitKey(1) & 0xFF == ord('q')) or (time.time() > final_timeout):
                break
        else:
            break
    cv2.imwrite("document.jpg",frame[100:400,100:600])
    result = google_ocr.detect_text("document.jpg")
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
    T.insert(END, "Is this your name?: {}\n".format(result["PERSON"][0]))
    '''
    r = sr.Recognizer()
    with sr.Microphone() as source: 
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            #label = Label(root, text=  "You said : {}".format(text))
            #label.pack() 
            print("You said : {}".format(text))
            T.insert(END, "You said : {}\n".format(text))
            if text == "yes":
                cv2.imwrite(result["PERSON"]+".jpg",face_frame)
        except:
            #T.insert(END,"Sorry could not recognize what you said\n")
            print("Speak....")
    '''
    print(result["PERSON"][0])
    # print(face_frame)
    #cv2.imwrite(result["PERSON"][0]+".jpg",face_frame)
    if result["PERSON"][0]:
        new_face_image = config.IMAGE_PATH+result["PERSON"][0]+".jpg"
        cv2.imwrite(new_face_image,face_frame)
        image = face_recognition.load_image_file(new_face_image)
        face_encoding = face_recognition.face_encodings(image)[0]
        face_encoding.tofile(config.ENCODED_IMAGE+result["PERSON"][0]+".enc")
    
    root.after(1000, task) 

def task():
    r = sr.Recognizer()
    with sr.Microphone() as source: 
        audio = r.listen(source)
        T.insert(END, "Speak Now!\n")
        try:
            text = r.recognize_google(audio)
            #label = Label(root, text=  "You said : {}".format(text))
            #label.pack() 
            print("You said : {}".format(text))
            T.insert(END, "You said : {}\n".format(text))
            if text == "stop" or text == "quit":
                root.destroy()
            if text == "start":
                captureimage()
            if text == "hi" or text == "yes":
                name1 = detect()
            if text == "login" or text == "log out" or text == "logout":
                action(text)
        except:
            #T.insert(END,"Sorry could not recognize what you said\n")
            print("Sorry could not recognize what you said")
    root.after(1000, task)  # reschedule event in 2 seconds

def printSomething():
    # if you want the button to disappear:
    # button.destroy() or button.pack_forget()
    label = Label(root, text= "Hey whatsup bro, i am doing something very interresting.")
    label.pack() 
    label = Label(root, text= "Hey whatsup bro, i am doing something very interresting.")
    #this creates a new label to the GUI
    label.pack() 

#printSomething()
root.after(1000, task)
root.mainloop()