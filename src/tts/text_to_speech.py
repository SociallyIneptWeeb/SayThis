from .services.elevenlabs_service import ElevenLabsService
from .services.ibm_watson_service import IBMWatsonService


class TextToSpeech:
    """Class for handling text-to-speech conversion using multiple TTS services."""
    
    def __init__(self, app, config_manager):
        """Initialize the TTS engine.
        
        Args:
            app (Application): The application instance.
            config_manager (ConfigManager): The configuration manager instance.
        """
        self.app = app
        self.config_manager = config_manager
        self.service_instance = None
        self.initialize_service()

    def initialize_service(self):
        """Initialize the appropriate service client."""
        selected_service = self.config_manager.get_selected_service()

        if selected_service == "ElevenLabs":
            self.service_instance = ElevenLabsService(self.config_manager)
        elif selected_service == "IBM Watson":
            self.service_instance = IBMWatsonService(self.config_manager)
        else:
            raise ValueError(f"Unsupported TTS service: {selected_service}")

    def get_character_usage(self):
        """Retrieve character usage and limit from the current TTS service.
        
        Returns:
            tuple: A tuple containing (character_count, character_limit).
        """
        return self.service_instance.get_character_usage()

    def synthesize_speech(self, text):
        """Convert text to speech and save to a file.
        
        Args:
            text (str): The text to convert to speech.
        
        Returns:
            Path: The path to the saved audio file.
        """
        return self.service_instance.synthesize_speech(text)
