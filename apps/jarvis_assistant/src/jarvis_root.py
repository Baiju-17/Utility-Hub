import pyttsx3
import speech_recognition as sr
import webbrowser
import pyjokes
import os
import datetime
import wikipedia
import pygame
import pyautogui
import subprocess

# Initialize the recognizer and the TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 170)

# Function to convert text to speech
def speak(text):
    print(f"Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech and convert it to text
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
            return query.lower()
        except Exception as e:
            # speak("I didn't catch that, sir.")
            return "none"

def greetme():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak('Good morning, sir.')
    elif 12 <= hour < 18:
        speak('Good afternoon, sir.')
    else:
        speak('Good evening, sir.')

def chat_with_gemini(prompt):
    """Use Gemini CLI to get a response for complex queries."""
    try:
        # Using the full path to gemini.cmd and shell=True for Windows
        gemini_path = r'C:\Users\baijn\AppData\Roaming\npm\gemini.cmd'
        process = subprocess.Popen(
            [gemini_path, '--prompt', prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            shell=True
        )
        stdout, stderr = process.communicate(timeout=30)
        
        # Filter out the header/footer noise if any, or just take the main response
        # Most of the time the last few lines contain the answer
        lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        
        # Simple heuristic: find the part after the prompt or just return the last significant block
        if lines:
            # Often the output has a lot of terminal formatting. 
            # We'll try to find the actual response part.
            # For now, let's take the last few lines that aren't metadata.
            response = " ".join(lines[-5:]) # Fallback
            # Better: strip common headers
            clean_lines = [l for l in lines if "Gemini CLI" not in l and "Signed in" not in l and "Plan:" not in l]
            if clean_lines:
                return " ".join(clean_lines)
        return "I am having trouble connecting to my brain, sir."
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "I encountered an error while thinking, sir."

def open_application(app_name):
    """Dynamically try to open applications."""
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "chrome.exe",
        "code": "code",
        "edge": "msedge.exe"
    }
    
    executable = apps.get(app_name.lower())
    if executable:
        speak(f"Opening {app_name}")
        os.system(f"start {executable}")
    else:
        # Fallback to general system start
        speak(f"Attempting to open {app_name}")
        os.system(f"start {app_name}")

# Main function
if __name__ == "__main__":
    greetme()
    speak("Jarvis is online. How can I assist you today, sir?")
    
    while True:
        # Toggle between voice and input for testing
        # query = input("Enter command (or type 'voice'): ").lower()
        # if query == 'voice':
        #     query = listen()
        
        query = listen()
        if query == "none":
            continue

        print(f"Query received: {query}")

        if 'exit' in query or 'stop' in query:
            speak("Goodbye! Have a great day, sir.")
            break

        elif 'youtube' in query:
            speak("Opening YouTube")
            webbrowser.open("https://www.youtube.com")

        elif 'google' in query:
            speak("Opening Google, sir")
            webbrowser.open("https://www.google.com")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"Sir, the time is {strTime}")

        elif 'open' in query:
            app = query.replace("open ", "").strip()
            open_application(app)

        elif 'joke' in query:
            speak(pyjokes.get_joke())

        elif 'who are you' in query or 'your name' in query:
            speak("I am Jarvis, your personal AI assistant. I am currently in Phase 2, powered by Gemini.")

        else:
            # Use Gemini for everything else!
            speak("Let me think...")
            response = chat_with_gemini(query)
            speak(response)
