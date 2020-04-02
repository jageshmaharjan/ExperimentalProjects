import pyaudio
import wave
import time
import os, sys


audio_file = "/home/jugs/Desktop/p257_430.wav"
wf = wave.open(audio_file, 'rb')

p = pyaudio.PyAudio()


def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)


stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                stream_callback=callback
                )

# data = wf.readframes(1024)
stream.start_stream()

# while len(data):
#     stream.write(data)
#     data = wf.readframes(1024)
while stream.is_active():
    time.sleep(0.1)

stream.stop_stream()
stream.close()
wf.close()

p.terminate()