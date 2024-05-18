import numpy as np
import cv2
from transformers import AutoProcessor, AutoModel


def sample_frame_indices(clip_len, frame_sample_rate, seg_len):
    converted_len = int(clip_len * frame_sample_rate)
    end_idx = np.random.randint(converted_len, seg_len)
    start_idx = end_idx - converted_len
    indices = np.linspace(start_idx, end_idx, num=clip_len)
    indices = np.clip(indices, start_idx, end_idx - 1).astype(np.int64)

    return indices


def get_video_frames(video_path, frame_indices):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Error opening video file '{video_path}'")
        return None
    
    frames = []
    for i in range(max(frame_indices) + 1):
        ret, frame = cap.read()
        if not ret:
            break
        if i in frame_indices:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames.append(frame_rgb)

    cap.release()
    return frames


def myFeatureExtractor(video_path):    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))    
    cap.release()
    
    indices = sample_frame_indices(clip_len=8, frame_sample_rate=3, seg_len=total_frames)
    video = get_video_frames(video_path, indices)    

    inputs = processor(videos=list(video), return_tensors="pt") 
    video_features = model.get_video_features(**inputs).detach()
    
    return video_features


processor = AutoProcessor.from_pretrained("microsoft/xclip-base-patch32")
model = AutoModel.from_pretrained("microsoft/xclip-base-patch32")