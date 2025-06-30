from elevenlabs.client import ElevenLabs
from elevenlabs.core.api_error import ApiError


class ElevenLabsService:
    """Service class for ElevenLabs text-to-speech functionality."""
    
    def __init__(self, config_manager):
        """Initialize the ElevenLabs service.
        
        Args:
            config_manager (ConfigManager): The configuration manager instance.
        """
        self.config_manager = config_manager
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the ElevenLabs client with API key."""
        service_config = self.config_manager.get_service_config()
        api_key = service_config.get("api_key")
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
        tts_params = self.config_manager.get_service_config()
        output_file = self.config_manager.get_data_dir() / f"audio{tts_params.get('file_extension')}"

        try:
            audio = self.client.text_to_speech.convert(
                text=text,
                voice_id=tts_params.get("voice_id"),
                model_id=tts_params.get("model_id"),
                output_format=tts_params.get("output_format"),
            )

            # Write the audio stream to the file
            with open(output_file, "wb") as f:
                for chunk in audio:
                    if chunk:
                        f.write(chunk)
                        
        except ApiError as e:
            output_file.unlink(missing_ok=True)
            raise RuntimeError(e.body['detail']['message'])

        return output_file
