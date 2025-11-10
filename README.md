# Sign Language to Text Converter

A real-time sign language detection and conversion system that recognizes hand gestures and converts them to English text using computer vision and machine learning.

## Features

- Real-time hand tracking using MediaPipe
- Sign language gesture recognition
- Conversion to English text
- **Text-to-Speech (TTS)** - Speaks out detected signs
- Support for common ASL (American Sign Language) signs
- Camera-based input interface
- Extensible sign dictionary
- Toggle TTS on/off during runtime

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

### Web Application (Recommended)

Run the web application:
```bash
python app.py
```

Or using the startup script:
```bash
./run.sh
```

Then open your browser and navigate to:
```
http://localhost:5000
```

### Desktop Application

Run the desktop application (requires camera access):
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
├── app.py                  # Flask web application (for Kubernetes/Docker)
├── main.py                 # Desktop application entry point
├── detector.py             # Hand detection and tracking
├── recognizer.py           # Sign language recognition
├── text_converter.py       # Sign to text conversion
├── text_to_speech.py       # Text-to-speech module
├── gesture_recognizer.py   # Gesture-based recognition
├── train_model.py          # Training script for custom signs
├── test_detection.py       # Test hand detection functionality
├── verify_setup.py         # Verify installation and setup
├── sign_dictionary.json    # Sign to text mapping dictionary
├── templates/              # HTML templates
│   └── index.html          # Web interface
├── static/                 # Static files
│   ├── css/                # CSS stylesheets
│   └── js/                 # JavaScript files
├── k8s/                    # Kubernetes manifests
│   ├── deployment.yaml     # Kubernetes deployment
│   ├── service.yaml        # Kubernetes service
│   ├── configmap.yaml      # Configuration map
│   └── ingress.yaml        # Ingress configuration
├── model/                  # Trained models directory
├── data/                   # Training data directory
├── Dockerfile              # Docker container definition
├── docker-compose.yml      # Docker Compose configuration
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── QUICKSTART.md          # Quick start guide
├── SIGNS_GUIDE.md         # Signs reference guide
└── DEPLOYMENT.md          # Deployment guide
```

## How It Works

1. **Hand Detection**: Uses MediaPipe to detect and track hand landmarks in real-time
2. **Feature Extraction**: Extracts hand pose features from detected landmarks
3. **Sign Recognition**: Classifies hand gestures using rule-based gesture recognition
4. **Text Conversion**: Maps recognized signs to English text
5. **Text-to-Speech**: Speaks out the recognized signs automatically
6. **Display**: Shows the recognized text on screen

## Supported Signs

The system currently supports common ASL signs. You can extend the sign dictionary by:
- Adding new signs to `sign_dictionary.json`
- Training the model with new gesture data
- Modifying the recognition threshold

## Requirements

- Python 3.8+
- Webcam/Camera (for desktop app) or browser with camera access (for web app)
- MediaPipe
- OpenCV
- NumPy
- pyttsx3 (for text-to-speech)
- Flask (for web application)
- Gunicorn (for production deployment)

## Text-to-Speech (TTS)

The application includes text-to-speech functionality that speaks out detected signs:

- **Automatic Speech**: When a sign is recognized and added to the sentence, it's automatically spoken
- **Toggle Control**: Press 't' key to toggle TTS on/off during runtime
- **Configurable**: Adjust speech rate and volume in `main.py`
- **Cross-platform**: Works on Windows, macOS, and Linux

### TTS Controls

- **'t' key**: Toggle text-to-speech on/off
- TTS status is displayed on screen (green = ON, red = OFF)

### TTS Configuration

In `main.py`, you can adjust:
```python
tts_enabled = True   # Enable/disable TTS by default
tts_rate = 150       # Speech rate (words per minute)
tts_volume = 0.8     # Volume (0.0 to 1.0)
```

## Deployment

### Docker Deployment

```bash
# Build image
docker build -t sign-language-detector:latest .

# Run container
docker run -d -p 5000:5000 --device=/dev/video0 sign-language-detector:latest
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Access via port forward
kubectl port-forward service/sign-language-detector-service 5000:80
```

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

## API Endpoints

The web application provides the following API endpoints:

- `GET /` - Main web interface
- `GET /video_feed` - Video stream with sign detection
- `GET /api/status` - Get current detection status
- `GET /api/sentence` - Get current sentence
- `POST /api/sentence` - Clear sentence
- `POST /api/sentence/backspace` - Remove last word
- `POST /api/tts/toggle` - Toggle TTS on/off
- `GET /api/health` - Health check endpoint
- `GET /api/config` - Get configuration
- `POST /api/config` - Update configuration

## License

MIT License

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

