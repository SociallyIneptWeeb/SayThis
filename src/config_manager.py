import json
from pathlib import Path


class ConfigManager:
    """Manages application configuration, including API key storage."""
    
    def __init__(self):
        """Initialize the configuration manager."""
        self.data_dir = Path.home() / ".saythis"
        self.config_filepath = self.data_dir / "config.json"
        
        # Ensure the data directory exists
        self.data_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.default_config = {
            "selected_service": "ElevenLabs",
            "ElevenLabs": {
                "api_key": "",
                "voice_id": "JBFqnCBsd6RMkjVDRZzb",
                "model_id": "eleven_turbo_v2_5",
                "output_format": "mp3_22050_32",
                "file_extension": ".mp3"
            },
            "IBM Watson": {
                "api_key": "",
                "file_extension": ".wav"
            }
        }
        self.selected_service = self.default_config["selected_service"]

        self.load_config()

    def get_data_dir(self):
        """Get the data directory path.
        
        Returns:
            Path: The data directory path
        """
        return self.data_dir
    
    def load_config(self):
        """Load configuration from file.
        
        Returns:
            dict: Configuration dictionary
        """
        if not self.config_filepath.exists():
            # Create default config if file doesn't exist
            self.save_config(self.default_config)
            self.selected_service = self.default_config["selected_service"]
            return self.default_config
        
        try:
            with open(self.config_filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.selected_service = config.get("selected_service")
            return config
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            # If config file is corrupted, return defaults
            print(f"Warning: Could not load config file ({e}). Using defaults.")
            self.selected_service = self.default_config["selected_service"]
            return self.default_config
    
    def save_config(self, config):
        """Save configuration to file.
        
        Args:
            config (dict): Configuration dictionary to save
        """
        with open(self.config_filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)
    
    def get_selected_service(self):
        """Get the currently selected TTS service.
        
        Returns:
            str: The name of the selected service
        """
        return self.selected_service
    
    def set_selected_service(self, service):
        """Set the selected TTS service.
        
        Args:
            service (str): The service name to select ("ElevenLabs" or "IBM Watson")
        """
        config = self.load_config()
        config["selected_service"] = service
        self.selected_service = service
        self.save_config(config)

    def get_service_config(self):
        """Get configuration for the currently selected service.
            
        Returns:
            dict: The service configuration
        """
        config = self.load_config()
        return config.get(self.selected_service)
    
    def set_service_config(self, service_config):
        """Set configuration for the selected service.
        
        Args:
            service_config (dict): Configuration to set
        """
        config = self.load_config()
        config[self.selected_service] = service_config
        self.save_config(config)
