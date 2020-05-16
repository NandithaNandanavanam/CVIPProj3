import speech_recognition as sr
while True:
    r = sr.Recognizer()
    with sr.Microphone() as source:
        #print("Speak Anything :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print(text)
            #print("You said : {}".format(text))
        except:
            #print("Sorry could not recognize what you said")
            print(0)