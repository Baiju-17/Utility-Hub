import os
import queue
import sounddevice as sd
import vosk
import sys
import json

# Set up Vosk recognizer with a pre-downloaded model
model_path = "vosk-model-small-en-us-0.15"  # Change this to the path of your model
if not os.path.exists(model_path):
    print(f"Please download the model from https://alphacephei.com/vosk/models and unpack as '{model_path}' in the current folder.")
    sys.exit()

vosk.SetLogLevel(0)  # Mute logs for cleaner output
model = vosk.Model(model_path)
samplerate = 16000  # Sampling rate for sound

# Queue to hold audio data
q = queue.Queue()

# Audio callback function for sounddevice
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Recognize speech from microphone
def recognize_speech():
    # Create a Vosk recognizer
    recognizer = vosk.KaldiRecognizer(model, samplerate)

    # Start recording from the microphone
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16', channels=1, callback=callback):
        print("Listening...")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result_json = json.loads(result)
                if 'text' in result_json:
                    return result_json['text']
            else:
                partial_result = recognizer.PartialResult()
                print(f"Partial: {partial_result}")

# Example usage
if __name__ == "__main__":
    while True:
        print("Say something (or 'exit' to stop):")
        recognized_text = recognize_speech()
        print(f"You said: {recognized_text}")
        if 'exit' in recognized_text.lower():
            break
