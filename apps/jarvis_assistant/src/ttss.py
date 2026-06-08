import speech_recognition as sr
import pyttsx3

recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty("rate", 170)

def speak(query):
    engine.say(query)
    engine.runAndWait()

def listen():
    with sr.Microphone(sample_rate=44100, chunk_size=1024) as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1,)
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-in')
            print(f"User said: {query}\n")
        except Exception as e:
            print(f"Sorry, I did not get that. Exception: {e}")
            return "none"
        return query
    
if __name__ == "__main__":
    while True:
        command = listen()
        speak(f'''You said: {command}''') 
        if command.lower() == "exit":
            print("Exiting...")
            break
        