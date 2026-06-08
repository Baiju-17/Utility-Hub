import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os


# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.setProperty('rate', 170)

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet the user
def greetMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 12:
        speak("Good Morning!,sir")
    elif hour >= 12 and hour < 18:
        speak("Good Afternoon!,sir")
    else:
        speak("Good Evening!,sir")

    speak("I am Jarvis. How can I assist you today sir")

# Function to take voice commands from the user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You said: {query}\n")
        return query.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not get that.")
        # speak("Sorry, I did not get that. Please say that again.")
        return "none"
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        # speak(f"Could not request results; {e}")
        return "none"


# Main function
if __name__ == "__main__":
    greetMe()
    while True:
        query = takeCommand().lower()

        if "wikipedia" in query:
            speak("Searching Wikipedia...")
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif "open youtube" in query:
            print("opening youtube , sir ")
            speak("opening youtube , sir ")
            webbrowser.open("youtube.com")

        elif "open google" in query:
            webbrowser.open("google.com")

        elif "the time" in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif "open code" in query:
            codePath = "C:\\Path\\To\\Your\\VSCode\\Installation"
            os.startfile(codePath)

        elif "exit" in query or "stop" in query:
            speak("Goodbye Sir!")
            break
