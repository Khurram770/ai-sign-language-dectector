"""
Sign Language Recognition Module
Classifies hand gestures into sign language signs.
"""

import numpy as np
import cv2
import os
import json
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import pickle
from gesture_recognizer import GestureRecognizer


class SignRecognizer:
    def __init__(self, model_path=None, sign_dict_path="sign_dictionary.json", use_gesture_recognition=True):
        """
        Initialize the SignRecognizer.
        
        Args:
            model_path: Path to pre-trained model file
            sign_dict_path: Path to sign dictionary JSON file
            use_gesture_recognition: Use rule-based gesture recognition (default: True)
        """
        self.model_path = model_path
        self.model = None
        self.sign_dict = self.load_sign_dictionary(sign_dict_path)
        self.use_gesture_recognition = use_gesture_recognition
        
        # Initialize gesture recognizer for rule-based recognition
        if use_gesture_recognition:
            self.gesture_recognizer = GestureRecognizer()
        else:
            self.gesture_recognizer = None
        
        if model_path and os.path.exists(model_path) and not use_gesture_recognition:
            self.load_model(model_path)
        elif not use_gesture_recognition:
            # Initialize a simple model (will need training)
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def load_sign_dictionary(self, dict_path):
        """Load sign dictionary from JSON file."""
        try:
            with open(dict_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Sign dictionary not found at {dict_path}")
            return {}
    
    def load_model(self, model_path):
        """Load a trained model from file."""
        try:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
            print(f"Model loaded from {model_path}")
        except Exception as e:
            print(f"Error loading model: {e}")
            self.model = RandomForestClassifier(n_estimators=100, random_state=42)
    
    def save_model(self, model_path):
        """Save the trained model to file."""
        os.makedirs(os.path.dirname(model_path) if os.path.dirname(model_path) else '.', exist_ok=True)
        with open(model_path, 'wb') as f:
            pickle.dump(self.model, f)
        print(f"Model saved to {model_path}")
    
    def train(self, features, labels, test_size=0.2):
        """
        Train the recognition model.
        
        Args:
            features: Feature vectors (n_samples, n_features)
            labels: Corresponding labels (n_samples,)
            test_size: Proportion of data to use for testing
        """
        if len(features) == 0:
            print("No training data provided")
            return
        
        X_train, X_test, y_train, y_test = train_test_split(
            features, labels, test_size=test_size, random_state=42
        )
        
        self.model.fit(X_train, y_train)
        
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        print(f"Training accuracy: {train_score:.2f}")
        print(f"Test accuracy: {test_score:.2f}")
    
    def predict(self, features, confidence_threshold=0.3):
        """
        Predict sign from features.
        
        Args:
            features: Feature vector (n_features,) or (1, n_features)
            confidence_threshold: Minimum confidence for prediction
            
        Returns:
            prediction: Predicted sign ID or None
            confidence: Prediction confidence
        """
        if self.model is None:
            return None, 0.0
        
        if features is None or len(features) == 0:
            return None, 0.0
        
        # Ensure features is 2D
        if len(features.shape) == 1:
            features = features.reshape(1, -1)
        
        # Get prediction probabilities
        try:
            probabilities = self.model.predict_proba(features)[0]
            max_prob_idx = np.argmax(probabilities)
            confidence = probabilities[max_prob_idx]
            
            if confidence >= confidence_threshold:
                prediction = self.model.classes_[max_prob_idx]
                return int(prediction), float(confidence)
            else:
                return None, float(confidence)
        except Exception as e:
            print(f"Error during prediction: {e}")
            return None, 0.0
    
    def recognize_sign(self, features, confidence_threshold=0.3, landmarks=None):
        """
        Recognize sign and return text.
        
        Args:
            features: Feature vector from hand detector (optional if using gesture recognition)
            confidence_threshold: Minimum confidence for recognition
            landmarks: List of hand landmarks in format [id, x, y] (required for gesture recognition)
            
        Returns:
            text: Recognized sign text or None
            confidence: Recognition confidence
        """
        # Use gesture-based recognition if enabled and landmarks are provided
        if self.use_gesture_recognition and landmarks is not None and len(landmarks) >= 21:
            sign_id, sign_name, confidence = self.gesture_recognizer.recognize_from_landmarks(landmarks)
            
            if sign_id is not None and confidence >= confidence_threshold:
                # Check if sign is in dictionary, otherwise use recognized name
                if str(sign_id) in self.sign_dict:
                    return self.sign_dict[str(sign_id)], confidence
                elif sign_name:
                    return sign_name, confidence
            
            return None, confidence if confidence else 0.0
        
        # Fall back to ML model if gesture recognition is disabled or landmarks not available
        if self.model is not None and features is not None:
            sign_id, confidence = self.predict(features, confidence_threshold)
            
            if sign_id is not None and str(sign_id) in self.sign_dict:
                return self.sign_dict[str(sign_id)], confidence
        
        return None, 0.0

