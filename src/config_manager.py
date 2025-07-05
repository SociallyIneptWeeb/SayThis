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

    def _merge_with_defaults(self, loaded_config):
        """Merge loaded config with default config for backwards compatibility.
        
        Args:
            loaded_config (dict): The configuration loaded from file
            
        Returns:
            dict: Merged configuration with defaults filled in
        """
        def deep_merge(default, loaded):
            """Recursively merge two dictionaries."""
            merged = default.copy()
            
            for key, value in loaded.items():
                if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
                    # Recursively merge nested dictionaries
                    merged[key] = deep_merge(merged[key], value)
                else:
                    # Use loaded value for non-dict values or new keys
                    merged[key] = value
            
            return merged
        
        return deep_merge(self.default_config, loaded_config)

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
            
            # Merge with defaults for backwards compatibility
            merged_config = self._merge_with_defaults(config)
            
            # Save the merged config if it was updated
            if merged_config != config:
                self.save_config(merged_config)

            self.selected_service = merged_config["selected_service"]
            return merged_config
            
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
