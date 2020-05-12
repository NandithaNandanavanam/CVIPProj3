from tkinter import *
import tkinter.filedialog as fdialog
import cv2
import Voice
import capture
import time

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
    
def captureimage():
    img = capture.capture_image()
    cv2.imwrite("facedetected.png",img)
    
    photo=PhotoImage(file='facedetected.png')
    
    canvas.delete("all")
    canvas2 = canvas.create_image(1,1,anchor=NW, image=photo)
    canvas.itemconfig(canvas1, image = canvas2)
    canvas.pack()
    root.pack(side=LEFT)
       
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

label_voicetest = Label(leftframe,text="Speak Anything",bg="beige")
label_voicetest.grid(row=4,column=0, padx=5, pady=5)
 
while True:
    root.update_idletasks()
    root.update()
     
    image = PhotoImage(file="gecap.PNG") 
    image = image.subsample(3,3)
    Label(leftframe, image=image).grid(row=0,column=0, padx=5, pady=5)
    Label(leftframe, text="Welcome to the Touch less Face enabled Clock In/Clock Out System. Say LOGIN to Clock In, EXIT to close", bg='beige',bd=3).grid(row=1, column=0, padx=5, pady=5)

    root.update_idletasks()
    root.update()
    
    Label(rightframe, text="Chat with the System", bg='beige',fg='black',bd=3).grid(row=0,column=0,padx=5, pady=5) 
    Label(rightframe, text=time.strftime("%H:%M:%S"), bg='beige',fg='black',bd=3).grid(row=1,column=0,padx=5, pady=5)
    Label(rightframe, text="System: Hello, What do you want to do?", bg='beige',fg='black',bd=3).grid(row=2,column=0,padx=5, pady=5)
    
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
        Label(rightframe, text=time.strftime("%H:%M:%S"), bg='white',fg='black',bd=3).grid(row=5,column=0,padx=5, pady=5)
        Label(rightframe, text="Okay!Look at the camera", bg='white',fg='black',bd=3).grid(row=6,column=0,padx=5, pady=5)
    elif voicecommand=="exit":
        break
    else:
        continue
   
   
  
    
    
    
    
  






       




    
