import cv2 , os 
from moviepy.editor import *
import librosa

#Loading the images
images = [img for img in os.listdir("./images/") if img.endswith(".png") or img.endswith(".jpg")]
# frame = cv2.imread(os.path.join("./images/", images[0]))


#loading the audio
y , s  = librosa.load('./audio/beats.mp3')
beat_frames = librosa.onset.onset_detect(y=y, sr=s)
beat_times = librosa.frames_to_time(beat_frames, sr=s)
beat_times = [beat_times[i] for i in range(0,len(beat_times),4) ]
beat_times = beat_times[:len(images)]
beat_times = [0] + list(beat_times)
audio_clip = AudioFileClip('./audio/beats.mp3')
cut_audio = audio_clip.subclip(0.00,beat_times[-1] )
print(beat_times)
clips =[]
for i in range(len(images)):
    image = cv2.imread(os.path.join("./images/", images[i]))
    print(beat_times[i+1] - beat_times[i])
    clip = ImageClip(image).set_duration(beat_times[i+1] - beat_times[i])
    clips.append(clip)


#for adding Transition in between the images
# for i in range(len(clips) - 1):
#     transition = CompositeVideoClip([clips[i].crossfadeout(1), clips[i+1].crossfadein(1)]).set_duration(1)
#     clips[i] = concatenate_videoclips([clips[i], transition])



video = concatenate_videoclips(clips, method="compose")
audio = AudioFileClip('./audio/beats.mp3').subclip(0,beat_times[-1])
video = video.set_audio(audio)
video.write_videofile("my_concatet.mp4", fps=24)
