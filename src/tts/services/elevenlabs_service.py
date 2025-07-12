from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError
from .base_service import BaseTTSService


class ElevenLabsService(BaseTTSService):
    """Service class for ElevenLabs text-to-speech functionality."""
    
    def __init__(self, config_manager):
        """Initialize the ElevenLabs service.
        
        Args:
            config_manager (ConfigManager): The configuration manager instance.
        """
        super().__init__(config_manager)
    
    def _initialize_client(self):
        """Initialize the ElevenLabs client with API key."""
        service_config = self.config_manager.get_service_config()
        api_key = service_config.get("api_key")
        if not api_key:
            self.client = None
        else:
            self.client = ElevenLabs(api_key=api_key)
    
    def get_character_usage(self):
        """Get character usage from ElevenLabs.
        
        Returns:
            tuple: A tuple containing (character_count, character_limit).
            
        Raises:
            RuntimeError: If there's an error retrieving usage information.
        """
        try:
            subscription = self.client.user.subscription.get()
            return subscription.character_count, subscription.character_limit
        except ApiError as e:
            raise RuntimeError(e.body['detail']['message'])
    
    def synthesize_speech(self, text):
        """Synthesize speech using ElevenLabs.
        
        Args:
            text (str): The text to convert to speech.
        
        Returns:
            Path: The path to the saved audio file.
            
        Raises:
            RuntimeError: If there's an error during synthesis.
        """
        if not self.is_initialized():
            raise RuntimeError("ElevenLabs client not initialized. Please check your API key.")
        
        tts_params = self.config_manager.get_service_config()
        output_file = self.get_output_file_path()

        try:
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=tts_params.get("voice_id"),
                model_id=tts_params.get("model_id"),
                output_format=tts_params.get("output_format"),
                voice_settings=tts_params.get("voice_settings")
            )

            # Write the audio stream to the file
            with open(output_file, "wb") as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
                        
        except ApiError as e:
            self.cleanup_output_file(output_file)
            raise RuntimeError(e.body['detail']['message'])

        return output_file
