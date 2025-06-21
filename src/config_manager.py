import json
from pathlib import Path


class ConfigManager:
    """Manages application configuration, including API key storage."""
    
    def __init__(self):
        """Initialize the configuration manager."""
        self.config_filepath = Path(__file__).parent / "data" / "config.json"
        
        # Default configuration
        self.default_config = {
            "api_key": "",
            "voice_id": "JBFqnCBsd6RMkjVDRZzb",
            "model_id": "eleven_multilingual_v2",
            "output_format": "mp3_22050_32",
            "file_extension": ".mp3"
        }
    
    def load_config(self):
        """Load configuration from file.
        
        Returns:
            dict: Configuration dictionary
        """
        default_config = self.default_config.copy()
        if not self.config_filepath.exists():
            # Create default config if file doesn't exist
            self.save_config(self.default_config)
            return default_config
        
        try:
            with open(self.config_filepath, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # Merge with defaults to ensure all keys exist
            merged_config = default_config
            merged_config.update(config)
            return merged_config
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            # If config file is corrupted, return defaults
            print(f"Warning: Could not load config file ({e}). Using defaults.")
            return default_config
    
    def save_config(self, config):
        """Save configuration to file.
        
        Args:
            config (dict): Configuration dictionary to save
        """
        with open(self.config_filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=4)

    def get_tts_parameters(self):
        """Get all TTS parameters at once.
        
        Returns:
            dict: Dictionary containing voice_id, model_id, output_format, and file_extension
        """
        config = self.load_config()
        return {
            "voice_id": config.get("voice_id"),
            "model_id": config.get("model_id"),
            "output_format": config.get("output_format"),
            "file_extension": config.get("file_extension")
        }

    def get_api_key(self):
        """Get the API key from configuration.
        
        Returns:
            str: The API key
        """
        return self.get_setting("api_key")
    
    def set_api_key(self, api_key):
        """Set the API key in configuration.
        
        Args:
            api_key (str): The API key to save
        """
        self.set_setting("api_key", api_key)
    
    def get_setting(self, key):
        """Get a configuration setting.
        
        Args:
            key (str): The configuration key
            
        Returns:
            The configuration value
        """
        config = self.load_config()
        return config.get(key)
    
    def set_setting(self, key, value):
        """Set a configuration setting.
        
        Args:
            key (str): The configuration key
            value: The value to set
        """
        config = self.load_config()
        config[key] = value
        self.save_config(config)
