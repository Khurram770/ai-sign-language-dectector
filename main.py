"""
Main Application
Real-time sign language detection and text conversion.
"""

import cv2
import numpy as np
import time
import os
from detector import HandDetector
from recognizer import SignRecognizer
from text_converter import TextConverter




def main():
    """Main application loop."""
    # Initialize components
    detector = HandDetector(
        mode=False,
        max_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.5
    )
    
    # Use gesture-based recognition (rule-based, no training needed)
    recognizer = SignRecognizer(
        model_path="model/sign_model.pkl",
        sign_dict_path="sign_dictionary.json",
        use_gesture_recognition=True  # Enable rule-based gesture recognition
    )
    
    print("=" * 60)
    print("Gesture-based sign recognition enabled!")
    print("=" * 60)
    print("Supported signs:")
    print("  - Hello (open hand)")
    print("  - Good (thumbs up)")
    print("  - Bad (thumbs down)")
    print("  - Yes (OK sign)")
    print("  - Stop (fist)")
    print("  - More (pointing)")
    print("  - Victory (peace sign)")
    print("  - I Love You")
    print("  - Letters: A, B, C")
    print("  - And more...")
    print("=" * 60)
    print("Hold each gesture for ~1 second to add it to your sentence.")
    print("=" * 60)
    
    converter = TextConverter(sign_dict_path="sign_dictionary.json")
    
    # Initialize camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    # Variables for sign recognition
    last_sign_time = 0
    sign_hold_duration = 1.0  # seconds to hold sign before adding to sentence
    current_sign = None
    sign_start_time = None
    confidence_threshold = 0.4
    
    print("Sign Language Detector Started")
    print("Controls:")
    print("  - 'q': Quit")
    print("  - 'c': Clear sentence")
    print("  - 'b': Backspace (remove last word)")
    print("  - Space: Show your sign to the camera")
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from camera")
            break
        
        # Flip image horizontally for mirror effect
        img = cv2.flip(img, 1)
        
        # Detect hands
        img, results = detector.find_hands(img, draw=True)
        
        # Get hand landmarks and features
        landmarks = detector.get_landmark_positions(img, hand_no=0)
        features = detector.extract_features(img, hand_no=0)
        
        if landmarks and len(landmarks) >= 21:
            # Recognize sign using gesture recognition (landmarks-based)
            sign_text, confidence = recognizer.recognize_sign(
                features, 
                confidence_threshold=confidence_threshold,
                landmarks=landmarks
            )
            
            current_time = time.time()
            
            if sign_text:
                # Check if this is the same sign as before
                if sign_text == current_sign:
                    # Check if we've held the sign long enough
                    if sign_start_time and (current_time - sign_start_time) >= sign_hold_duration:
                        # Add sign to sentence
                        converter.add_sign(sign_text, min_confidence=confidence_threshold, confidence=confidence)
                        sign_start_time = None  # Reset to avoid重复添加
                        current_sign = None
                else:
                    # New sign detected
                    current_sign = sign_text
                    sign_start_time = current_time
                
                last_sign_time = current_time
                
                # Display current sign
                cv2.putText(
                    img, f"Sign: {sign_text} ({confidence:.2f})",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
                )
            else:
                # No sign detected or low confidence
                if current_time - last_sign_time > 0.5:
                    current_sign = None
                    sign_start_time = None
        
        # Display current sentence
        sentence = converter.get_current_sentence()
        if sentence:
            # Wrap text if too long
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
                    img, line,
                    (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
                )
                y_offset += 30
        
        # Display instructions
        instructions = [
            "Press 'q' to quit",
            "Press 'c' to clear",
            "Press 'b' for backspace"
        ]
        y_pos = img.shape[0] - 90
        for instruction in instructions:
            cv2.putText(
                img, instruction,
                (10, y_pos), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1
            )
            y_pos += 20
        
        # Display hand type and finger states if detected
        hand_type = detector.get_hand_type(hand_no=0)
        if hand_type and landmarks and len(landmarks) >= 21:
            # Show finger states for debugging
            if hasattr(recognizer, 'gesture_recognizer') and recognizer.gesture_recognizer:
                fingers = recognizer.gesture_recognizer.analyze_fingers(
                    [[lm[0], lm[1], lm[2], 0] for lm in landmarks]
                )
                if fingers:
                    extended_count = recognizer.gesture_recognizer.count_extended_fingers(fingers)
                    finger_info = f"Fingers: {extended_count}/5"
                    cv2.putText(
                        img, finger_info,
                        (img.shape[1] - 200, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1
                    )
            
            cv2.putText(
                img, f"Hand: {hand_type}",
                (img.shape[1] - 150, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2
            )
        
        # Show image
        cv2.imshow("Sign Language Detector", img)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('c'):
            converter.clear_sentence()
            print("Sentence cleared")
        elif key == ord('b'):
            converter.remove_last_word()
            print("Last word removed")
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()
    print("Application closed")


if __name__ == "__main__":
    os.makedirs("model", exist_ok=True)
    main()

