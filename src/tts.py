import uuid
from pathlib import Path

from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError


class TextToSpeech:
    """Class for handling text-to-speech conversion using ElevenLabs API."""
    
    # API Constants
    DEFAULT_API_KEY = "YOUR-API-KEY"  # Replace with your actual API key
    DEFAULT_VOICE_ID = "JBFqnCBsd6RMkjVDRZzb"
    DEFAULT_MODEL_ID = "eleven_multilingual_v2"
    DEFAULT_OUTPUT_FORMAT = "mp3_22050_32"
    DEFAULT_FILE_EXTENSION = ".mp3"
    
    def __init__(self, voice_id=None, model_id=None, output_format=None):
        """Initialize the TTS engine with ElevenLabs.
        
        Args:
            voice_id (str, optional): ID of the voice to use.
            model_id (str, optional): ID of the model to use.
            output_format (str, optional): Format of the output audio.
        """
        # Initialize ElevenLabs client
        self.client = ElevenLabs(api_key=self.DEFAULT_API_KEY)
        
        # Default configuration
        self.voice_id = voice_id or self.DEFAULT_VOICE_ID
        self.model_id = model_id or self.DEFAULT_MODEL_ID
        self.output_format = output_format or self.DEFAULT_OUTPUT_FORMAT
    
    def configure_voice(self, voice_id):
        """Configure the voice to use.
        
        Args:
            voice_id (str): ID of the voice to use.
        """
        self.voice_id = voice_id
    
    def configure_model(self, model_id):
        """Configure the model to use.
        
        Args:
            model_id (str): ID of the model to use.
        """
        self.model_id = model_id
    
    def configure_output_format(self, output_format):
        """Configure the output format.
        
        Args:
            output_format (str): Format of the output audio.
        """
        self.output_format = output_format
    
    def synthesize_speech(self, text, output_path=None):
        """Convert text to speech and save to a file.
        
        Args:
            text (str): The text to convert to speech.
            output_path (str, optional): The path to save the audio file.
                                         If None, a UUID-based filename will be used.
        
        Returns:
            Path: The path to the saved audio file.
        """
        # Generate audio stream from text
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            model_id=self.model_id,
            output_format=self.output_format,
        )
        
        # Generate a unique filename if not provided
        if output_path is None:
            output_path = f"{uuid.uuid4()}{self.DEFAULT_FILE_EXTENSION}"
        
        # Create a Path object for the output file
        output_file = Path(output_path)

        try:
            # Write the audio stream to the file
            with open(output_file, "wb") as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
        except ApiError as e:
            Path.unlink(output_file, missing_ok=True)
            raise RuntimeError(e.body['detail']['message'])

        return output_file


# Example usage if this file is run directly
if __name__ == "__main__":
    TEST_MESSAGE = "This is a test from ElevenLabs TTS."
    
    tts = TextToSpeech()
    tts.synthesize_speech(TEST_MESSAGE)
