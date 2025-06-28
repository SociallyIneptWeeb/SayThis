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

    def get_character_usage(self):
        """Retrieve character usage and limit from the ElevenLabs subscription.
        
        Returns:
            tuple: A tuple containing (character_count, character_limit).
        """
        try:
            subscription = self.client.user.subscription.get()
            return subscription.character_count, subscription.character_limit
        except ApiError as e:
            raise RuntimeError(e.body['detail']['message'])
    
    def synthesize_speech(self, text):
        """Convert text to speech and save to a file.
        
        Args:
            text (str): The text to convert to speech.
        
        Returns:
            Path: The path to the saved audio file.
        """
        tts_params = self.app.get_tts_parameters()
        output_file = Path(__file__).parent / 'data' / f"audio{tts_params['file_extension']}"
        
        audio = self.client.text_to_speech.convert(
            text=text,
            voice_id=tts_params["voice_id"],
            model_id=tts_params["model_id"],
            output_format=tts_params["output_format"],
        )

        try:
            # Write the audio stream to the file
            with open(output_file, "wb") as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
        except ApiError as e:
            output_file.unlink(missing_ok=True)
            raise RuntimeError(e.body['detail']['message'])

        return output_file
