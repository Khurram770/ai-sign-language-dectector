# Quick Start Guide

## Installation

1. **Navigate to the project directory:**
   ```bash
   cd sign-language-detector
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Basic Usage

Run the main application:
```bash
python main.py
```

**Note:** The application uses gesture-based recognition (no training required). It recognizes signs in real-time based on hand landmark analysis.

### Test Hand Detection

Test if your camera and hand detection are working:
```bash
python test_detection.py
```

### Train Your Own Model (Optional)

1. **Collect training data:**
   ```bash
   python train_model.py
   ```
   Follow the interactive prompts to collect data for different signs.

2. **The model will be automatically trained** after collecting data for multiple signs.

## Hand Gesture Usage Guide

### Getting Started

1. **Start the application**: Run `python main.py`
2. **Position yourself**: Sit or stand in front of your camera with good lighting
3. **Show your hand**: Hold your hand in front of the camera so it's fully visible
4. **Make a gesture**: Use one of the supported gestures below
5. **Hold steady**: Keep the gesture for about 1 second for recognition
6. **See results**: The recognized sign will appear on screen and be added to your sentence

### Setup Tips for Best Results

- **Lighting**: Use bright, even lighting. Avoid backlighting or shadows on your hand
- **Distance**: Keep your hand 30-60 cm (12-24 inches) from the camera
- **Background**: Use a plain, contrasting background (avoid busy patterns)
- **Camera angle**: Position camera so your hand is centered in the frame
- **Stability**: Hold gestures steady for 1-2 seconds

### Supported Gestures - Step by Step

#### 1. Hello 👋
**How to make it:**
- Extend all five fingers straight out
- Keep your palm facing the camera
- Spread fingers slightly apart
- Hold for 1 second

**Visual**: Open hand with all fingers extended upward

---

#### 2. Good 👍
**How to make it:**
- Make a fist with your four fingers (index, middle, ring, pinky)
- Extend only your thumb upward
- Keep thumb pointing straight up
- Hold for 1 second

**Visual**: Fist with thumb pointing up

---

#### 3. Bad 👎
**How to make it:**
- Make a fist with your four fingers
- Point your thumb downward
- Keep thumb pointing straight down
- Hold for 1 second

**Visual**: Fist with thumb pointing down

---

#### 4. Yes 👌 (OK Sign)
**How to make it:**
- Touch your thumb tip to your index finger tip to form a circle
- Keep your middle, ring, and pinky fingers closed/curled
- The circle should be visible to the camera
- Hold for 1 second

**Visual**: Thumb and index finger form an "O" shape, other fingers closed

---

#### 5. Stop ✋ (Fist)
**How to make it:**
- Close all fingers into a tight fist
- Keep thumb over your fingers (not extended)
- Make sure all fingers are clearly closed
- Hold for 1 second

**Visual**: Closed fist with all fingers curled

---

#### 6. More 👉 (Pointing)
**How to make it:**
- Extend only your index finger straight out
- Keep thumb, middle, ring, and pinky fingers closed
- Point index finger forward or slightly up
- Hold for 1 second

**Visual**: Index finger extended, other fingers closed

---

#### 7. Victory ✌️ (Peace Sign)
**How to make it:**
- Extend your index and middle fingers straight up
- Keep them spread apart (forming a "V")
- Keep thumb, ring, and pinky fingers closed
- Hold for 1 second

**Visual**: Index and middle fingers form a "V", other fingers closed

---

#### 8. I Love You 🤟
**How to make it:**
- Extend your thumb, index finger, and pinky finger
- Keep your middle and ring fingers closed/curled down
- Spread the extended fingers slightly
- Hold for 1 second

**Visual**: Thumb, index, and pinky extended; middle and ring closed

---

#### 9. Less (Three Fingers)
**How to make it:**
- Extend your index, middle, and ring fingers
- Keep thumb and pinky closed
- Keep the three extended fingers together
- Hold for 1 second

**Visual**: Three fingers (index, middle, ring) extended upward

---

#### 10. Water (Four Fingers)
**How to make it:**
- Extend your index, middle, ring, and pinky fingers
- Keep thumb closed/curled
- Keep the four extended fingers together
- Hold for 1 second

**Visual**: Four fingers extended, thumb closed

---

### Letter Signs

#### 11. Letter A
**How to make it:**
- Make a fist with all fingers closed
- Position your thumb against the side of your fist (not extended outward)
- Keep thumb close to your index finger
- Hold for 1 second

**Visual**: Fist with thumb pressed against the side

---

#### 12. Letter B
**How to make it:**
- Extend your index, middle, ring, and pinky fingers straight up
- Keep fingers together (touching)
- Keep thumb closed against your palm
- Hold for 1 second

**Visual**: Four fingers extended together, thumb closed

---

#### 13. Letter C
**How to make it:**
- Curve your thumb and index finger to form a "C" shape
- Keep a moderate gap between thumb and index (about 2-3 cm)
- Keep middle, ring, and pinky fingers closed
- Hold for 1 second

**Visual**: Thumb and index form a curved "C" shape

---

### Practice Tips

1. **Start Simple**: Begin with easy gestures like "Hello" (open hand) or "Stop" (fist)
2. **Check Recognition**: Watch the confidence score on screen (aim for >0.7)
3. **Adjust Position**: If not recognized, try adjusting hand distance or angle
4. **Be Patient**: Hold gestures steady for the full 1 second
5. **Practice**: Try each gesture multiple times to get comfortable

### Troubleshooting Gesture Recognition

**If a gesture is not recognized:**

1. **Check lighting**: Ensure your hand is well-lit without shadows
2. **Adjust distance**: Move hand closer or further from camera
3. **Clear background**: Make sure background isn't distracting
4. **Hold steady**: Keep gesture stable for full duration
5. **Make it clear**: Ensure gesture matches the description exactly
6. **Check confidence**: Look at confidence score - if low (<0.5), adjust position

**Common Issues:**

- **"Hand not detected"**: Move hand closer to camera, improve lighting
- **"Low confidence"**: Make gesture more clearly, hold steadier
- **"Wrong sign detected"**: Ensure gesture matches description exactly
- **"Flickering detection"**: Hold gesture more steadily

### Building Sentences

1. Make your first gesture and hold for 1 second
2. Wait for it to be added to the sentence (you'll see it appear)
3. Make your next gesture and hold for 1 second
4. Continue adding gestures to build your sentence
5. Use 'c' key to clear the sentence
6. Use 'b' key to remove the last word

### Example Usage Session

```
1. Start application: python main.py
2. Show "Hello" gesture → "Hello" appears on screen
3. Hold for 1 second → "Hello" added to sentence
4. Show "Good" gesture → "Good" appears on screen
5. Hold for 1 second → "Good" added to sentence
6. Sentence now shows: "Hello Good"
7. Press 'c' to clear and start over
```

## Controls

When running the main application:

- **Show your hand** to the camera to detect signs
- **Press 'q'** to quit
- **Press 'c'** to clear the current sentence
- **Press 'b'** to remove the last word (backspace)
- **Press 't'** to toggle text-to-speech on/off

### Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `c` | Clear the current sentence |
| `b` | Backspace (remove last word) |
| `t` | Toggle text-to-speech on/off |

### Text-to-Speech (TTS)

The application can speak out detected signs:

- **Automatic**: When a sign is recognized and added to your sentence, it's automatically spoken
- **Toggle**: Press 't' key to enable/disable TTS during runtime
- **Status**: TTS status is displayed on screen (green = ON, red = OFF)
- **Volume**: Adjust TTS volume and rate in `main.py` if needed

## How It Works

1. **Hand Detection**: The system uses MediaPipe to detect and track 21 hand landmarks in real-time
2. **Finger Analysis**: Analyzes which fingers are extended or closed
3. **Gesture Recognition**: Rule-based system matches finger patterns to known gestures
4. **Text Conversion**: The recognized gesture is converted to English text
5. **Sentence Building**: Gestures are combined to form sentences when held for 1 second

## Customization

### Adding New Signs

1. Edit `sign_dictionary.json` to add new sign mappings:
   ```json
   {
     "30": "New Sign"
   }
   ```

2. Collect training data for the new sign using `train_model.py`

3. Retrain the model with the new data

### Adjusting Confidence Threshold

In `main.py`, modify the `confidence_threshold` variable:
```python
confidence_threshold = 0.4  # Increase for stricter recognition
```

### Adjusting Sign Hold Duration

In `main.py`, modify the `sign_hold_duration` variable:
```python
sign_hold_duration = 1.0  # Seconds to hold sign before adding to sentence
```

## Troubleshooting

### Camera not working
- Make sure your camera is connected and not being used by another application
- Try changing the camera index in `main.py`: `cap = cv2.VideoCapture(0)` to `cap = cv2.VideoCapture(1)`
- Check camera permissions in your system settings
- Restart the application

### Poor recognition accuracy
- **Improve lighting**: Use bright, even lighting without shadows
- **Adjust distance**: Keep hand 30-60 cm from camera
- **Clear background**: Use plain background
- **Hold steady**: Keep gestures stable for full duration
- **Make gestures clearly**: Ensure gestures match descriptions exactly
- **Check confidence score**: Aim for confidence > 0.7
- Adjust the confidence threshold in `main.py` if needed

### Hand not detected
- Move hand closer to camera
- Improve lighting conditions
- Ensure hand is fully visible in frame
- Check camera is working (test with `test_detection.py`)
- Try different hand positions

### Wrong sign detected
- Review gesture instructions in this guide
- Make gesture more clearly and distinctly
- Ensure all fingers are in correct positions
- Hold gesture steadier
- Check if gesture matches supported signs

### Model not found error
- This should not occur with gesture-based recognition (no model needed)
- If using ML model, train your own model using `train_model.py`

## Next Steps

1. **Practice gestures**: Start with basic gestures (Hello, Good, Stop) and work your way up
2. **Build sentences**: Try combining multiple gestures to form sentences
3. **Customize**: Adjust confidence threshold and hold duration in `main.py`
4. **Add new gestures**: Modify `gesture_recognizer.py` to add new gesture recognition
5. **Train ML model** (optional): Use `train_model.py` to train a machine learning model for more complex gestures
6. **Extend functionality**: Add more features like gesture history, export sentences, etc.

## Quick Reference

### Most Common Gestures

| Gesture | How to Make | Hold Time |
|---------|-------------|-----------|
| Hello | Open hand, all fingers extended | 1 second |
| Good | Thumbs up | 1 second |
| Yes | OK sign (thumb + index circle) | 1 second |
| Stop | Closed fist | 1 second |
| More | Point with index finger | 1 second |

### Recognition Tips

- ✅ Good lighting
- ✅ Plain background
- ✅ Steady hand position
- ✅ Clear, distinct gestures
- ✅ Hold for full duration
- ❌ Avoid shadows
- ❌ Avoid busy backgrounds
- ❌ Don't move hand quickly
- ❌ Don't make partial gestures

## Support

For issues or questions, please refer to the main README.md file.

