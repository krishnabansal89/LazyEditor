# from librosa import *
# import matplotlib.pyplot as plt


# # Load the audio file
# audio , sr = load('./audio/beats.mp3')

# plt.figure(figsize=(14, 5))

# display.waveshow(audio, sr=sr)
# plt.title('Audio Waveform')
# plt.show()
from librosa import *
import matplotlib.pylab as plt
import librosa.display
import pandas as pd

# Load the audio file
# audio, sr = load('./audio/beats.mp3')
# print(audio.shape)
# pd.Series(audio).plot(figsize=(14, 5))
# plt.figure(figsize=(14, 5))



# import matplotlib.pyplot as plt
y, sr = load('./audio/beats.mp3' , sr=None)
display.waveshow(y, sr=sr, label="test")
# librosa.display.waveshow(audio, sr=sr)
# plt.title('Audio Waveform')
# plt.show()
