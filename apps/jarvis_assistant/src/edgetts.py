import edge_tts
import asyncio

async def text_to_speech(text, output_file, voice="hi-IN-MadhurNeural", rate="+20%", volume="+100%"):
    communicate = edge_tts.Communicate(text=text, voice=voice, rate=rate, volume=volume)
    
    # Convert text to speech and save to the output file
    await communicate.save(output_file)
    print(f'speech has been saved to your{output_file}')
text = 'hello sir'
output_file = "voice.MP3"
asyncio.run(text_to_speech(text , output_file))