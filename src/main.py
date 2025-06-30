from tts import TextToSpeech
from ui import UI
from config_manager import ConfigManager


class Application:
    """Main application class that coordinates TTS engine and UI components."""
    
    def __init__(self):
        """Initialize the application with configuration manager and TTS engine."""
        self.config_manager = ConfigManager()
        self.tts_engine = TextToSpeech(self, self.config_manager)
    
    def run(self):
        """Run the application with GUI."""
        ui = UI(self)
        ui.run()
    
    def generate_audio(self, message):
        """Convert the provided message to speech and save to a file.
        
        Args:
            message (str): The text message to convert to speech
            
        Returns:
            Path: The path to the saved audio file.
        """
        return self.tts_engine.synthesize_speech(message)
    
    def get_character_usage(self):
        """Get character usage information from the TTS engine.
        
        Returns:
            tuple: A tuple containing (character_count, character_limit).
            
        Raises:
            RuntimeError: If there's an error retrieving usage information.
        """
        return self.tts_engine.get_character_usage()
    
    def get_selected_service(self):
        """Get the currently selected TTS service.
        
        Returns:
            str: The name of the selected service
        """
        return self.config_manager.get_selected_service()
    
    def set_selected_service(self, service):
        """Set the selected TTS service and reinitialize TTS engine.
        
        Args:
            service (str): The service name to select
        """
        self.config_manager.set_selected_service(service)
        self.tts_engine.initialize_service()

    def get_service_config(self):
        """Get the configuration for the currently selected TTS service.
        
        Returns:
            dict: The configuration parameters for the service
        """
        return self.config_manager.get_service_config()
    
    def set_service_config(self, service_config):
        """Set configuration for the currently selected TTS service.
        
        Args:
            service_config (dict): Configuration parameters to set for the service
        """
        self.config_manager.set_service_config(service_config)
        self.tts_engine.initialize_service()


def main():
    """Main entry point of the application."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
