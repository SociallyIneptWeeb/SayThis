from pathlib import Path

from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError


class TextToSpeech:
    """Class for handling text-to-speech conversion using ElevenLabs API."""
    
    def __init__(self, app, api_key):
        """Initialize the TTS engine with ElevenLabs.
        
        Args:
            app (Application): The application instance.
            api_key (str): The API key for ElevenLabs.
        """
        self.app = app
        self.client = ElevenLabs(api_key=api_key)

    def configure_api_key(self, api_key):
        """Reinitialize the client with the new API key.
        
        Args:
            api_key (str): The new API key to use.
        """
        self.client = ElevenLabs(api_key=api_key)
    
    def synthesize_speech(self, text):
        """Convert text to speech and save to a file.
        
        Args:
            text (str): The text to convert to speech.
        
        Returns:
            Path: The path to the saved audio file.
        """
        tts_params = self.app.get_tts_parameters()
        
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=tts_params["voice_id"],
            model_id=tts_params["model_id"],
            output_format=tts_params["output_format"],
        )
        
        output_file = Path(__file__).parent / 'data' / f"audio{tts_params['file_extension']}"

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
