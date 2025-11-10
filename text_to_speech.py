"""
Text-to-Speech Module
Provides text-to-speech functionality for sign language detection.
"""

import threading
import queue
import time


class TextToSpeech:
    """Text-to-speech engine for speaking detected signs."""
    
    def __init__(self, enabled=True, rate=150, volume=0.8, voice_id=None):
        """
        Initialize the Text-to-Speech engine.
        
        Args:
            enabled: Whether TTS is enabled
            rate: Speech rate (words per minute, default 150)
            volume: Speech volume (0.0 to 1.0, default 0.8)
            voice_id: Voice ID to use (None for default)
        """
        self.enabled = enabled
        self.rate = rate
        self.volume = volume
        self.voice_id = voice_id
        self.engine = None
        self.speech_queue = queue.Queue()
        self.speaking = False
        self.worker_thread = None
        self.stop_flag = False
        
        if self.enabled:
            self._initialize_engine()
            self._start_worker()
    
    def _initialize_engine(self):
        """Initialize the TTS engine."""
        try:
            import pyttsx3
            self.engine = pyttsx3.init()
            
            # Set speech rate
            self.engine.setProperty('rate', self.rate)
            
            # Set volume
            self.engine.setProperty('volume', self.volume)
            
            # Set voice if specified
            if self.voice_id is not None:
                voices = self.engine.getProperty('voices')
                if voices and self.voice_id < len(voices):
                    self.engine.setProperty('voice', voices[self.voice_id].id)
            
            print("Text-to-Speech engine initialized successfully")
            
        except ImportError:
            print("Warning: pyttsx3 not installed. TTS disabled.")
            print("Install it with: pip install pyttsx3")
            self.enabled = False
            self.engine = None
        except Exception as e:
            print(f"Warning: Failed to initialize TTS engine: {e}")
            print("TTS will be disabled.")
            self.enabled = False
            self.engine = None
    
    def _start_worker(self):
        """Start the worker thread for speech synthesis."""
        if not self.enabled or self.engine is None:
            return
        
        self.stop_flag = False
        self.worker_thread = threading.Thread(target=self._speech_worker, daemon=True)
        self.worker_thread.start()
    
    def _speech_worker(self):
        """Worker thread that processes speech queue."""
        while not self.stop_flag:
            try:
                # Get text from queue with timeout
                text = self.speech_queue.get(timeout=0.5)
                if text is None:  # Shutdown signal
                    break
                
                self.speaking = True
                try:
                    self.engine.say(text)
                    self.engine.runAndWait()
                except Exception as e:
                    print(f"Error during speech: {e}")
                finally:
                    self.speaking = False
                    self.speech_queue.task_done()
                    
            except queue.Empty:
                continue
            except Exception as e:
                print(f"Error in speech worker: {e}")
                self.speaking = False
    
    def speak(self, text, interrupt=False):
        """
        Speak the given text.
        
        Args:
            text: Text to speak
            interrupt: If True, clear queue and speak immediately
        """
        if not self.enabled or self.engine is None or not text:
            return
        
        if interrupt:
            # Clear queue and add new text
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                except queue.Empty:
                    break
        
        # Add text to queue
        try:
            self.speech_queue.put_nowait(text)
        except queue.Full:
            print("Speech queue is full, skipping...")
    
    def speak_async(self, text):
        """Speak text asynchronously (non-blocking)."""
        self.speak(text, interrupt=False)
    
    def stop(self):
        """Stop current speech and clear queue."""
        if self.engine is None:
            return
        
        try:
            self.engine.stop()
            while not self.speech_queue.empty():
                try:
                    self.speech_queue.get_nowait()
                except queue.Empty:
                    break
        except Exception as e:
            print(f"Error stopping speech: {e}")
    
    def is_speaking(self):
        """Check if currently speaking."""
        return self.speaking or not self.speech_queue.empty()
    
    def set_rate(self, rate):
        """Set speech rate (words per minute)."""
        self.rate = rate
        if self.engine:
            self.engine.setProperty('rate', rate)
    
    def set_volume(self, volume):
        """Set speech volume (0.0 to 1.0)."""
        self.volume = max(0.0, min(1.0, volume))
        if self.engine:
            self.engine.setProperty('volume', self.volume)
    
    def get_voices(self):
        """Get available voices."""
        if self.engine is None:
            return []
        
        try:
            voices = self.engine.getProperty('voices')
            return [(i, voice.name, voice.id) for i, voice in enumerate(voices)] if voices else []
        except Exception as e:
            print(f"Error getting voices: {e}")
            return []
    
    def set_voice(self, voice_id):
        """Set voice by ID."""
        if self.engine is None:
            return
        
        try:
            voices = self.engine.getProperty('voices')
            if voices and 0 <= voice_id < len(voices):
                self.engine.setProperty('voice', voices[voice_id].id)
                self.voice_id = voice_id
        except Exception as e:
            print(f"Error setting voice: {e}")
    
    def shutdown(self):
        """Shutdown the TTS engine."""
        self.stop_flag = True
        self.stop()
        if self.worker_thread and self.worker_thread.is_alive():
            # Send shutdown signal
            try:
                self.speech_queue.put_nowait(None)
            except:
                pass
            self.worker_thread.join(timeout=1.0)
        
        if self.engine:
            try:
                self.engine.stop()
            except:
                pass
            self.engine = None


# Global TTS instance
_tts_instance = None


def get_tts(enabled=True, rate=150, volume=0.8, voice_id=None):
    """
    Get or create a global TTS instance.
    
    Args:
        enabled: Whether TTS is enabled
        rate: Speech rate
        volume: Speech volume
        voice_id: Voice ID
        
    Returns:
        TextToSpeech instance
    """
    global _tts_instance
    if _tts_instance is None:
        _tts_instance = TextToSpeech(enabled=enabled, rate=rate, volume=volume, voice_id=voice_id)
    return _tts_instance

