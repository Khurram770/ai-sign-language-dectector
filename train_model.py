"""
Training Script for Sign Language Recognition Model
Collect and train on sign language gesture data.
"""

import cv2
import numpy as np
import os
import pickle
import json
import time
from detector import HandDetector
from recognizer import SignRecognizer


def collect_training_data(sign_id, num_samples=50, output_dir="data"):
    """
    Collect training data for a specific sign.
    
    Args:
        sign_id: ID of the sign to collect data for
        num_samples: Number of samples to collect
        output_dir: Directory to save training data
    """
    os.makedirs(output_dir, exist_ok=True)
    
    detector = HandDetector(
        mode=False,
        max_hands=1,
        detection_confidence=0.7,
        tracking_confidence=0.5
    )
    
    cap = cv2.VideoCapture(0)
    samples_collected = 0
    features_list = []
    
    print(f"Collecting data for sign ID: {sign_id}")
    print(f"Press 's' to capture sample, 'q' to quit")
    print(f"Target: {num_samples} samples")
    
    while samples_collected < num_samples:
        success, img = cap.read()
        if not success:
            break
        
        img = cv2.flip(img, 1)
        img, results = detector.find_hands(img, draw=True)
        
        features = detector.extract_features(img, hand_no=0)
        
        # Display instructions
        cv2.putText(
            img, f"Sign ID: {sign_id} | Samples: {samples_collected}/{num_samples}",
            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2
        )
        cv2.putText(
            img, "Press 's' to capture, 'q' to quit",
            (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2
        )
        
        if features is not None:
            cv2.putText(
                img, "Hand detected - Press 's' to capture",
                (10, 110), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2
            )
        
        cv2.imshow("Training Data Collection", img)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('s') and features is not None:
            features_list.append(features)
            samples_collected += 1
            print(f"Sample {samples_collected}/{num_samples} collected")
            time.sleep(0.5)  # Small delay between captures
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Save collected data
    if features_list:
        data_file = os.path.join(output_dir, f"sign_{sign_id}.npz")
        np.savez(data_file, features=np.array(features_list), label=sign_id)
        print(f"Data saved to {data_file}")
        return len(features_list)
    else:
        print("No data collected")
        return 0


def load_training_data(data_dir="data"):
    """
    Load all training data from directory.
    
    Args:
        data_dir: Directory containing training data files
        
    Returns:
        features: Array of feature vectors
        labels: Array of labels
    """
    features_list = []
    labels_list = []
    
    if not os.path.exists(data_dir):
        print(f"Data directory {data_dir} does not exist")
        return np.array([]), np.array([])
    
    for filename in os.listdir(data_dir):
        if filename.startswith("sign_") and filename.endswith(".npz"):
            filepath = os.path.join(data_dir, filename)
            data = np.load(filepath)
            features_list.extend(data['features'])
            labels_list.extend([data['label']] * len(data['features']))
    
    if features_list:
        return np.array(features_list), np.array(labels_list)
    else:
        return np.array([]), np.array([])


def train_model(data_dir="data", model_path="model/sign_model.pkl"):
    """
    Train the sign language recognition model.
    
    Args:
        data_dir: Directory containing training data
        model_path: Path to save the trained model
    """
    print("Loading training data...")
    features, labels = load_training_data(data_dir)
    
    if len(features) == 0:
        print("No training data found. Please collect training data first.")
        print("You can use collect_training_data() function to collect data.")
        return
    
    print(f"Loaded {len(features)} samples")
    print(f"Number of classes: {len(np.unique(labels))}")
    
    # Initialize recognizer
    recognizer = SignRecognizer()
    
    # Train model
    print("Training model...")
    recognizer.train(features, labels)
    
    # Save model
    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    recognizer.save_model(model_path)
    print(f"Model trained and saved to {model_path}")


def interactive_training():
    """Interactive training interface."""
    # Load sign dictionary
    with open("sign_dictionary.json", 'r') as f:
        sign_dict = json.load(f)
    
    print("Sign Language Model Training")
    print("=" * 40)
    print("Available signs:")
    for sign_id, sign_text in sorted(sign_dict.items(), key=lambda x: int(x[0])):
        print(f"  {sign_id}: {sign_text}")
    print()
    
    while True:
        try:
            sign_id = input("Enter sign ID to train (or 'train' to train model, 'quit' to exit): ")
            
            if sign_id.lower() == 'quit':
                break
            elif sign_id.lower() == 'train':
                train_model()
            else:
                sign_id = int(sign_id)
                if str(sign_id) in sign_dict:
                    num_samples = int(input("Number of samples to collect (default 50): ") or "50")
                    collect_training_data(sign_id, num_samples)
                else:
                    print("Invalid sign ID")
        except ValueError:
            print("Invalid input")
        except KeyboardInterrupt:
            print("\nTraining interrupted")
            break


if __name__ == "__main__":
    import time
    os.makedirs("data", exist_ok=True)
    os.makedirs("model", exist_ok=True)
    
    # Run interactive training
    interactive_training()

