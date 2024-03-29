import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.metrics import structural_similarity as ssim
def shot_boundary_detection(video_path):
    # Open the video
    cap = cv2.VideoCapture(video_path)

    # Initialize variables
    ret, prev_frame = cap.read()
    prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_hist = cv2.calcHist([prev_frame], [0], None, [256], [0, 256])
    shot_boundaries = []

    # Loop through frames
    frame_count = 0
    while True:
        ret, curr_frame = cap.read()
        if not ret:
            break

        curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        curr_hist = cv2.calcHist([curr_frame], [0], None, [256], [0, 256])

        # Compare histograms
        hist_diff = cv2.compareHist(prev_hist, curr_hist, cv2.HISTCMP_BHATTACHARYYA)

        # Adaptive thresholding
        mean_diff = np.mean(np.abs(prev_frame.astype(np.float32) - curr_frame.astype(np.float32)))
        threshold =  min(0.7, 0.4 + mean_diff / 255)
        
        if hist_diff > threshold:
            print(f"Frame {frame_count} - Hist diff: {hist_diff}, Mean diff: {mean_diff}, Threshold: {threshold}")
            shot_boundaries.append(frame_count)
            combined_frame = np.hstack((prev_frame, curr_frame))
            cv2.imshow("Current and Previous Frames", combined_frame)
            cv2.waitKey(13)
            # plt.figure(figsize=(10, 5))
            # plt.subplot(1, 2, 1)
            # plt.plot(prev_hist, color='r')
            # plt.title('Previous Frame Histogram')
            # plt.xlabel('Bin')
            # plt.ylabel('Count')

            # plt.subplot(1, 2, 2)
            # plt.plot(curr_hist, color='g')
            # plt.title('Current Frame Histogram')
            # plt.xlabel('Bin')
            # plt.ylabel('Count')

            # plt.tight_layout()
            # plt.show()
            print(f"Shot boundary detected at frame {frame_count}")

        prev_frame = curr_frame
        prev_hist = curr_hist
        frame_count += 1

    cap.release()
    return shot_boundaries

# Example usage
def shot_boundary_detection_edge(video_path):
    # Open the video
    cap = cv2.VideoCapture(video_path)

    # Initialize variables
    ret, prev_frame = cap.read()
    prev_frame = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
    prev_edges = cv2.Canny(prev_frame, 300, 300)
    shot_boundaries = []

    # Loop through frames
    frame_count = 0
    while True:
        ret, curr_frame = cap.read()
        if not ret:
            break

        curr_frame = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
        curr_edges = cv2.Canny(curr_frame, 300, 300)

        # Compare edge maps
        edge_diff = np.sum(np.abs(curr_edges.astype(np.float32) - prev_edges.astype(np.float32))) / (np.sum(curr_edges))
        threshold = 4  # Adjust this threshold as needed

        # Detect shot boundary
        if edge_diff > threshold:
            print(f"Frame {frame_count} - Edge diff: {edge_diff}, Threshold: {threshold}")
            shot_boundaries.append(frame_count)
            combined_frame = np.hstack((prev_edges, curr_edges))
            cv2.imshow("Current and Previous Frames", combined_frame)
            cv2.waitKey(13)
            print(f"Shot boundary detected at frame {frame_count}")

        prev_frame = curr_frame
        prev_edges = curr_edges
        frame_count += 1

    cap.release()
    cv2.destroyAllWindows()
    return shot_boundaries

def diff_threshhold(video):
    cap = cv2.VideoCapture(video)
    ret , frame = cap.read()
    count = 0
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if ret:
        while True:
            ret_ , frame_ = cap.read()
            frame_ = cv2.cvtColor(frame_, cv2.COLOR_BGR2GRAY)
            # diff = cv2.absdiff(frame, frame_)
            (score, diff) = ssim(frame, frame_, full=True)

# Print the SSIM score
            if(score<0.9):
                print(f"Frame {count} - SSIM score: {score}")
                diff = (diff * 255).astype(np.uint8)
                cv2.imshow('Difference', diff)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
            print(f"SSIM score: {score}")

            # Display the difference image (for visualization purposes)
            
            frame = frame_
            count+=1
 
shot_boundaries = diff_threshhold("./video2.mp4")
print(f"Shot boundaries: {shot_boundaries}")