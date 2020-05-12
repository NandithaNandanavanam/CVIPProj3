from tkinter import *
import cv2
import Voice
import capture
import time
import PIL
from PIL import Image,ImageTk

def verify_voice_command():
    print("Verifying")
    while True:
        label_voicetest.configure(text="Is this what you said? Say Yes or No")
        label_voicetest.place()
        
        root.update_idletasks()
        root.update()
        
        voiceverify = Voice.voice_module()
        if voiceverify=="yes":
            print("Verified")
            label_voicetest.configure(text="Speak Anything")
            label_voicetest.place()
            break
        elif voiceverify=="no":
            print("Not correct")
            label_voicetest.configure(text="Speak Anything")
            label_voicetest.place()
            break

def display_chat(voicecommand,rownum):
    rownum=rownum+1
    Label(rightframe, text=time.strftime("%H:%M:%S"), bg='white',fg='black',bd=3).grid(row=rownum,column=0,padx=5, pady=5)
    rownum=rownum+1
    Label(rightframe, text="You said : " + voicecommand, bg='white',fg='black',bd=3).grid(row=rownum,column=0,padx=5, pady=5)
    

def show_frame():
    _, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    frame = cv2.flip(frame, 1)  
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)  
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk 
    lmain.configure(image=imgtk)
        
#GUI
root = Tk() 
root.title("ClockIn/ClockOut Application") 
root.config(bg="beige") 
 
leftframe = Frame(root, width=200, height=400, bg='beige')
leftframe.grid(row=0, column=0, padx=10, pady=5)
rightframe = Frame(root, width=650, height=400, bg='beige')
rightframe.grid(row=0, column=1, padx=10, pady=5)

label_voice = Label(leftframe,text="")
label_voice.grid(row=5,column=0, padx=5, pady=5)

label_voicetest = Label(leftframe,text="Speak Anything",bg="lightgrey")
label_voicetest.grid(row=4,column=0, padx=5, pady=5)

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

cap = cv2.VideoCapture(0)
while True:
    root.update_idletasks()
    root.update()
     
    lmain=Label(leftframe)
    lmain.grid(row=0,column=0, padx=5, pady=5)
    
    root.update_idletasks()
    root.update()
   
    show_frame()

    root.update_idletasks()
    root.update()

    Label(leftframe, text="Welcome to the Touch less Face enabled Clock In/Clock Out System. Say LOGIN to Clock In, EXIT to close", bg='lightgrey',bd=10).grid(row=1, column=0, padx=5, pady=5)

    Label(rightframe, text="Chat with the System", bg='lightgrey',fg='black',bd=3).grid(row=0,column=0,padx=5, pady=5) 
    Label(rightframe, text=time.strftime("%H:%M:%S"), bg='lightgrey',fg='black',bd=3).grid(row=1,column=0,padx=5, pady=5)
    Label(rightframe, text="System: Hello, What do you want to do?", bg='lightgrey',fg='black',bd=3).grid(row=2,column=0,padx=5, pady=5)
    
    root.update_idletasks()
    root.update()
    
    voicecommand = Voice.voice_module()
    label_voice.configure(text="You said : " + voicecommand)
    label_voice.place()
    
    root.update_idletasks()
    root.update()
    
    verify_voice_command()
    
    rownum=2
    display_chat(voicecommand,rownum)
    
    if voicecommand=="login":
        Label(rightframe, text=time.strftime("%H:%M:%S"), bg='lightgrey',fg='black',bd=3).grid(row=5,column=0,padx=5, pady=5)
        Label(rightframe, text="Okay!Look at the camera", bg='lightgrey',fg='black',bd=3).grid(row=6,column=0,padx=5, pady=5)
        
        cv2.imwrite("face1.png",frame)
        
        root.update_idletasks()
        root.update()
    
    elif voicecommand=="exit":
        break
    else:
        continue
   

    
    
    
    
  






       




    
