import speech_recognition as sr
import edge_tts
import asyncio
import os
import pygame
import time
import webbrowser

pygame.mixer.init()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-IN')
        print(f"Aapne kaha: {command}")
        return command
    except sr.UnknownValueError:
        print("Sorry sir, main thik se sun nahi paya.")
        return ""
    except sr.RequestError as e:
        print(f"Speech Recognition error: {e}")
        return ""

async def text_to_speech(text, output_file='voice.mp3'):
    if not text.strip():
        return
    communicate = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural", rate="+20%")
    await communicate.save(output_file)
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def open_website(site):
    print(f"Opening website: {site}")
    webbrowser.open(site)

async def jarvis():
    await text_to_speech("Jarvis aapke liye hazir hai sir.")
    while True:
        command = recognize_speech()
        if not command:
            continue

        if 'exit' in command.lower():
            print("Exiting JARVIS...")
            await text_to_speech("Thik hai sir, system band ho raha hai.")
            break

        elif 'hello' in command.lower():
            await text_to_speech("Hello sir, aap kaise hain?")

        elif 'mai theek hu' in command.lower():
            await text_to_speech("Mujhe sunkar khushi hui ki aap swasth hain.")

        elif 'your name' in command.lower():
            await text_to_speech("Main Jarvis hoon, aapka personal desktop assistant.")

        elif 'baten batao' in command.lower():
            await text_to_speech("Zindagi me sakaratmak soch rakhna aur samay ka sadupyog karna sabse zaroori hai.")

        elif 'time' in command.lower():
            await text_to_speech(f"Sir, abhi {time.strftime('%I:%M %p')} baj rahe hain.")

        elif 'date' in command.lower():
            await text_to_speech(f"Aaj {time.strftime('%d-%m-%Y')} hai.")

        elif 'shape of you' in command.lower():
            try:
                pygame.mixer.music.load(r"C:\Users\baijn\Desktop\JARVIS\Ed Sheeran - Shape of You (Official Music Video)(MP3_320K).mp3")
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
            except Exception as e:
                print("Music file error:", e)

        elif 'youtube' in command.lower():
            await text_to_speech("Opening YouTube.")
            open_website("https://www.youtube.com")

        elif 'google' in command.lower():
            await text_to_speech("Opening Google.")
            open_website("https://www.google.com")

        elif 'flipkart' in command.lower():
            await text_to_speech("Opening Flipkart.")
            open_website("https://www.flipkart.com")

        elif 'anime' in command.lower():
            await text_to_speech("Opening Hianime.")
            open_website("https://www.hianime.to")

        else:
            await text_to_speech(f"Aapne kaha: {command}")

if __name__ == "__main__":
    asyncio.run(jarvis())
