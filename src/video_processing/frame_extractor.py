import cv2
import os
from pathlib import Path
import yaml

class FrameExtractor:
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.output_dir = Path(self.config['video_processing']['output_dir'])
        self.frame_interval = self.config['video_processing']['frame_interval']
        
        # Create output directory if it doesn't exist
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_frames(self, video_path: str) -> list:
        """
        Extract frames from video at specified intervals.
        
        Args:
            video_path (str): Path to the video file
            
        Returns:
            list: List of paths to extracted frames
        """
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        frame_paths = []
        frame_count = 0
        frame_number = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            if frame_count % self.frame_interval == 0:
                frame_path = self.output_dir / f"frame_{frame_number:04d}.jpg"
                cv2.imwrite(str(frame_path), frame)
                frame_paths.append(str(frame_path))
                frame_number += 1
            
            frame_count += 1
        
        cap.release()
        return frame_paths 