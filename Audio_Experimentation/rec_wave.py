import sounddevice as sd
import soundfile as sf
import sys
import os
import argparse


def get_real_time_audio():
  fs = 16000
  channels = 1
  duration = 5
  filename = "recorded.wav"
  print("please play the audio!")
  myrec = sd.rec(int(duration  *fs), samplerate=fs, channels=channels)
  sd.wait()
  sf.write(filename, myrec,samplerate=fs)
  play_rec = sd.playrec(myrec, fs, channels=2)
  sd.wait()
  print("Done!")



