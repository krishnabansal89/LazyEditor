import librosa
import matplotlib.pyplot as plt

# Load the audio file
y , s  = librosa.load('./audio/beats.mp3')

# Extract tempo and beat frames
tempo, beat_frames = librosa.beat.beat_track(y=y, sr=s)
beat_times = librosa.frames_to_time(beat_frames, sr=s)


onset_frames = librosa.onset.onset_detect(y=y, sr=s)
onset_times = librosa.frames_to_time(onset_frames, sr=s)

librosa.display.waveshow(y, sr=s)
plt.plot(beat_times,  marker='o', color='red') 
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.title('Audio Waveform with Beat Markers')
plt.show()

# Print the results
print('Tempo:', onset_times)
print('Beat frames:', beat_times)
