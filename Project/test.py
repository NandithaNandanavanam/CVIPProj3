from tkinter import *
import capture
import speech_recognition as sr
import numpy as np
import cv2
import face_recognition

import face_reg
import google_ocr
import ner
import os
import config
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

def detect():
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
        T.insert(END, "Welcome:{}".format(name))
        print("Welcome:{}\n".format(name))
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
    print(face_frame)
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
            if text == "no":
                detect()
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