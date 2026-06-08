import pyttsx3
import speech_recognition as sr
import webbrowser
import pyjokes
import os
import datetime
import wikipedia
from googletrans import Translator
import pygame
import pyautogui

# Initialize the recognizer and the TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate",170)

# Function to convert text to speech
def speak(query):
    engine.say(query)
    engine.runAndWait()


# Function to recognize speech and convert it to text
def listen():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(f"Sorry, I did not get that. Exception: {e}")
            return "none"
        return query

def greetme():
    hour = datetime.datetime.now().hour
    if hour<=0 or hour<=12:
        speak('good morning ,sir')
    elif hour<=12 or hour<=18:
        speak('good afternoon sir')
        
    else:
        speak('good evening sir')
        
# Function to open a website
def open_website(site):
    print(f"Opening website: {site}")
    webbrowser.open(site)


# Function to tell a joke
def tell_joke():
    joke = pyjokes.get_joke()
    print(joke)
    speak(joke)

# Function to open an application
def open_application(app_name):
    print(f"Opening application: {app_name}")
    if 'notepad' in app_name:
        os.system('notepad')
    elif 'calculator' in app_name:
        os.system('calc')

def search_wikipedia(query):
    try:
        speak("Searching in Wikipedia...,sir")
        query = query.replace("search in wikipedia", "").strip()
        if query:  # Make sure the query is not empty
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        else:
            speak("Sorry, I didn't catch the topic to search.")
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Your query could refer to multiple topics. Did you mean: {e.options}?")
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find anything on Wikipedia about that.")
        if "Ok no problem" in query:
            speak("ask anithing sir")
    except Exception as e:
        speak("An error occurred while searching Wikipedia.")
        print(e)

# Set your OpenAI API key
# openai.api_key = 'YOUR_API_KEY'

# def chat_with_gpt(prompt):
#     """Send a prompt to OpenAI's GPT model and return the response."""
#     # response = openai.Completion.create(
#         engine="text-davinci-003",  # or "gpt-4" depending on your subscription
#         prompt=prompt,
#         max_tokens=150
#     )
#     return response.choices[0].text.strip()


# Function to play the song
def play_song(music):
    # Path where songs are stored
    songs_dir = 'C:\\Users\\baijn\\Music'  # Change to your songs folder path

    # List all files in the songs directory
    songs = os.listdir(songs_dir)

    # Check if the song exists in the directory
    for song in songs:
        if music in song.lower():
            print(f"Playing {song}")
            song_path = os.path.join(songs_dir, song)
            pygame.mixer.init()
            pygame.mixer.music.load(song_path)
            pygame.mixer.music.play( )

            speak(f"Playing {song}")
            while pygame.mixer.music.get_busy():  # Keep script running until the song ends
                continue

            return

    speak("Sorry, I couldn't find the song in your list.")
    print("Song not found")

# Main function
if __name__ == "__main__":
    greetme()
    speak("Hello sir i am jarvis , how can I assist you today sir?")
    while True:
        query = input("enter what you want : ")
        # query = listen().lower()
        print(f"Query received: {query}") 

        if 'exit' in query:
            speak("Goodbye!,you have a goodday sir")
            break

        elif 'youtube' in query:
            speak("Opening YouTube")
            open_website("https://www.youtube.com")

        elif 'google' in query:
            speak("opening google,sir")
            open_website("https://www.google.com")

        elif 'Wikipedia' in query:
            speak('What the topic sir')
            query = listen()
            print(f"Topic received: {query}")
            search_wikipedia(query)

        elif 'Flipkart' in query:
            speak("Opening Flipkart,sir")
            open_website("https://www.flipkart.com/")

        elif 'anime' in query:
            speak("Opening Hianime,sir")
            open_website("https://www.hianime.to/")

        elif 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")


        elif 'open code' in query:
            speak("Opening Visual Studio Code")
            codePath = "C:\\Users\\baijn\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
            os.startfile(codePath)

        elif 'shape of you' in query:
            music_dir = "C:\\Users\\baijn\\Music\\Ed Sheeran - Shape of You (Official Music Video)(MP3_320K).mp3"
            speak("playing shape of you,sir")
            # songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir))
        
        # elif 'close music' in query:
        #     os.system("taskkill /im Boom3D.exe /f")
        #     speak("closing music")

        elif "open" in query:
            app = query.replace("open ", "")
            os.system("start " + app + ".exe")
            speak("Opening " + app)

        elif "close" in query:
            app = query.replace("close ", "")
            os.system("taskkill /im " + app + ".exe /f")
            speak("Closing " + app)
            

        elif 'joke' in query:
            tell_joke()

        elif 'hello' in query:
            speak("Hello sir, how are you")

        elif 'i am fine' in query or 'I am fine' in query or 'me thik hu' in query:
            speak("That's great sir")
        
        elif 'thank you' in query:
            speak("perfact , sir")
        elif 'what is your name' in query or 'whats your name' in query:
            speak('my name is jarvis, i am in my first phase. my sir told me in future i became the most advance and denger AI in the whole world ')  
            speak('here is my sir name ')
            print('Baijanth kewat')
        elif 'again' in query:
             speak('i saying. my name is jarvis, i am in my first phase. my sir told me in future i became the most advance and dengerous AI in the whole world ')      
        elif '' in query:
            speak('')
        elif '' in query:
            speak('')
        elif '' in query:
            speak('')
        elif '' in query:
            speak('')
        
        elif 'open' in query:
            if 'Notepad' in query:
                speak("Opening Notepad")
                open_application('notepad')
            elif 'calculator' in query:
                speak("Opening Calculator")
                open_application('calculator')
            
        elif 'music' in query:
            speak("playing music,sir")
            play_song()
        
        elif 'translate' in query:
            speak('ok sir')
            
       
        else:
            speak(f"You said: {query}")
