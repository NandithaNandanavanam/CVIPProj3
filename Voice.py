import speech_recognition as sr
import pyaudio

def voice_module():
    
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak Anything :")
        audio = r.listen(source)
        try:
            text = r.recognize_google(audio)
            print("You said:"+text)
        except:
            text= "Sorry could not recognize what you said"
            
    return text
    


    
    
    
        
        
    
        