import speech_recognition as sr
import sounddevice as sd
import numpy as np
import sys
import backend.src.send_data_to_gpt as send_data_to_gpt
import backend.src.compare_to_other_cases as compare_to_other_cases
import json
import ffmpeg


# Set console to UTF-8 mode for Hebrew text
sys.stdout.reconfigure(encoding='utf-8')

def record_audio(duration=5, samplerate=44100):
    print("Recording... Speak now!")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
    sd.wait()  # Wait until the recording is complete
    print("Recording complete.")
    return np.squeeze(audio_data)

def transcribe_audio(audio, samplerate=44100, language="he-IL"):
    recognizer = sr.Recognizer()
    # Convert the numpy array to raw PCM data
    audio_data = audio.astype(np.int16).tobytes()
    # Calculate sample width from dtype
    sample_width = audio.dtype.itemsize
    
    audio_source = sr.AudioData(audio_data, samplerate, sample_width)
    try:
        print("Processing audio...")
        text = recognizer.recognize_google(audio_source, language=language)
        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand the audio.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    
def convert_to_pcm(file_path, output_sample_rate=44100):
    # Use ffmpeg to extract PCM raw data
    process = (
        ffmpeg.input(file_path)
        .output('pipe:', format='s16le', acodec='pcm_s16le', ac=1, ar=output_sample_rate)
        .run(capture_stdout=True, capture_stderr=True)
    )
    raw_audio = process[0]  # Captured stdout is the raw audio
    pcm_data = np.frombuffer(raw_audio, dtype=np.int16)
    return pcm_data, output_sample_rate
    
# def is_button_pressed():
#     #TODO: Implement button press detection
#     return True  # Placeholder for actual button press detection
    
# def main():
#     our_json = {}
    
#     while is_button_pressed():
#         print("Speech-to-Text for Hebrew")
#         audio = record_audio()
#         transcribed_audio = transcribe_audio(audio)
#         response = send_data_to_gpt.chat_with_gpt(transcribed_audio)
#         json_response = json.loads(response)
#         for key, value in json_response.items():                        #items is a method that returns a view object. The view object contains the key-value pairs of the dictionary, as tuples in a list.
#             if key not in our_json:
#                 our_json[key] = value
#         print(f"ChatGPT says:\n{response}")                             # just for testing
#         compare_to_other_cases.compare(our_json)
    


if __name__ == "__main__":
    # main()
    pass
