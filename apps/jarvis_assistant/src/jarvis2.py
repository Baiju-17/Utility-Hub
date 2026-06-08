import pyttsx3
import speech_recognition as sr
import os 

# Initialize the text-to-speech engine
engine = pyttsx3.init("sapi5")
voices = engine.getProperty("voices")
engine.setProperty("rate", 170)
engine.setProperty("voice", voices[0].id)


def speak(audio):
    """Convert text to speech."""
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    """Listen for a voice command and recognize the speech."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source,0,4)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
    except Exception as e:
        print("say that again")
        return "None"
    return query
   

if __name__ == "__main__":
    speak("Hello sir")
    while True:
        
        query = takeCommand().lower()
        if "jarvis" in query:
           from j_greetme import greetme
           greetme()
           
        #    while True:
                # query = takeCommand().lower()
        elif "sleep" in query:
            print(f"Query received: {query}\n")
            speak("OK sir, you can call me anytime")
            break
        elif "exit" in query:
            speak("Ok sir, you have a goodday")
            exit()
        elif "hello" in query:
            speak("Hello sir, how are you")

                # elif "i am fine" in query:
                #     speak("That's great sir")

        elif "how are you" in query:
            speak("perfact , sir")

        elif "thank you" in query:
            speak ("welcome sir")

        # elif "google" in query:
        #     from j_search import searchGoogle
        #     searchGoogle(query)
        #     speak()
                    
        # elif "Youtube" in query:
        #     from j_search import searchyoutube
        #     searchyoutube(query)
            
        # elif "Wikipedia" in query:
        #     from j_search import searchWikipedia
        #     searchWikipedia(query)
                