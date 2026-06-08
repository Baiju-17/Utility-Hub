import speech_recognition as sr
import edge_tts
import asyncio
import os
import pygame
import datetime
import time

import webbrowser

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone(device_index=18) as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjust for noise
        audio = recognizer.listen(source)

    try:
        # Recognize the spoken words
        print("Recognizing...")
        command = recognizer.recognize_google(audio, language='en-IN')
        print(f"aapne kaha: {command}")
        
        return command
    except sr.UnknownValueError:
        print("Sorry sir, me thik se soon nhi paya kya aap phir se bolenege")
        return ""
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        return ""

# Function to generate speech using Edge TTS with MadhurNeural voice
async def text_to_speech(text, output_file='voices.MP3'):
    communicate = edge_tts.Communicate(text, voice="hi-IN-MadhurNeural",rate="+20%")  # Using MadhurNeural voice
    await communicate.save(output_file)
    pygame.mixer.init()
    pygame.mixer.music.load(output_file)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
      pygame.time.Clock().tick(10)
    pygame.mixer.quit() # Optional: Clean up the file after playing



def open_website(site):
    print(f"Opening website: {site}")
    webbrowser.open(site)

# Main function to control the assistant

async def jarvis():

    # pygame.mixer.init()
    # pygame.mixer.music.load('C:\\Users\\baijn\\Desktop\\JARVIS\\the_best_alarm_of_ever.mp3')
    # pygame.mixer.music.play()
    # while pygame.mixer.music.get_busy():
    #   pygame.time.Clock().tick(10)

    
    # await text_to_speech('jarvis aapke liye hazir hai sir')
    # await text_to_speech('bataiye sir mai aapke liye kya kar sakta hu')
    while True:
        
        command = recognize_speech()
        await text_to_speech(f"aapne kaha: {command}")
        if command:
            
            if 'exit' in command.lower():
                print("Exiting JARVIS...")
                await text_to_speech("thik hai Sir jaisi aapki marzi, system is now going to shutdown .")
                break
            elif 'hello' in command.lower():
                await text_to_speech("Hello sir, aap kaise he ?")
            elif 'mai theek hu' in command.lower():
                await text_to_speech('mujhe soon ke bahut khusi huwi ki swasth he')
            elif 'your name' in command.lower():
                await text_to_speech("Me JARVIS hu, aapka personal desktop assistant.")
            elif "baten batao" in command.lower():
                await text_to_speech("""Zindagi ke kuch mahatvapurn baatein jo yaad rakhni chahiye:

                                        Sakaratmak Soch (Positive Thinking): Har mushkil mein kuch seekhne ko milta hai. Negative soch ke badle, har situation ka bright side dekhne ki koshish karo.

                                        Waqt ka mahatva (Value of Time): Waqt sabse badi daulat hai. Uska sadupyog karo, bekaar mein barbad mat karo.
                                        Main aapki madad ke liye hamesha taiyaar hoon, sir!""")
            elif 'time' in command.lower():
                await text_to_speech(f"sir abhi {time.strftime('%I:%M %p')} baj rhe he ")
            elif 'date' in command.lower():
                await text_to_speech(f"aaj : {time.strftime('%d-%m-%Y')} hai")
            elif 'shape of you' in command.lower():
                # os.startfile('C:\\Users\\baijn\\Music\\Ed Sheeran - Shape of You (Official Music Video)(MP3_320K).mp3')
                pygame.init()
                pygame.mixer.init()
                pygame.mixer.music.load('C:\\Users\\baijn\\Desktop\\JARVIS\\Ed Sheeran - Shape of You (Official Music Video)(MP3_320K).mp3')
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)

            elif 'youtube' in command.lower():
                 await text_to_speech("Opening YouTube")
                 open_website("https://www.youtube.com")

            elif 'google' in command.lower():
                await text_to_speech("opening google,sir")
                open_website("https://www.google.com")

            # elif 'Wikipedia' in command.lower():
            #     await text_to_speech('What the topic sir')
            #     command.lower():= listen()
            #     print(f"Topic received: {command.lower():")
            #     search_wikipedia(command.lower():

            elif 'Flipkart' in command.lower():
                await text_to_speech("Opening Flipkart,sir")
                open_website("https://www.flipkart.com/")

            elif 'anime' in command.lower():
                await text_to_speech("Opening Hianime,sir")
                open_website("https://www.hianime.to/")
        
            else:
                # print("Asking OpenAI for a response...")
                # response = openai_chat(command)
                # print(f"OpenAI Response: {response}")
                # await text_to_speech(response)
                await text_to_speech(f"Aapne kaha: {command}")
        # else:
            # await text_to_speech("sorry sir , me thik se soon nhi paya kya aap phir se bolenge ?")

# Run the assistant
if __name__ == "__main__":
    asyncio.run(jarvis())
    
