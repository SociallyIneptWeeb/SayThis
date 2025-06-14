from tts import TextToSpeech
from ui import UI
from config_manager import ConfigManager


class Application:
    """Main application class that coordinates TTS engine and UI components."""
    
    def __init__(self):
        """Initialize the application with configuration manager and TTS engine."""
        self.config_manager = ConfigManager()
        self.tts_engine = TextToSpeech(self, self.config_manager.get_api_key())
    
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
    
    def get_api_key(self):
        """Get the current API key from configuration.
        
        Returns:
            str: The current API key, or empty string if not set.
        """
        return self.config_manager.get_api_key()
    
    def update_api_key(self, api_key):
        """Update the API key for the TTS engine.
        
        Args:
            api_key (str): The new API key to use.
        """
        self.config_manager.set_api_key(api_key)
        self.tts_engine.configure_api_key(api_key)
    
    def get_tts_parameters(self):
        """Get TTS parameters from configuration.
        
        Returns:
            dict: Dictionary containing TTS parameters.
        """
        return self.config_manager.get_tts_parameters()


def main():
    """Main entry point of the application."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
