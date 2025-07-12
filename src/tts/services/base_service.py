from abc import ABC, abstractmethod
from pathlib import Path


class BaseTTSService(ABC):
    """Abstract base class for text-to-speech services."""
    
    def __init__(self, config_manager):
        """Initialize the TTS service.
        
        Args:
            config_manager (ConfigManager): The configuration manager instance.
        """
        self.config_manager = config_manager
        self.client = None
        self._initialize_client()
    
    @abstractmethod
    def _initialize_client(self):
        """Initialize the service client.
        
        This method must be implemented by each service to set up
        their specific client with appropriate credentials.
        """
        pass
    
    @abstractmethod
    def get_character_usage(self):
        """Get character usage from the TTS service.
        
        Returns:
            tuple: A tuple containing (character_count, character_limit).
                  Return (-1, -1) if usage tracking is not available.
            
        Raises:
            RuntimeError: If there's an error retrieving usage information.
        """
        pass
    
    @abstractmethod
    def synthesize_speech(self, text):
        """Synthesize speech using the TTS service.
        
        Args:
            text (str): The text to convert to speech.
        
        Returns:
            Path: The path to the saved audio file.
            
        Raises:
            RuntimeError: If there's an error during synthesis.
        """
        pass
    
    def is_initialized(self):
        """Check if the service client is properly initialized.
        
        Returns:
            bool: True if the client is initialized, False otherwise.
        """
        return self.client is not None
    
    def get_output_file_path(self, file_extension=None):
        """Get the output file path for audio files.
        
        Args:
            file_extension (str, optional): File extension to use.
                                          If None, gets from service config.
        
        Returns:
            Path: The path where the audio file should be saved.
        """
        if file_extension is None:
            tts_params = self.config_manager.get_service_config()
            file_extension = tts_params.get('file_extension', '.mp3')
        
        return self.config_manager.get_data_dir() / f"audio{file_extension}"
    
    def cleanup_output_file(self, output_file):
        """Clean up the output file in case of errors.
        
        Args:
            output_file (Path): The path to the file to clean up.
        """
        if isinstance(output_file, (str, Path)):
            Path(output_file).unlink(missing_ok=True)
