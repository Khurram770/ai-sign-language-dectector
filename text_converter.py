"""
Text Conversion Module
Manages conversion of recognized signs to English text and sentence building.
"""

import json
import os


class TextConverter:
    def __init__(self, sign_dict_path="sign_dictionary.json"):
        """
        Initialize the TextConverter.
        
        Args:
            sign_dict_path: Path to sign dictionary JSON file
        """
        self.sign_dict = self.load_sign_dictionary(sign_dict_path)
        self.current_sentence = []
        self.history = []
    
    def load_sign_dictionary(self, dict_path):
        """Load sign dictionary from JSON file."""
        try:
            with open(dict_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Sign dictionary not found at {dict_path}")
            return {}
    
    def add_sign(self, sign_text, min_confidence=0.5, confidence=1.0):
        """
        Add a recognized sign to the current sentence.
        
        Args:
            sign_text: The recognized sign text
            min_confidence: Minimum confidence to accept the sign
            confidence: Confidence of the recognition
            
        Returns:
            bool: True if sign was added, False otherwise
        """
        if sign_text and confidence >= min_confidence:
            # Avoid adding duplicate consecutive signs
            if not self.current_sentence or self.current_sentence[-1] != sign_text:
                self.current_sentence.append(sign_text)
                return True
        return False
    
    def get_current_sentence(self):
        """Get the current sentence as a string."""
        return " ".join(self.current_sentence)
    
    def clear_sentence(self):
        """Clear the current sentence."""
        if self.current_sentence:
            self.history.append(" ".join(self.current_sentence))
        self.current_sentence = []
    
    def get_history(self):
        """Get the history of all sentences."""
        return self.history
    
    def remove_last_word(self):
        """Remove the last word from the current sentence."""
        if self.current_sentence:
            self.current_sentence.pop()
    
    def convert_sign_to_text(self, sign_id):
        """
        Convert a sign ID to text.
        
        Args:
            sign_id: The sign ID
            
        Returns:
            text: The corresponding text or None
        """
        sign_key = str(sign_id)
        if sign_key in self.sign_dict:
            return self.sign_dict[sign_key]
        return None
    
    def format_output(self, current_sign=None, confidence=0.0):
        """
        Format the output for display.
        
        Args:
            current_sign: Currently recognized sign
            confidence: Confidence of recognition
            
        Returns:
            formatted_text: Formatted output string
        """
        output_lines = []
        
        if current_sign:
            output_lines.append(f"Sign: {current_sign} ({confidence:.2f})")
        
        sentence = self.get_current_sentence()
        if sentence:
            output_lines.append(f"Sentence: {sentence}")
        
        if self.history:
            output_lines.append(f"History: {' | '.join(self.history[-3:])}")
        
        return "\n".join(output_lines)

