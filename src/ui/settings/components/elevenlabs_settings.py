import tkinter as tk
from tkinter import ttk
from ...constants import UIConstants


class ElevenLabsSettings:
    """Component for ElevenLabs-specific settings."""
    
    def __init__(self, parent, app):
        """Initialize the ElevenLabs settings component.
        
        Args:
            parent: The parent widget to contain this component
            app: The Application instance
        """
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the ElevenLabs settings widgets."""
        # API Key Configuration Section
        api_frame = ttk.Frame(self.frame)
        api_frame.pack(pady=10, fill=tk.X)
        
        # API Key label and entry
        ttk.Label(api_frame, text="ElevenLabs API Key:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        # API Key entry field
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(
            api_frame,
            textvariable=self.api_key_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            show=UIConstants.API_KEY_ENTRY_SHOW_CHAR,
            width=40
        )
        self.api_key_entry.pack(anchor=tk.W)
        
        # Voice ID Configuration Section
        voice_frame = ttk.Frame(self.frame)
        voice_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(voice_frame, text="Voice ID:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        self.voice_id_var = tk.StringVar()
        voice_id_entry = ttk.Entry(
            voice_frame,
            textvariable=self.voice_id_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=40
        )
        voice_id_entry.pack(anchor=tk.W)
        
        # Model ID Configuration Section
        model_frame = ttk.Frame(self.frame)
        model_frame.pack(pady=10, fill=tk.X)
        
        # Model ID label and entry
        ttk.Label(model_frame, text="Model ID:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        # Model ID dropdown field
        self.model_id_var = tk.StringVar()
        self.model_id_dropdown = ttk.Combobox(
            model_frame,
            textvariable=self.model_id_var,
            values=["eleven_turbo_v2_5", "eleven_flash_v2_5", "eleven_multilingual_v2", "eleven_v3"],
            state="readonly",
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=38
        )
        self.model_id_dropdown.pack(anchor=tk.W)
        
        # Output Format Configuration Section
        output_frame = ttk.Frame(self.frame)
        output_frame.pack(pady=10, fill=tk.X)
        
        # Output Format label and dropdown
        ttk.Label(output_frame, text="Output Format:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        # Output Format dropdown field
        self.output_format_var = tk.StringVar()
        self.output_format_dropdown = ttk.Combobox(
            output_frame,
            textvariable=self.output_format_var,
            values=[
                "mp3_22050_32",
                "mp3_44100_32",
                "mp3_44100_64",
                "mp3_44100_96",
                "mp3_44100_128",
                "mp3_44100_192"
            ],
            state="readonly",
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=38
        )
        self.output_format_dropdown.pack(anchor=tk.W)
    
    def pack(self, **kwargs):
        """Pack the component frame."""
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        """Hide the component frame."""
        self.frame.pack_forget()
    
    def load_settings(self):
        """Load settings from the application configuration."""
        config = self.app.get_service_config()
        self.api_key_var.set(config.get("api_key", ""))
        self.voice_id_var.set(config.get("voice_id", ""))
        self.model_id_var.set(config.get("model_id", "eleven_turbo_v2_5"))
        self.output_format_var.set(config.get("output_format", "mp3_22050_32"))
    
    def get_settings(self):
        """Get the current settings from the UI.
        
        Returns:
            dict: Dictionary containing the ElevenLabs settings
        """
        return {
            "api_key": self.api_key_var.get(),
            "voice_id": self.voice_id_var.get(),
            "model_id": self.model_id_var.get(),
            "output_format": self.output_format_var.get(),
            "file_extension": ".mp3"
        }
