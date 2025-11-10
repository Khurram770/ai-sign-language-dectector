"""
Test script for hand detection.
Simple script to test if hand detection is working correctly.
"""

import cv2
from detector import HandDetector


def test_hand_detection():
    """Test hand detection functionality."""
    detector = HandDetector(
        mode=False,
        max_hands=2,
        detection_confidence=0.7,
        tracking_confidence=0.5
    )
    
    cap = cv2.VideoCapture(0)
    
    print("Hand Detection Test")
    print("Press 'q' to quit")
    
    while True:
        success, img = cap.read()
        if not success:
            print("Failed to read from camera")
            break
        
        img = cv2.flip(img, 1)
        
        # Detect hands
        img, results = detector.find_hands(img, draw=True)
        
        # Get hand landmarks
        if results.multi_hand_landmarks:
            landmarks = detector.get_landmark_positions(img, hand_no=0)
            hand_type = detector.get_hand_type(hand_no=0)
            
            if landmarks:
                cv2.putText(
                    img, f"Hand Detected: {hand_type} | Landmarks: {len(landmarks)}",
                    (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2
                )
            
            # Extract features
            features = detector.extract_features(img, hand_no=0)
            if features is not None:
                cv2.putText(
                    img, f"Features: {len(features)} dimensions",
                    (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2
                )
        else:
            cv2.putText(
                img, "No hand detected",
                (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2
            )
        
        cv2.imshow("Hand Detection Test", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print("Test completed")


if __name__ == "__main__":
    test_hand_detection()

