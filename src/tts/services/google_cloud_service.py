from pathlib import Path
from google.cloud import texttospeech
from .base_service import BaseTTSService


class GoogleCloudService(BaseTTSService):
    """Service class for Google Cloud text-to-speech functionality."""
    
    def __init__(self, config_manager):
        """Initialize the Google Cloud service.
        
        Args:
            config_manager (ConfigManager): The configuration manager instance.
        """
        super().__init__(config_manager)
    
    def _initialize_client(self):
        """Initialize the Google Cloud TTS client with service account JSON file path."""
        service_config = self.config_manager.get_service_config()
        service_account_json_path = service_config.get("service_account_json_path")

        try:
            self.client = texttospeech.TextToSpeechClient.from_service_account_json(service_account_json_path)
        except Exception as e:
            self.client = None

    def get_character_usage(self):
        """Get character usage from Google Cloud TTS.
        
        Note: Google Cloud TTS doesn't provide real-time usage statistics.
        This returns -1, -1 to indicate usage tracking is not available.
        
        Returns:
            tuple: A tuple containing (-1, -1) to indicate no usage tracking.
        """
        # Google Cloud TTS pricing is pay-per-use without usage tracking
        return -1, -1
    
    def synthesize_speech(self, text):
        """Synthesize speech using Google Cloud TTS.
        
        Args:
            text (str): The text to convert to speech.
        
        Returns:
            Path: The path to the saved audio file.
            
        Raises:
            RuntimeError: If there's an error during synthesis.
        """
        if not self.is_initialized():
            raise RuntimeError("Google Cloud TTS client could not be initialized. Please check your service account JSON file path.")

        output_file = self.get_output_file_path()

        try:
            tts_params = self.config_manager.get_service_config()
            
            # Set the text input to be synthesized
            synthesis_input = texttospeech.SynthesisInput(text=text)
            
            # Build the voice request
            voice = texttospeech.VoiceSelectionParams(
                language_code=tts_params.get("language_code"),
                name=tts_params.get("voice_name"),
                ssml_gender=getattr(texttospeech.SsmlVoiceGender, tts_params.get("voice_gender"))
            )
            
            # Select the type of audio file you want returned
            audio_config = texttospeech.AudioConfig(
                audio_encoding=getattr(texttospeech.AudioEncoding, tts_params.get("audio_encoding")),
                speaking_rate=tts_params.get("speaking_rate"),
                pitch=tts_params.get("pitch"),
                volume_gain_db=tts_params.get("volume_gain_db")
            )
            
            # Perform the text-to-speech request
            response = self.client.synthesize_speech(
                input=synthesis_input, voice=voice, audio_config=audio_config
            )
            
            # Save the audio to a file
            with open(output_file, "wb") as out:
                out.write(response.audio_content)
            
            return output_file
            
        except Exception as e:
            self.cleanup_output_file(output_file)
            raise RuntimeError(f"Error during Google Cloud TTS synthesis: {str(e)}")
