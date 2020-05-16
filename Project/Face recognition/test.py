import face_recognition
import numpy as np
from tkinter import *
import speech_recognition as sr
import face_reg

root = Tk()
root.title("Face enabled Time clock")
root.attributes("-zoomed",True)

topframe=Frame(root)
topframe.pack(side=TOP)

bottomframe=Frame(root)
bottomframe.pack(side=BOTTOM)

leftframe=Frame(topframe,bg='black')
leftframe.pack(side=LEFT)

rightframe=Frame(bottomframe)
rightframe.pack(side=RIGHT)

canvas=Canvas(leftframe,width=600,height=200)
canvas.pack()
photo=PhotoImage(file='ub_pic.jpg')
canvas1=canvas.create_image(20,10,anchor=NW, image=photo)
leftframe.pack(side=LEFT)



def captureimage():
    img = capture.capture_image()
    cv2.imwrite("facedetected.png",img)
    
    photo=PhotoImage(file='facedetected.png')
    
    canvas.delete("all")
    canvas2 = canvas.create_image(1,1,anchor=NW, image=photo)
    canvas.itemconfig(canvas1, image = canvas2)
    canvas.pack()
    leftframe.pack(side=LEFT)
    root.after(1000, task) 

def task():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said : {}".format(text))
            if text == "stop":
                root.destroy()
            if text == "start":
                captureimage()
            if text == "detect":
                detect()
        except:
            print("Sorry could not recognize what you said")
    root.after(1000, task)  # reschedule event in 2 seconds

root.after(1000, task)
root.mainloop()