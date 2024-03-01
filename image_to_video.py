import cv2 , os 
from moviepy.editor import *
import librosa
import numpy as np

#Loading the images
images = [img for img in os.listdir("./images/") if img.endswith(".png") or img.endswith(".jpg")]
# frame = cv2.imread(os.path.join("./images/", images[0]))


#loading the audio
y , s  = librosa.load('./audio/beats.mp3')

S, phase = librosa.magphase(librosa.stft(y))
rms = librosa.feature.rms(S=S)

stft = librosa.stft(y)
stft_magnitude = np.abs(stft)  

threshold = 0.05  # Adjust this threshold value as needed

# Assuming you've calculated either 'rms' or 'stft_magnitude'





beat_frames = librosa.onset.onset_detect(y=y, sr=s , backtrack=True)
beat_times = librosa.frames_to_time(beat_frames, sr=s)
# beat_strength = librosa.onset.onset_strength(y=y, sr=s)
beat_times = [beat_times[i] for i in range(0,len(beat_times),3) ]
beat_times = beat_times[:len(images)]
beat_times = list(beat_times)
audio_clip = AudioFileClip('./audio/beats.mp3')
cut_audio = audio_clip.subclip(0.00,beat_times[-1] )

filtered_onsets = []
for i, onset_frame in enumerate(beat_frames):
    intensity_at_onset = rms[0, onset_frame]  # Assuming you used RMS
    if intensity_at_onset > threshold:
        filtered_onsets.append(onset_frame)

# Convert back to time if needed
filtered_onset_times = [0] + list(librosa.frames_to_time(filtered_onsets, sr=s))


print(filtered_onset_times)
clips =[]
c = 0
for i in range(len(images)):
    image = cv2.imread(os.path.join("./images/", images[c]))
    for j in range(i , len(filtered_onset_times) - 1):
        if filtered_onset_times[i] + 0.1  < filtered_onset_times[j]:
            clip = ImageClip(image).set_duration(filtered_onset_times[j] - filtered_onset_times[i])
            print("j ",j)
            clips.append(clip)
            print("cc ",c)
            c+=1
            break
    # if filtered_onset_times[i] +1 < filtered_onset_times[i+1]:
    #     clip = ImageClip(image).set_duration(filtered_onset_times[i+1] - filtered_onset_times[i])
    #     print("i ",i)
    #     clips.append(clip)
    #     print("cc ",c)
    #     c+=1
   

# print(beat_strength)

#for adding Transition in between the images
# for i in range(len(clips) - 1):
#     transition = CompositeVideoClip([clips[i].crossfadeout(1), clips[i+1].crossfadein(1)]).set_duration(1)
#     clips[i] = concatenate_videoclips([clips[i], transition])
fade_duration = 0.1  # 1-second fade-in for each clip
clips = [clip.crossfadein(fade_duration) for clip in clips]
clips = [clip.crossfadeout(fade_duration) for clip in clips]



video = concatenate_videoclips(clips, method="compose" )
audio = AudioFileClip('./audio/beats.mp3').subclip(0,video.duration)
video = video.set_audio(audio)
video.write_videofile("my_concatet.mp4", fps=24)
