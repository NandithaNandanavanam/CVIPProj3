import speech_recognition as sr
import pyaudio

def voice_module():
    err = 0
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
        except:
            text= "Sorry could not recognize what you said"
            err = 1
    return text,err
