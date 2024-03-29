import cv2
import os
from moviepy.editor import *
import librosa
import numpy as np

# Loading the images
images = [img for img in os.listdir("./images/") if img.endswith(".png") or img.endswith(".jpg")]
videos = [vid for vid in os.listdir("./videos/") if vid.endswith(".mp4") or vid.endswith(".avi")]

# Loading the audio
y, sr = librosa.load('./audio/beats.mp3')
S, phase = librosa.magphase(librosa.stft(y))
rms = librosa.feature.rms(S=S)
threshold = rms.std()  # Adjust this threshold value as needed

# Detecting beats
beat_frames = librosa.onset.onset_detect(y=y, sr=sr, backtrack=True)
filtered_onsets = [onset_frame for onset_frame, intensity_at_onset in zip(beat_frames, rms[0, beat_frames])
                   if intensity_at_onset > threshold]
filtered_onset_times = librosa.frames_to_time(filtered_onsets, sr=sr)

# Calculating time gaps between beats
time_gaps = [filtered_onset_times[i + 1] - filtered_onset_times[i] for i in range(len(filtered_onset_times) - 1)]

# Sorting time gaps from largest to smallest
time_gaps.sort(reverse=True)

# Creating clips
clips = []
image_index = 0
video_index = 0

for gap in time_gaps:
    if video_index >= len(videos) and image_index >= len(images):
        break
    if videos and gap >= VideoFileClip(os.path.join("./videos/", videos[video_index])).duration:
        video = VideoFileClip(os.path.join("./videos/", videos[video_index]))
        clip = video.set_duration(gap)
        video_index += 1
    else:
        image = cv2.imread(os.path.join("./images/", images[image_index]))
        clip = ImageClip(image).set_duration(gap)
        image_index += 1

    clips.append(clip)

    

# Concatenating clips
video = concatenate_videoclips(clips, method="compose")
audio = AudioFileClip('./audio/beats.mp3').subclip(0, video.duration)
video = video.set_audio(audio)
video.write_videofile("my_concatet_2.mp4", fps=24)