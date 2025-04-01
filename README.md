# Store OCR Reader

A Python-based OCR system for extracting product information from store shelf videos.

## Setup

1. Create and activate virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:
- macOS: `brew install tesseract`
- Ubuntu: `sudo apt-get install tesseract-ocr`
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki

4. Configure MongoDB:
- Install MongoDB locally or use MongoDB Atlas
- Update `config/config.yaml` with your MongoDB connection string

5. (Optional) Configure Google Cloud Vision:
- Create a Google Cloud project
- Enable the Cloud Vision API
- Create service account credentials
- Set the environment variable: `GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json`

## Project Structure

```
ocr_reader/
├── config/
│   └── config.yaml
├── src/
│   ├── video_processing/
│   ├── object_detection/
│   ├── ocr_processing/
│   ├── database/
│   ├── validation/
│   └── main.py
├── tests/
├── requirements.txt
└── README.md
```

## Usage

1. Place your video file in the input directory
2. Run the main script:
```bash
python src/main.py --input path/to/video.mp4
```

## Features

- Video frame extraction
- Object detection using YOLOv8
- OCR processing using Tesseract
- MongoDB storage
- Optional Google Cloud Vision validation
