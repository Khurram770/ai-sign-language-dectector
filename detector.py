"""
Hand Detection Module
Uses MediaPipe to detect and track hand landmarks in real-time.
"""

import cv2
import mediapipe as mp
import numpy as np


class HandDetector:
    def __init__(self, mode=False, max_hands=2, detection_confidence=0.5, tracking_confidence=0.5):
        """
        Initialize the HandDetector.
        
        Args:
            mode: Whether to treat input images as a batch of static images
            max_hands: Maximum number of hands to detect
            detection_confidence: Minimum confidence for hand detection
            tracking_confidence: Minimum confidence for hand tracking
        """
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.tracking_confidence = tracking_confidence
        
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.tracking_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        
    def find_hands(self, img, draw=True):
        """
        Find hands in the image.
        
        Args:
            img: Input image (BGR format)
            draw: Whether to draw hand landmarks on the image
            
        Returns:
            img: Image with or without drawn landmarks
            results: MediaPipe hand detection results
        """
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(img_rgb)
        
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS
                    )
        
        return img, self.results
    
    def get_landmark_positions(self, img, hand_no=0, draw=False):
        """
        Get the positions of all hand landmarks.
        
        Args:
            img: Input image
            hand_no: Hand index (0 for first hand, 1 for second)
            draw: Whether to draw landmark positions
            
        Returns:
            landmark_list: List of landmark positions [id, x, y]
        """
        landmark_list = []
        
        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[hand_no]
            h, w, c = img.shape
            
            for id, landmark in enumerate(hand.landmark):
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                landmark_list.append([id, cx, cy])
                
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)
        
        return landmark_list
    
    def extract_features(self, img, hand_no=0):
        """
        Extract normalized hand features for classification.
        
        Args:
            img: Input image
            hand_no: Hand index
            
        Returns:
            features: Normalized feature vector or None if no hand detected
        """
        landmark_list = self.get_landmark_positions(img, hand_no)
        
        if len(landmark_list) == 0:
            return None
        
        # Get base point (wrist)
        base_x, base_y = landmark_list[0][1], landmark_list[0][2]
        
        # Normalize all points relative to the base
        features = []
        for landmark in landmark_list:
            # Normalize coordinates relative to wrist
            norm_x = (landmark[1] - base_x) / img.shape[1]
            norm_y = (landmark[2] - base_y) / img.shape[0]
            features.extend([norm_x, norm_y])
        
        return np.array(features)
    
    def get_hand_type(self, hand_no=0):
        """
        Get the type of hand (Left or Right).
        
        Args:
            hand_no: Hand index
            
        Returns:
            hand_type: "Left" or "Right" or None
        """
        if self.results.multi_handedness:
            if hand_no < len(self.results.multi_handedness):
                hand_label = self.results.multi_handedness[hand_no].classification[0].label
                return hand_label
        return None

