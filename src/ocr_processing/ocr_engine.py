import pytesseract
from PIL import Image
import yaml
from typing import Dict, Tuple

class OCREngine:
    def __init__(self, config_path: str = "config/config.yaml"):
        with open(config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        
        self.tesseract_config = self.config['ocr_processing']['tesseract_config']
        self.min_confidence = self.config['ocr_processing']['min_confidence']
    
    def extract_text(self, image_path: str) -> Tuple[str, float]:
        """
        Extract text from an image using Tesseract OCR.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            Tuple[str, float]: (extracted text, confidence score)
        """
        try:
            image = Image.open(image_path)
            # Get text and confidence data
            data = pytesseract.image_to_data(image, config=self.tesseract_config, output_type=pytesseract.Output.DICT)
            
            # Combine text from all words with confidence > threshold
            text_parts = []
            confidences = []
            
            for i, conf in enumerate(data['conf']):
                if conf != '-1':  # -1 means no confidence data
                    conf = float(conf)
                    if conf >= self.min_confidence:
                        text_parts.append(data['text'][i])
                        confidences.append(conf)
            
            text = ' '.join(text_parts)
            avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
            
            return text, avg_confidence
            
        except Exception as e:
            print(f"Error processing image {image_path}: {str(e)}")
            return "", 0.0
    
    def process_product(self, image_path: str) -> Dict:
        """
        Process a product image and extract relevant information.
        
        Args:
            image_path (str): Path to the product image
            
        Returns:
            Dict: Dictionary containing extracted information
        """
        text, confidence = self.extract_text(image_path)
        
        # Basic product information extraction
        # This is a simple implementation - can be enhanced with NLP
        lines = text.split('\n')
        product_info = {
            'product_name': lines[0] if lines else '',  # First line as product name
            'company_name': '',  # To be implemented with better text analysis
            'product_description': '\n'.join(lines[1:]) if len(lines) > 1 else '',  # Rest as description
            'confidence': confidence,
            'raw_text': text
        }
        
        return product_info 