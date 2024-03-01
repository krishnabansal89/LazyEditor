import librosa

#the librosa.load function takes sr(sample rate) as an argument. Set it to None for default sample rate of the audio
#It defaults to 22.5kHz if no argument is passed. 
#res-type = resample type. Set it to kaiser_best if audio resolution is too low or too many prominent beats are missed.
 
audio_file, sample_rate = librosa.load('./audio/beat2.mp3', sr=None, res_type = 'kaiser_fast')
oenv = librosa.onset.onset_strength(y = audio_file, sr=sample_rate)
tempo, beat_frames = librosa.beat.beat_track(onset_envelope=oenv, sr=sample_rate)
beat_time = librosa.frames_to_time(beat_frames,sr=sample_rate)
timestamps = []
beat_strengths = oenv[beat_frames]
for i in range(0, len(beat_frames)) :
    if beat_strengths[i] > 3 :     #6.8475 is a tried and tested threshold for now. Working on an algo
        timestamps.append(beat_time[i]) #to find an accurate threshold for different songs.
with open('tempo.txt', 'w') as f:
    for timestamp in timestamps :
        f.writelines(f'{timestamp:.3f}\n')