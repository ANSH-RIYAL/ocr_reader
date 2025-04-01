from ultralytics import YOLO
import cv2
import yaml
from pathlib import Path
from typing import List, Tuple

class ObjectDetector:
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.model = YOLO(self.config['object_detection']['model'])
        self.conf_threshold = self.config['object_detection']['confidence_threshold']
    
    def detect_objects(self, image_path: str) -> List[Tuple[Tuple[int, int, int, int], float]]:
        """
        Detect objects in an image using YOLOv8.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            List[Tuple[Tuple[int, int, int, int], float]]: List of (bbox, confidence) tuples
        """
        results = self.model(image_path, conf=self.conf_threshold)
        
        detections = []
        for result in results:
            boxes = result.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                confidence = box.conf[0].cpu().numpy()
                detections.append(((int(x1), int(y1), int(x2), int(y2)), float(confidence)))
        
        return detections
    
    def crop_objects(self, image_path: str, output_dir: str) -> List[str]:
        """
        Detect and crop objects from an image.
        
        Args:
            image_path (str): Path to the image file
            output_dir (str): Directory to save cropped objects
            
        Returns:
            List[str]: List of paths to cropped object images
        """
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not read image: {image_path}")
        
        detections = self.detect_objects(image_path)
        cropped_paths = []
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for i, (bbox, _) in enumerate(detections):
            x1, y1, x2, y2 = bbox
            cropped = image[y1:y2, x1:x2]
            
            output_path = output_dir / f"object_{i:04d}.jpg"
            cv2.imwrite(str(output_path), cropped)
            cropped_paths.append(str(output_path))
        
        return cropped_paths 