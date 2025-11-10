# Sign Language Gestures Guide

This guide explains the hand gestures that the sign language detector can recognize.

## Supported Gestures

### Basic Gestures

1. **Hello** 👋
   - **Gesture**: Open hand with all fingers extended
   - **How to**: Extend all five fingers straight out
   - **Sign ID**: 0

2. **Good** 👍
   - **Gesture**: Thumbs up
   - **How to**: Extend only your thumb upward, keep other fingers closed
   - **Sign ID**: 8

3. **Bad** 👎
   - **Gesture**: Thumbs down
   - **How to**: Point your thumb downward, keep other fingers closed
   - **Sign ID**: 9

4. **Yes** 👌
   - **Gesture**: OK sign (thumb and index finger form a circle)
   - **How to**: Touch your thumb and index finger together to form a circle, keep other fingers closed
   - **Sign ID**: 3

5. **Stop** ✋
   - **Gesture**: Closed fist
   - **How to**: Close all fingers into a fist
   - **Sign ID**: 10

6. **More** 👉
   - **Gesture**: Pointing with index finger
   - **How to**: Extend only your index finger, keep other fingers closed
   - **Sign ID**: 12

7. **Victory** ✌️
   - **Gesture**: Peace sign (V)
   - **How to**: Extend index and middle fingers, keep thumb, ring, and pinky closed
   - **Sign ID**: 20

8. **I Love You** 🤟
   - **Gesture**: Thumb, index, and pinky extended
   - **How to**: Extend thumb, index finger, and pinky; keep middle and ring fingers closed
   - **Sign ID**: 7

9. **Less** 
   - **Gesture**: Three fingers extended (index, middle, ring)
   - **How to**: Extend index, middle, and ring fingers; keep thumb and pinky closed
   - **Sign ID**: 13

10. **Water**
    - **Gesture**: Four fingers extended (all except thumb)
    - **How to**: Extend index, middle, ring, and pinky fingers; keep thumb closed
    - **Sign ID**: 14

### Letter Signs

11. **Letter A** 
    - **Gesture**: Fist with thumb on the side
    - **How to**: Close all fingers except thumb, which is positioned on the side
    - **Sign ID**: 21

12. **Letter B**
    - **Gesture**: All fingers extended except thumb
    - **How to**: Extend index, middle, ring, and pinky fingers together; keep thumb closed
    - **Sign ID**: 22

13. **Letter C**
    - **Gesture**: Curved hand (C shape)
    - **How to**: Form a C shape with thumb and index finger, moderate distance between them
    - **Sign ID**: 23

## Tips for Best Recognition

1. **Lighting**: Ensure good lighting so the camera can see your hand clearly
2. **Distance**: Keep your hand at a comfortable distance from the camera (not too close or too far)
3. **Background**: Use a plain background for better hand detection
4. **Stability**: Hold gestures steady for 1-2 seconds for recognition
5. **Clarity**: Make gestures clearly and distinctly
6. **Hand Position**: Keep your hand fully visible in the camera frame

## How to Use

1. Run the application: `python main.py`
2. Position your hand in front of the camera
3. Make one of the supported gestures
4. Hold the gesture for about 1 second
5. The recognized sign will appear on screen
6. The sign will be added to your sentence after holding it

## Controls

- **'q'**: Quit the application
- **'c'**: Clear the current sentence
- **'b'**: Remove the last word (backspace)

## Recognition Confidence

The system displays a confidence score (0.0 to 1.0) for each recognized gesture. Higher confidence (closer to 1.0) indicates more reliable recognition. If confidence is low, try:

- Adjusting your hand position
- Improving lighting conditions
- Making the gesture more clearly
- Holding the gesture longer

## Adding New Gestures

To add new gestures, you can:

1. Modify `gesture_recognizer.py` to add new gesture recognition logic
2. Update `sign_dictionary.json` to add new sign mappings
3. Train a machine learning model with `train_model.py` for more complex gestures

