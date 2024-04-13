
# from moviepy.video.fx import 

#Loading the images

# frame = cv2.imread(os.path.join("./images/", images[0]))


#loading the audio
 # Adjust this threshold value as needed

# Assuming you've calculated either 'rms' or 'stft_magnitude'

def distort(get_frame, t):
    import numpy as np
    """
    This function creates a zoom in effect by cropping the frame
    and resizing it to the original dimensions.
    """
    frame = get_frame(t)
    height, width, _ = frame.shape

    # Calculate the zoom factor based on time
    zoom_factor = 1 + (1 - t / 1)

    # Calculate the new dimensions for the cropped frame
    new_height = int(height / zoom_factor)
    new_width = int(width / zoom_factor)

    # Calculate the top-left corner for the cropped region
    top = int((height - new_height) / 2)
    left = int((width - new_width) / 2)

    # Crop and resize the frame
    cropped_frame = frame[top:top+new_height, left:left+new_width]
    resized_frame = np.resize(cropped_frame, (height, width, 3))

    return resized_frame

def zoom_in_cv(t):
    if t < 0.5:
        return 1 +  0.6*t
    else:
        return 1.3
    






def return_index(list_ , item):
    for i in range(len(list_)):
        if list_[i] == item:
            return i
    return -1

def remove_items(list_ , item):
    new_list = []
    removed = False
    for i in list_:
        if i == item and removed == False:
            new_list.append(-1)
            removed = True
        else:
            new_list.append(i)
    return new_list
def isIn(list_ , item):
    for i in list_:
        if i == item:
            return True
    return False   





def render_video(uid: str):
    import cv2 , os 
    import moviepy.editor as mp
    import librosa
    import numpy as np
    import pandas as pd
    import random
    import moviepy.video.fx.all as vfx
    images , videos , music = [] , [] , ""
    if os.path.exists(f"./incoming_images/{uid}/"):
        images = [img for img in os.listdir(f"./incoming_images/{uid}/") if img.endswith(".png") or (img.endswith(".jpg"))]
    if os.path.exists(f"./incoming_videos/{uid}/"):
        videos = [vid for vid in os.listdir(f"./incoming_videos/{uid}/") if vid.endswith(".mp4") or vid.endswith(".avi")]
    if os.path.exists(f"./incoming_audio/{uid}/"):
        music = [mus for mus in os.listdir(f"./incoming_audio/{uid}/") if mus.endswith(".mp3") or mus.endswith(".wav")][0]
    y , s  = librosa.load(os.path.join(f"./incoming_audio/{uid}/", music))

    S, phase = librosa.magphase(librosa.stft(y))
    rms = librosa.feature.rms(S=S)

    threshold = rms.std()

    beat_frames = librosa.onset.onset_detect(y=y, sr=s , backtrack=True)
    filtered_onsets = []
    for i, onset_frame in enumerate(beat_frames):
        intensity_at_onset = rms[0, onset_frame]  # Assuming you used RMS
        
        if intensity_at_onset > threshold:
            filtered_onsets.append(onset_frame)

    # Convert back to time if needed
    filtered_onset_times = [0] + list(librosa.frames_to_time(filtered_onsets, sr=s))

    # for i  , frame in enumerate(filtered_onsets):
    print("length of images " , len(images)+len(videos))
    filtered_onset_times_ = filtered_onset_times[0:len(images)+len(videos)]
    hierarchy = {}
    for i , time in enumerate(filtered_onset_times_):
        hierarchy[time] = filtered_onset_times[i+1] - filtered_onset_times[i]
    print("Last time " , list(hierarchy.keys())[-1])
    print("Hierarchy " , len(hierarchy))
    times = list(hierarchy.values())
    times.sort(reverse=True)
    length_for_videos = times[0:len(videos)]
    length_for_images = times[len(videos):]
    timing_for_videos , timing_for_images = [], []
    values_ = list(hierarchy.values())
    print(length_for_images , "Length for images" , values_)
    print(values_ , "Values")
    for i in range(len(length_for_videos)):
        element = list(hierarchy.keys())[values_.index(length_for_videos[i])]
        if element not in timing_for_videos:
            timing_for_videos.append(element)
        else:
            values_ = remove_items(values_, length_for_videos[i])
            element = list(hierarchy.keys())[return_index(values_, length_for_videos[i])]
            timing_for_videos.append(element)
    for i in range(len(length_for_images)):
        element = list(hierarchy.keys())[return_index(values_, length_for_images[i])]
        # print(element , "Element")
        if isIn(timing_for_images , element) == False:
            print(element , "Element added")
            timing_for_images.append(element)
        else:
            # print(element , "Element removed" , return_index(values_, length_for_images[i]))
            if return_index(values_, length_for_images[i]) == -1:
                print("Removed" , length_for_images[i] , "Removed" , isIn(values_, length_for_images[i]))
            values_ = remove_items(values_, length_for_images[i])
            element = list(hierarchy.keys())[return_index(values_, length_for_images[i])]
            timing_for_images.append(element)
    print(len(timing_for_images) , len(timing_for_videos) , " timignfgg", len(hierarchy.keys()))

    print(timing_for_images , "Timing for images")

    clips =[]
    c = 0
    i_ , j_ = 0 , 0
    for i in hierarchy.keys():
        if i in list(timing_for_images):
            print(images[i_], "Image here" , i_)
            
            image = cv2.imread(os.path.join(f"./incoming_images/{uid}/", images[i_]))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            i_+=1
            image = mp.ImageClip(image).set_duration(hierarchy[i])
            width, height = image.size
            # Check if the image is already in 9:16 aspect ratio
            if width / height == 9 / 16:
                print("Image is already in 9:16 aspect ratio. No cropping needed.")
                cropped_image = image.resize((1080 , 1920))
            else:
                # Calculate the new dimensions for 9:16 aspect ratio
                # while maintaining the original aspect ratio
                new_width = int(height * (9/16))
                new_height = height

                # Calculate the crop dimensions
                left = (width - new_width) // 2
                right = left + new_width
                top = 0
                bottom = height

                # Crop the image
                cropped_image = image.crop(x1=left, y1=top, x2=right, y2=bottom).resize((1080 , 1920))

            clip = (cropped_image.resize(zoom_in_cv))
        elif i in list(timing_for_videos):
            print("Video here")
            video = mp.VideoFileClip(os.path.join(f"./incoming_videos/{uid}/", videos[j_]))
            j_+=1
            if video.duration > hierarchy[i]:
                t = video.duration - hierarchy[i]
                start_time = random.random() * t
                clip = video.subclip( start_time , start_time + hierarchy[i] ).resize((1080 , 1920))
            # clip = video.set_duration(hierarchy[i]).resize((1080 , 1920))
            else:
                clip = video.fx(vfx.speedx, factor = hierarchy[i]/video.duration)
            # width, height = clip.size

            # # Check if the clip is already in 9:16 aspect ratio
            # if width / height == 9 / 16:
            #     print("Video is already in 9:16 aspect ratio. No cropping needed.")
            #     cropped_clip = clip.resize((1080 , 1920))
            # else:
            #     # Calculate the new dimensions for 9:16 aspect ratio
            #     # while maintaining the original aspect ratio
            #     new_width = int(height * (9/16))
            #     new_height = height

            #     # Calculate the crop dimensions
            #     left = (width - new_width) // 2
            #     right = left + new_width
            #     top = 0
            #     bottom = height

            #     # Crop the clip
            #     cropped_clip = clip.crop(x1=left, y1=top, x2=right, y2=bottom).resize((1080 , 1920))

            clip = (clip.fx(vfx.fadein, 0.2)
                        .fx(vfx.fadeout, 0.2)
                        )    
        else:
            print("Not foundddddd")
            print(i)
        clips.append(clip)





    video = mp.concatenate_videoclips(clips, method="compose" )
    audio = mp.AudioFileClip(os.path.join(f"./incoming_audio/{uid}/", music)).subclip(0,video.duration)
    video = video.set_audio(audio)
    video.write_videofile(f"./output/{uid}/edit.mp4", fps=24 )
    return True

