import pyttsx3
import datetime
import os
import sounddevice as sd
import queue
import vosk
import json

# Text-to-Speech Engine Setup
engine = pyttsx3.init("sapi5")
engine.setProperty("rate", 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

# Vosk Model Load करें (इसे डाउनलोड करके path दें)
model_path = "vosk-model-small-en-us-0.15"  # Change to your model path
model = vosk.Model(model_path)

# Audio Queue Setup
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, flush=True)
    q.put(bytes(indata))

def command():
    with sd.RawInputStream(samplerate=44100, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 44100)
        print("Listening...")

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                query = result["text"]
                print(f"You said: {query}")
                return query.lower()
    return "none"

if __name__ == "__main__":
    while True:
        # speak("Hello sir,")
        text = command()

        if text != "none":
            print(f"Query received: {text}\n")
            speak(f"You said: {text}")

        elif text == "the time":
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"Sir, the time is {strTime}")

        elif "play music" in text:
            music_dir = "C:\\Users\\baijn\\Music"
            songs = os.listdir(music_dir)
            os.startfile(os.path.join(music_dir, songs[1]))

        else:
            print("No valid query received.")

