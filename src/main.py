from tts import TextToSpeech
from ui import UI


class Application:
    def __init__(self):
        self.tts_engine = TextToSpeech()
    
    def run(self):
        """Run the application with GUI."""
        # Create and start the GUI
        gui = UI(self)
        gui.run()
    
    def generate_audio(self, message):
        """Convert the provided message to speech and save to a file.
        
        Args:
            message (str): The text message to convert to speech
            
        Returns:
            Path: The path to the saved audio file.
        """
        return self.tts_engine.synthesize_speech(message)


def main():
    """Main entry point of the application."""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
