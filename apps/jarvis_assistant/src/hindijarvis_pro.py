import speech_recognition as sr
import edge_tts
import asyncio
import os
import pygame
import time
import webbrowser
import subprocess

# --- Configuration ---
GEMINI_PATH = r'C:\Users\baijn\AppData\Roaming\npm\gemini.cmd'
VOICE = "hi-IN-MadhurNeural" # Madhur sounds great for Hinglish too
TEMP_AUDIO = "jarvis_voice_pro.mp3"

# Initialize Pygame Mixer once at start
pygame.mixer.init()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening (Main sun raha hoon)...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing (Samajh raha hoon)...")
        # Language hi-IN handles Hinglish quite well
        command = recognizer.recognize_google(audio, language='hi-IN')
        print(f"User: {command}")
        return command
    except sr.UnknownValueError:
        return ""
    except sr.RequestError:
        print("Network error.")
        return ""

# Function to generate speech using Edge TTS
async def text_to_speech(text):
    if not text:
        return
    
    print(f"Jarvis: {text}")
    communicate = edge_tts.Communicate(text, voice=VOICE, rate="+20%")
    await communicate.save(TEMP_AUDIO)
    
    pygame.mixer.music.load(TEMP_AUDIO)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()

async def chat_with_gemini_hinglish(prompt):
    """Fetch Hinglish responses from Gemini."""
    try:
        # Prompt for Hinglish (English words mixed with Hindi)
        full_prompt = f"Please respond to this in Hinglish (Mix of Hindi and English), keep it short and friendly: {prompt}"
        
        process = subprocess.Popen(
            [GEMINI_PATH, '--prompt', full_prompt],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            shell=True
        )
        stdout, _ = process.communicate(timeout=25)
        
        lines = [l.strip() for l in stdout.split('\n') if l.strip()]
        clean_lines = [l for l in lines if "Gemini CLI" not in l and "Signed in" not in l and "Plan:" not in l and ">" not in l]
        
        if clean_lines:
            return " ".join(clean_lines)
        return "Sorry sir, main thoda confuse ho gaya. Please repeat kijiye."
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "Sir, brain connection mein issue hai. Check kijiye."

async def jarvis():
    await text_to_speech("Greeting sir, I'm here! Bataiye aapne mujhe kaise yaad kiya?")
    
    while True:
        command = recognize_speech()
        
        if not command:
            continue

        command_lower = command.lower()

        # Exit
        if any(word in command_lower for word in ['exit', 'stop', 'bye', 'shatdown', 'band karo']):
            await text_to_speech("Okay sir, system is shutting down. Have a good day!")
            break
            
        # Basic Greetings
        elif any(word in command_lower for word in ['hello', 'hi', 'namaste', 'kaise ho']):
            await text_to_speech("Hello sir! Main bilkul fine hoon. Aap kaise hain?")

        # Time
        elif any(word in command_lower for word in ['time', 'waqt', 'samay']):
            strTime = time.strftime('%I:%M %p')
            await text_to_speech(f"Sir, right now time is {strTime}.")

        # Camera Commands
        elif 'open' in command_lower and 'camera' in command_lower:
            await text_to_speech("Sure sir, opening the camera for you.")
            os.system("start microsoft.windows.camera:")

        elif 'close' in command_lower and 'camera' in command_lower:
            await text_to_speech("Closing camera right away, sir.")
            os.system("taskkill /f /im WindowsCamera.exe")

        # Automation
        elif 'youtube' in command_lower:
            await text_to_speech("Sure sir, YouTube open kar raha hoon.")
            webbrowser.open("https://www.youtube.com")

        elif 'google' in command_lower:
            await text_to_speech("Okay sir, Google is opening.")
            webbrowser.open("https://www.google.com")

        elif 'khola' in command_lower or 'kholo' in command_lower or 'open' in command_lower:
            app = command_lower.replace("kholo", "").replace("khola", "").replace("open", "").strip()
            await text_to_speech(f"Yes sir, {app} open ho raha hai.")
            os.system(f"start {app}")

        # Gemini Brain (Hinglish)
        else:
            await text_to_speech("Ek minute sir, main soch kar batata hoon...")
            response = await chat_with_gemini_hinglish(command)
            await text_to_speech(response)

if __name__ == "__main__":
    try:
        asyncio.run(jarvis())
    except KeyboardInterrupt:
        print("Jarvis stopped.")
    finally:
        pygame.mixer.quit()
        if os.path.exists(TEMP_AUDIO):
            try:
                os.remove(TEMP_AUDIO)
            except:
                pass
