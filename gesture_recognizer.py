"""
Gesture-Based Sign Language Recognizer
Recognizes ASL signs based on hand landmark positions and finger states.
"""

import numpy as np
import math


class GestureRecognizer:
    """Recognizes sign language gestures based on hand landmark analysis."""
    
    def __init__(self):
        """Initialize the gesture recognizer."""
        # Landmark indices for MediaPipe Hands
        # Thumb: 4 (tip), 3, 2, 1
        # Index: 8 (tip), 7, 6, 5
        # Middle: 12 (tip), 11, 10, 9
        # Ring: 16 (tip), 15, 14, 13
        # Pinky: 20 (tip), 19, 18, 17
        # Wrist: 0
        
        self.landmark_names = {
            'WRIST': 0,
            'THUMB_CMC': 1, 'THUMB_MCP': 2, 'THUMB_IP': 3, 'THUMB_TIP': 4,
            'INDEX_MCP': 5, 'INDEX_PIP': 6, 'INDEX_DIP': 7, 'INDEX_TIP': 8,
            'MIDDLE_MCP': 9, 'MIDDLE_PIP': 10, 'MIDDLE_DIP': 11, 'MIDDLE_TIP': 12,
            'RING_MCP': 13, 'RING_PIP': 14, 'RING_DIP': 15, 'RING_TIP': 16,
            'PINKY_MCP': 17, 'PINKY_PIP': 18, 'PINKY_DIP': 19, 'PINKY_TIP': 20
        }
    
    def calculate_distance(self, point1, point2):
        """Calculate Euclidean distance between two points."""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
    def is_finger_extended(self, landmarks, finger_tip, finger_pip, finger_mcp, is_thumb=False):
        """
        Check if a finger is extended.
        
        Args:
            landmarks: List of landmark positions [id, x, y, z]
            finger_tip: Tip landmark index
            finger_pip: PIP joint landmark index
            finger_mcp: MCP joint landmark index
            is_thumb: Whether this is the thumb (uses different logic)
        """
        if len(landmarks) <= max(finger_tip, finger_pip, finger_mcp):
            return False
        
        tip = landmarks[finger_tip]  # [id, x, y, z]
        pip = landmarks[finger_pip]
        mcp = landmarks[finger_mcp]
        wrist = landmarks[0]
        
        if is_thumb:
            # For thumb, check if tip is further from wrist than MCP joint
            # Thumb extended if tip is more to the side than MCP
            tip_dist_from_wrist_x = abs(tip[1] - wrist[1])
            mcp_dist_from_wrist_x = abs(mcp[1] - wrist[1])
            return tip_dist_from_wrist_x > mcp_dist_from_wrist_x
        else:
            # For other fingers, check if tip is above PIP joint (smaller y = higher on screen)
            # In image coordinates, y increases downward, so tip[2] < pip[2] means tip is above pip
            return tip[2] < pip[2]
    
    def analyze_fingers(self, landmarks):
        """
        Analyze which fingers are extended.
        
        Returns:
            dict: Finger states (True = extended, False = closed)
        """
        if len(landmarks) < 21:
            return None
        
        fingers = {
            'thumb': self.is_finger_extended(
                landmarks, 4, 3, 2, is_thumb=True
            ),
            'index': self.is_finger_extended(
                landmarks, 8, 6, 5, is_thumb=False
            ),
            'middle': self.is_finger_extended(
                landmarks, 12, 10, 9, is_thumb=False
            ),
            'ring': self.is_finger_extended(
                landmarks, 16, 14, 13, is_thumb=False
            ),
            'pinky': self.is_finger_extended(
                landmarks, 20, 18, 17, is_thumb=False
            )
        }
        
        return fingers
    
    def count_extended_fingers(self, fingers):
        """Count how many fingers are extended."""
        if fingers is None:
            return 0
        return sum([1 for f in fingers.values() if f])
    
    def recognize_gesture(self, landmarks):
        """
        Recognize gesture from hand landmarks.
        
        Args:
            landmarks: List of landmark positions [id, x, y, z]
            
        Returns:
            tuple: (sign_id, sign_name, confidence)
        """
        if landmarks is None or len(landmarks) < 21:
            return None, None, 0.0
        
        # Convert to list of [x, y] coordinates
        hand_landmarks = [[lm[1], lm[2]] for lm in landmarks]
        
        # Analyze finger states
        fingers = self.analyze_fingers(landmarks)
        if fingers is None:
            return None, None, 0.0
        
        extended_count = self.count_extended_fingers(fingers)
        
        # Get key landmark positions
        thumb_tip = landmarks[4]
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]
        wrist = landmarks[0]
        
        # Calculate distances
        thumb_index_dist = self.calculate_distance(
            [thumb_tip[1], thumb_tip[2]], [index_tip[1], index_tip[2]]
        )
        index_middle_dist = self.calculate_distance(
            [index_tip[1], index_tip[2]], [middle_tip[1], middle_tip[2]]
        )
        
        # Normalize distances (relative to hand size)
        hand_size = self.calculate_distance(
            [wrist[1], wrist[2]], [middle_tip[1], middle_tip[2]]
        )
        if hand_size < 10:  # Too small, invalid
            return None, None, 0.0
        
        thumb_index_norm = thumb_index_dist / hand_size
        index_middle_norm = index_middle_dist / hand_size
        
        # Gesture Recognition Logic
        
        # THUMBS UP (Good) - Only thumb extended, others closed
        if fingers['thumb'] and not fingers['index'] and not fingers['middle'] and \
           not fingers['ring'] and not fingers['pinky']:
            # Verify thumb is actually pointing up (tip above wrist)
            if thumb_tip[2] < wrist[2]:  # Thumb tip above wrist
                return 8, "Good", 0.9
        
        # THUMBS DOWN (Bad) - Thumb pointing down, others closed
        if not fingers['index'] and not fingers['middle'] and \
           not fingers['ring'] and not fingers['pinky']:
            # Check if thumb is pointing down (tip below wrist)
            if thumb_tip[2] > wrist[2] + 30:  # Thumb tip significantly below wrist
                return 9, "Bad", 0.85
        
        # OK SIGN / YES - Thumb and index form circle, others closed
        if fingers['thumb'] and fingers['index'] and not fingers['middle'] and \
           not fingers['ring'] and not fingers['pinky']:
            # Check if thumb and index are close (forming a circle)
            if thumb_index_norm < 0.2:  # Thumb and index close together (circle)
                # Also check if middle, ring, pinky are closed (not extended)
                middle_tip = landmarks[12]
                ring_tip = landmarks[16]
                pinky_tip = landmarks[20]
                middle_pip = landmarks[10]
                ring_pip = landmarks[14]
                pinky_pip = landmarks[18]
                
                if (middle_tip[2] > middle_pip[2] and 
                    ring_tip[2] > ring_pip[2] and 
                    pinky_tip[2] > pinky_pip[2]):
                    return 3, "Yes", 0.9
        
        # PEACE SIGN (V) - Index and middle extended, others closed
        if not fingers['thumb'] and fingers['index'] and fingers['middle'] and \
           not fingers['ring'] and not fingers['pinky']:
            if index_middle_norm > 0.2:  # Fingers spread apart
                return 20, "Victory", 0.85
        
        # POINTING (Index extended) - Only index finger extended
        if not fingers['thumb'] and fingers['index'] and not fingers['middle'] and \
           not fingers['ring'] and not fingers['pinky']:
            return 12, "More", 0.8
        
        # FIST (Stop) - All fingers closed
        if not fingers['thumb'] and not fingers['index'] and not fingers['middle'] and \
           not fingers['ring'] and not fingers['pinky']:
            return 10, "Stop", 0.9
        
        # OPEN HAND (Hello) - All fingers extended
        if fingers['thumb'] and fingers['index'] and fingers['middle'] and \
           fingers['ring'] and fingers['pinky']:
            return 0, "Hello", 0.9
        
        # THREE FINGERS - Index, middle, ring extended
        if not fingers['thumb'] and fingers['index'] and fingers['middle'] and \
           fingers['ring'] and not fingers['pinky']:
            return 13, "Less", 0.8
        
        # FOUR FINGERS - All except thumb
        if not fingers['thumb'] and fingers['index'] and fingers['middle'] and \
           fingers['ring'] and fingers['pinky']:
            return 14, "Water", 0.75
        
        # I LOVE YOU - Thumb, index, pinky extended
        if fingers['thumb'] and fingers['index'] and not fingers['middle'] and \
           not fingers['ring'] and fingers['pinky']:
            return 7, "I Love You", 0.85
        
        # LETTER A - Fist with thumb on side
        if not fingers['index'] and not fingers['middle'] and not fingers['ring'] and \
           not fingers['pinky'] and fingers['thumb']:
            # Check if thumb is positioned on the side
            if abs(thumb_tip[1] - wrist[1]) < 30:  # Thumb close to wrist horizontally
                return 21, "A", 0.8
        
        # LETTER B - All fingers extended except thumb
        if not fingers['thumb'] and fingers['index'] and fingers['middle'] and \
           fingers['ring'] and fingers['pinky']:
            # Check if fingers are together
            if index_middle_norm < 0.3:
                return 22, "B", 0.8
        
        # LETTER C - Curved hand (thumb and index form C)
        if fingers['thumb'] and fingers['index'] and not fingers['middle'] and \
           not fingers['ring'] and not fingers['pinky']:
            if 0.2 < thumb_index_norm < 0.4:  # Moderate distance (C shape)
                return 23, "C", 0.75
        
        # No match found
        return None, None, 0.0
    
    def recognize_from_landmarks(self, landmark_list):
        """
        Recognize sign from landmark list format [id, x, y].
        
        Args:
            landmark_list: List of landmarks in format [id, x, y]
            
        Returns:
            tuple: (sign_id, sign_name, confidence)
        """
        if landmark_list is None or len(landmark_list) < 21:
            return None, None, 0.0
        
        # Convert to format expected by recognize_gesture
        landmarks = []
        for lm in landmark_list:
            if len(lm) >= 3:
                landmarks.append([lm[0], lm[1], lm[2], 0])  # [id, x, y, z]
            else:
                return None, None, 0.0
        
        return self.recognize_gesture(landmarks)

