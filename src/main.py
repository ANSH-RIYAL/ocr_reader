import argparse
from pathlib import Path
from video_processing.frame_extractor import FrameExtractor
from object_detection.detector import ObjectDetector
from ocr_processing.ocr_engine import OCREngine
from database.mongodb_client import MongoDBClient

def process_video(video_path: str, config_path: str = "config/config.yaml"):
    """
    Process a video file through the entire pipeline.
    
    Args:
        video_path (str): Path to the video file
        config_path (str): Path to the configuration file
    """
    # Initialize components
    frame_extractor = FrameExtractor(config_path)
    object_detector = ObjectDetector(config_path)
    ocr_engine = OCREngine(config_path)
    db_client = MongoDBClient(config_path)
    
    # Extract frames from video
    print(f"Extracting frames from video: {video_path}")
    frame_paths = frame_extractor.extract_frames(video_path)
    print(f"Extracted {len(frame_paths)} frames")
    
    # Process each frame
    for frame_path in frame_paths:
        print(f"\nProcessing frame: {frame_path}")
        
        # Detect and crop objects
        output_dir = Path(frame_path).parent / "objects"
        object_paths = object_detector.crop_objects(frame_path, str(output_dir))
        print(f"Detected {len(object_paths)} objects")
        
        # Process each object
        for obj_path in object_paths:
            print(f"\nProcessing object: {obj_path}")
            
            # Extract text and product information
            product_info = ocr_engine.process_product(obj_path)
            
            # Add source information
            product_info['source_video'] = video_path
            product_info['source_frame'] = frame_path
            product_info['object_image'] = obj_path
            
            # Store in database
            product_id = db_client.insert_product(product_info)
            print(f"Stored product with ID: {product_id}")
            print(f"Extracted text: {product_info['raw_text'][:100]}...")

def main():
    parser = argparse.ArgumentParser(description='Process video for product information extraction')
    parser.add_argument('--input', required=True, help='Path to input video file')
    parser.add_argument('--config', default='config/config.yaml', help='Path to configuration file')
    
    args = parser.parse_args()
    
    # Check if video file exists
    if not Path(args.input).exists():
        print(f"Error: Video file not found: {args.input}")
        return
    
    # Process the video
    try:
        process_video(args.input, args.config)
    except Exception as e:
        print(f"Error processing video: {str(e)}")

if __name__ == "__main__":
    main()
