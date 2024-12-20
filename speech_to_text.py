import speech_recognition as sr
import sounddevice as sd
import numpy as np
import sys
import send_data_to_gpt


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
    
def main():
    print("Speech-to-Text for Hebrew")
    audio = record_audio()
    transcribed_audio = transcribe_audio(audio)


if __name__ == "__main__":
    print("Speech-to-Text for Hebrew")
    audio = record_audio()
    transcribe_audio(audio)
