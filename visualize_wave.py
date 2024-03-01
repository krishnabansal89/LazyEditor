# from librosa import *
# import matplotlib.pyplot as plt


# # Load the audio file
# audio , sr = load('./audio/beats.mp3')

# plt.figure(figsize=(14, 5))

# display.waveshow(audio, sr=sr)
# plt.title('Audio Waveform')
# plt.show()
from librosa import *
import matplotlib.pyplot as plt
import librosa.display

# Load the audio file
audio, sr = load('./audio/beats.mp3')

plt.figure(figsize=(14, 5))

librosa.display.waveshow(audio, sr=sr)
plt.title('Audio Waveform')
plt.show()
