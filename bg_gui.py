from tkinter import *
import tkinter.filedialog as fdialog
import cv2
import Voice
import capture
import speech_recognition as sr

def browseimage():
    filename = fdialog.askopenfilename()
    img = cv2.imread(filename)
    img=cv2.resize(img,(350,350))
    cv2.imwrite('face.png',img)
    photo=PhotoImage(file='face.png')
    
    canvas.delete("all")
    canvas2 = canvas.create_image(1,1,anchor=NW, image=photo)
    canvas.itemconfig(canvas1, image = canvas2)
    canvas.pack()
    leftframe.pack(side=LEFT)
    root.mainloop()
    
def voicemodule():
    voicecommand, error = Voice.voice_module()
    if error ==0:
        label1 = Label(rightframe, text="You said : " + voicecommand)
    else:
        label1 = Label(rightframe, text=voicecommand)

    label1.pack()
    rightframe.pack(side=RIGHT)
    root.mainloop()

    
def captureimage():
    img = capture.capture_image()
    cv2.imwrite("facedetected.png",img)
    
    photo=PhotoImage(file='facedetected.png')
    
    canvas.delete("all")
    canvas2 = canvas.create_image(1,1,anchor=NW, image=photo)
    canvas.itemconfig(canvas1, image = canvas2)
    canvas.pack()
    leftframe.pack(side=LEFT)
    root.mainloop()
    
#GUI
#Create window
root = Tk()
root.title("Face enabled Time clock")
root.attributes("-zoomed",True)

f = open("nohup.out", "r")
print(f.read().split().pop())
test = "dsf"
print(test)
#Create topframe, bottomframe, leftframe and rightframe
topframe=Frame(root)
topframe.pack(side=TOP)

bottomframe=Frame(root)
bottomframe.pack(side=BOTTOM)

leftframe=Frame(topframe,bg='black')
leftframe.pack(side=LEFT)

rightframe=Frame(bottomframe)
rightframe.pack(side=RIGHT)

canvas=Canvas(leftframe,width=500,height=400)
canvas.pack()
photo=PhotoImage(file='gecap.png')
canvas1=canvas.create_image(20,10,anchor=NW, image=photo)
leftframe.pack(side=LEFT)
    
#buttons
Bt1=Button(rightframe,text="Capture Image",background="LightBlue", bd=0,width=15,height=1,command=captureimage)
Bt1.pack(fill=X,pady=10)

Bt2=Button(rightframe,text="Capture Voice",background="LightBlue", bd=0,width=15,height=1,command=voicemodule)
Bt2.pack(fill=X,pady=10)

Bt3=Button(rightframe,text="Exit",background="LightBlue", bd=0,width=15,height=1,command=root.destroy)
Bt3.pack(fill=X,pady=10)

rightframe.pack(side=RIGHT)


#stable main window on infinity time
root.mainloop()

       




    