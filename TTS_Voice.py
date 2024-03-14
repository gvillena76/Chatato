#================CURRENT WORKING METHOD=================
import pyttsx3
engine = pyttsx3.init()
engine.setProperty("rate", 140)
voices = engine.getProperty('voices')
# engine.setProperty('voice', voices[1].id)
# engine.say("Greetings!  I am Chatato, human-cyborg relations!  What would you like to ask?'")
# engine.runAndWait()
# engine.stop()
for voice in voices:
    print(voice, voice.id)
    engine.setProperty('voice', voice.id)
    engine.say("Hello World!")
    engine.runAndWait()
    engine.stop()
#=======================================================

