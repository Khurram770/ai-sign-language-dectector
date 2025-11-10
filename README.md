# Sign Language to Text Converter

A real-time sign language detection and conversion system that recognizes hand gestures and converts them to English text using computer vision and machine learning.

## Features

- Real-time hand tracking using MediaPipe
- Sign language gesture recognition
- Conversion to English text
- Support for common ASL (American Sign Language) signs
- Camera-based input interface
- Extensible sign dictionary

## Installation

1. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Verify installation:
```bash
python verify_setup.py
```

This will check that all dependencies are installed and your camera is working.

## Usage

### Basic Usage

Run the main application:
```bash
python main.py
```

### Training Custom Signs

To train the model with your own signs:
```bash
python train_model.py
```

### Testing Individual Components

Test the hand detection:
```bash
python test_detection.py
```

### Verify Setup

Verify that everything is installed correctly:
```bash
python verify_setup.py
```

## Project Structure

```
sign-language-detector/
├── main.py                 # Main application entry point
├── detector.py             # Hand detection and tracking
├── recognizer.py           # Sign language recognition
├── text_converter.py       # Sign to text conversion
├── train_model.py          # Training script for custom signs
├── test_detection.py       # Test hand detection functionality
├── verify_setup.py         # Verify installation and setup
├── sign_dictionary.json    # Sign to text mapping dictionary
├── model/                  # Trained models directory
├── data/                   # Training data directory
├── requirements.txt        # Python dependencies
├── README.md              # This file
└── QUICKSTART.md          # Quick start guide
```

## How It Works

1. **Hand Detection**: Uses MediaPipe to detect and track hand landmarks in real-time
2. **Feature Extraction**: Extracts hand pose features from detected landmarks
3. **Sign Recognition**: Classifies hand gestures using a trained model
4. **Text Conversion**: Maps recognized signs to English text
5. **Display**: Shows the recognized text on screen

## Supported Signs

The system currently supports common ASL signs. You can extend the sign dictionary by:
- Adding new signs to `sign_dictionary.json`
- Training the model with new gesture data
- Modifying the recognition threshold

## Requirements

- Python 3.8+
- Webcam/Camera
- MediaPipe
- OpenCV
- NumPy

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

