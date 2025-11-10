"""
Flask Web Application for Sign Language Detection
Provides web interface and API for sign language detection.
"""

from flask import Flask, render_template, Response, jsonify, request
from flask_cors import CORS
import cv2
import numpy as np
import time
import threading
import base64
from detector import HandDetector
from recognizer import SignRecognizer
from text_converter import TextConverter
from text_to_speech import TextToSpeech
import json
import os
from PIL import Image
import io

app = Flask(__name__)
CORS(app)  # Enable CORS for browser camera access

# Global variables for sign detection
detector = None
recognizer = None
converter = None
tts = None
camera = None
camera_lock = threading.Lock()

# Sign detection state
detection_state = {
    'current_sentence': [],
    'current_sign': None,
    'sign_start_time': None,
    'last_sign_time': 0,
    'last_spoken_sign': None,
    'sign_hold_duration': 1.0,
    'confidence_threshold': 0.4,
    'tts_enabled': True
}


def init_components():
    """Initialize detection components."""
    global detector, recognizer, converter, tts
    
    if detector is None:
        detector = HandDetector(
            mode=False,
            max_hands=1,
            detection_confidence=0.7,
            tracking_confidence=0.5
        )
    
    if recognizer is None:
        recognizer = SignRecognizer(
            model_path="model/sign_model.pkl",
            sign_dict_path="sign_dictionary.json",
            use_gesture_recognition=True
        )
    
    if converter is None:
        converter = TextConverter(sign_dict_path="sign_dictionary.json")
    
    if tts is None:
        tts_enabled = os.getenv('TTS_ENABLED', 'true').lower() == 'true'
        tts = TextToSpeech(enabled=tts_enabled, rate=150, volume=0.8)


def get_camera():
    """Get or create camera instance."""
    global camera
    with camera_lock:
        if camera is None or not camera.isOpened():
            try:
                camera_index = int(os.getenv('CAMERA_INDEX', '0'))
                camera = cv2.VideoCapture(camera_index)
                if camera.isOpened():
                    camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                else:
                    print(f"Warning: Could not open camera {camera_index}")
                    return None
            except Exception as e:
                print(f"Error opening camera: {e}")
                return None
    return camera


def detect_signs(frame):
    """Detect signs in a frame."""
    global detector, recognizer, converter, tts, detection_state
    
    if detector is None or recognizer is None:
        init_components()
    
    # Flip frame horizontally for mirror effect
    frame = cv2.flip(frame, 1)
    
    # Detect hands
    frame, results = detector.find_hands(frame, draw=True)
    
    # Get hand landmarks
    landmarks = detector.get_landmark_positions(frame, hand_no=0)
    features = detector.extract_features(frame, hand_no=0)
    
    sign_text = None
    confidence = 0.0
    
    if landmarks and len(landmarks) >= 21:
        # Recognize sign
        sign_text, confidence = recognizer.recognize_sign(
            features,
            confidence_threshold=detection_state['confidence_threshold'],
            landmarks=landmarks
        )
        
        current_time = time.time()
        
        if sign_text:
            # Check if this is the same sign as before
            if sign_text == detection_state['current_sign']:
                # Check if we've held the sign long enough
                if (detection_state['sign_start_time'] and 
                    (current_time - detection_state['sign_start_time']) >= detection_state['sign_hold_duration']):
                    # Add sign to sentence
                    if converter.add_sign(sign_text, 
                                        min_confidence=detection_state['confidence_threshold'],
                                        confidence=confidence):
                        # Speak the recognized sign
                        if (detection_state['tts_enabled'] and tts and tts.engine is not None and
                            sign_text != detection_state['last_spoken_sign']):
                            tts.speak_async(sign_text)
                            detection_state['last_spoken_sign'] = sign_text
                        
                        # Update sentence
                        detection_state['current_sentence'] = converter.current_sentence.copy()
                    
                    detection_state['sign_start_time'] = None
                    detection_state['current_sign'] = None
            else:
                # New sign detected
                detection_state['current_sign'] = sign_text
                detection_state['sign_start_time'] = current_time
            
            detection_state['last_sign_time'] = current_time
        else:
            # No sign detected or low confidence
            if current_time - detection_state['last_sign_time'] > 0.5:
                detection_state['current_sign'] = None
                detection_state['sign_start_time'] = None
    
    # Get current sentence
    sentence = converter.get_current_sentence() if converter else ""
    
    return frame, sign_text, confidence, sentence


def generate_frames():
    """Generate video frames with sign detection."""
    global camera
    
    camera = get_camera()
    if camera is None:
        # Generate a placeholder frame if camera is not available
        while True:
            frame = np.zeros((480, 640, 3), dtype=np.uint8)
            cv2.putText(frame, "Camera not available", (50, 240),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
            time.sleep(1)
        return
    
    while True:
        try:
            with camera_lock:
                if camera is None or not camera.isOpened():
                    camera = get_camera()
                    if camera is None:
                        time.sleep(1)
                        continue
                
                success, frame = camera.read()
                if not success:
                    time.sleep(0.1)
                    continue
            
            # Detect signs
            frame, sign_text, confidence, sentence = detect_signs(frame)
            
            # Add text overlays
            if sign_text:
                cv2.putText(
                    frame, f"Sign: {sign_text} ({confidence:.2f})",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
                )
            
            if sentence:
                # Wrap sentence text
                words = sentence.split()
                lines = []
                current_line = ""
                for word in words:
                    test_line = current_line + " " + word if current_line else word
                    if len(test_line) < 40:
                        current_line = test_line
                    else:
                        if current_line:
                            lines.append(current_line)
                        current_line = word
                if current_line:
                    lines.append(current_line)
                
                y_offset = 70
                for line in lines:
                    cv2.putText(
                        frame, line,
                        (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
                    )
                    y_offset += 30
            
            # Add TTS status
            tts_status = "TTS: ON" if (detection_state['tts_enabled'] and tts and tts.engine) else "TTS: OFF"
            tts_color = (0, 255, 0) if (detection_state['tts_enabled'] and tts and tts.engine) else (0, 0, 255)
            cv2.putText(
                frame, tts_status,
                (frame.shape[1] - 120, frame.shape[0] - 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, tts_color, 2
            )
            
            # Encode frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 85])
            if not ret:
                continue
            
            frame_bytes = buffer.tobytes()
            
            # Yield frame in multipart format
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            
        except Exception as e:
            print(f"Error in frame generation: {e}")
            time.sleep(1)
            continue
        
        time.sleep(0.03)  # ~30 FPS


@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/video_feed')
def video_feed():
    """Video streaming route (legacy - for server-side camera)."""
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/api/detect', methods=['POST'])
def detect_from_image():
    """Detect sign from uploaded image frame."""
    global detector, recognizer, converter, tts, detection_state
    
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    try:
        # Get image file
        image_file = request.files['image']
        
        # Read image
        image_bytes = image_file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if frame is None:
            return jsonify({'error': 'Invalid image'}), 400
        
        # Initialize components if needed
        if detector is None or recognizer is None:
            init_components()
        
        # Detect signs
        frame, sign_text, confidence, sentence = detect_signs(frame)
        
        # Update detection state
        current_time = time.time()
        
        if sign_text:
            # Check if this is the same sign as before
            if sign_text == detection_state['current_sign']:
                # Check if we've held the sign long enough
                if (detection_state['sign_start_time'] and 
                    (current_time - detection_state['sign_start_time']) >= detection_state['sign_hold_duration']):
                    # Add sign to sentence
                    if converter.add_sign(sign_text, 
                                        min_confidence=detection_state['confidence_threshold'],
                                        confidence=confidence):
                        # Speak the recognized sign
                        if (detection_state['tts_enabled'] and tts and tts.engine is not None and
                            sign_text != detection_state['last_spoken_sign']):
                            tts.speak_async(sign_text)
                            detection_state['last_spoken_sign'] = sign_text
                        
                        # Update sentence
                        detection_state['current_sentence'] = converter.current_sentence.copy()
                    
                    detection_state['sign_start_time'] = None
                    detection_state['current_sign'] = None
            else:
                # New sign detected
                detection_state['current_sign'] = sign_text
                detection_state['sign_start_time'] = current_time
            
            detection_state['last_sign_time'] = current_time
        
        return jsonify({
            'sign': sign_text,
            'confidence': float(confidence) if confidence else 0.0,
            'sentence': sentence
        })
        
    except Exception as e:
        print(f"Error in detection: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/status', methods=['GET'])
def get_status():
    """Get current detection status."""
    global converter, detection_state
    
    sentence = converter.get_current_sentence() if converter else ""
    
    return jsonify({
        'sentence': sentence,
        'current_sign': detection_state['current_sign'],
        'tts_enabled': detection_state['tts_enabled'],
        'confidence_threshold': detection_state['confidence_threshold']
    })


@app.route('/api/sentence', methods=['GET'])
def get_sentence():
    """Get current sentence."""
    global converter
    sentence = converter.get_current_sentence() if converter else ""
    return jsonify({'sentence': sentence})


@app.route('/api/sentence', methods=['POST'])
def clear_sentence():
    """Clear current sentence."""
    global converter, detection_state
    
    if converter:
        converter.clear_sentence()
        detection_state['current_sentence'] = []
        detection_state['last_spoken_sign'] = None
    
    return jsonify({'success': True, 'message': 'Sentence cleared'})


@app.route('/api/sentence/backspace', methods=['POST'])
def remove_last_word():
    """Remove last word from sentence."""
    global converter, detection_state
    
    if converter:
        converter.remove_last_word()
        detection_state['current_sentence'] = converter.current_sentence.copy()
        detection_state['last_spoken_sign'] = None
    
    return jsonify({'success': True, 'message': 'Last word removed'})


@app.route('/api/tts/toggle', methods=['POST'])
def toggle_tts():
    """Toggle TTS on/off."""
    global tts, detection_state
    
    detection_state['tts_enabled'] = not detection_state['tts_enabled']
    
    if not detection_state['tts_enabled'] and tts:
        tts.stop()
    
    return jsonify({
        'success': True,
        'tts_enabled': detection_state['tts_enabled']
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes."""
    camera_available = False
    if camera:
        try:
            with camera_lock:
                camera_available = camera.isOpened()
        except:
            camera_available = False
    
    return jsonify({
        'status': 'healthy',
        'camera': camera_available,
        'detector': detector is not None,
        'recognizer': recognizer is not None
    }), 200


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get configuration."""
    return jsonify({
        'confidence_threshold': detection_state['confidence_threshold'],
        'sign_hold_duration': detection_state['sign_hold_duration'],
        'tts_enabled': detection_state['tts_enabled']
    })


@app.route('/api/config', methods=['POST'])
def update_config():
    """Update configuration."""
    global detection_state
    
    data = request.get_json()
    
    if 'confidence_threshold' in data:
        detection_state['confidence_threshold'] = float(data['confidence_threshold'])
    
    if 'sign_hold_duration' in data:
        detection_state['sign_hold_duration'] = float(data['sign_hold_duration'])
    
    return jsonify({
        'success': True,
        'config': {
            'confidence_threshold': detection_state['confidence_threshold'],
            'sign_hold_duration': detection_state['sign_hold_duration'],
            'tts_enabled': detection_state['tts_enabled']
        }
    })


def cleanup():
    """Cleanup resources."""
    global camera, tts
    
    if camera:
        camera.release()
    
    if tts:
        tts.shutdown()


@app.teardown_appcontext
def close_camera(error):
    """Close camera on app teardown."""
    pass


if __name__ == '__main__':
    # Initialize components
    init_components()
    
    # Get port from environment or use default
    port = int(os.getenv('PORT', 5000))
    host = os.getenv('HOST', '0.0.0.0')
    debug = os.getenv('DEBUG', 'false').lower() == 'true'
    
    try:
        app.run(host=host, port=port, debug=debug, threaded=True)
    finally:
        cleanup()

