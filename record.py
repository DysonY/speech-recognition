import sounddevice as sd
import speech_recognition as sr
import wavio
import sys

# from io import BytesIO
from os import path
from important import most_important


# Get absolute path of file in same directory
def get_path(filename):
    return path.join(path.dirname(path.realpath(__file__)), filename)


# Find a hardware-specific input device
def get_input_device():
    input_idx = sd.default.device[0]
    return sd.query_devices(input_idx)


# Callback function for generating output stream
def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata


# Recognize English (en-US) or German (de-DE) speech
def recognize_speech(filename, lang):
    r = sr.Recognizer()
    with sr.AudioFile(get_path(filename)) as source:
        audio = r.record(source)
    return r.recognize_google(audio, language=lang)


# Record for specified number of seconds
def record_audio(filename, duration):
    device = get_input_device()
    chans = device['max_input_channels']
    freq = device['default_samplerate']

    recording = sd.rec(int(duration*freq), samplerate=freq, channels=chans)
    sd.wait()
    wavio.write(filename, recording, freq, sampwidth=2)

    '''
    with sd.Stream(samplerate=44100, channels=chans, dtype='int16') as raw:
        sd.sleep(int(duration * 1000))
        data = raw.read(raw.read_available)[0]
        ostream = BytesIO(data)

        with open('temp.wav', 'wb') as f:
            f.write(ostream.read())
        ostream.close()

        try:
            print(recognize_speech(ostream, 'en-US'))
            ostream.close()
        except Exception as e:
            print(e)
            ostream.close()
    '''

def recognize_important(filename, lang):
    if lang == 'English':
        data = recognize_speech(filename, 'en-US')
    elif lang == 'German':
        data = recognize_speech(filename, 'de-DE')
    else:
        print(f'Invalid language {lang}')
        return []
    return most_important(data, lang)


if __name__  == '__main__':
    assert len(sys.argv) == 2
    assert sys.argv[1] == 'English' or sys.argv[1] == 'German'
    record_audio(60)
    print(recognize_important('_temp.wav', sys.argv[1]))


