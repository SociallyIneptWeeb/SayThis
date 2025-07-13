import tkinter as tk
from tkinter import ttk
from ...constants import UIConstants
from .tooltip import ToolTip


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
        
        # Voice Settings Configuration Section
        voice_settings_frame = ttk.LabelFrame(self.frame, text="Voice Settings", padding=(10, 5))
        voice_settings_frame.pack(pady=10, fill=tk.X)
        
        # Stability slider
        stability_frame = ttk.Frame(voice_settings_frame)
        stability_frame.pack(pady=5, fill=tk.X)
        
        stability_label = ttk.Label(stability_frame, text="Stability:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE))
        stability_label.pack(anchor=tk.W)
        
        # Add tooltip to the stability label
        ToolTip(stability_label, "Determines how stable the voice is and the randomness between each generation. Lower values introduce broader emotional range for the voice. Higher values can result in a monotonous voice with limited emotion.")

        self.stability_var = tk.DoubleVar(value=0.5)
        self.stability_scale = ttk.Scale(
            stability_frame,
            from_=0.0,
            to=1.0,
            variable=self.stability_var,
            orient=tk.HORIZONTAL,
            length=300
        )
        self.stability_scale.pack(anchor=tk.W, pady=(2, 0))
        
        self.stability_value_label = ttk.Label(stability_frame, text="0.5")
        self.stability_value_label.pack(anchor=tk.W)
        
        self.stability_scale.configure(command=lambda val: self.stability_value_label.configure(text=f"{float(val):.2f}"))
        
        # Similarity Boost slider
        similarity_frame = ttk.Frame(voice_settings_frame)
        similarity_frame.pack(pady=5, fill=tk.X)
        
        similarity_label = ttk.Label(similarity_frame, text="Similarity Boost:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE))
        similarity_label.pack(anchor=tk.W)
        
        # Add tooltip to the similarity boost label
        ToolTip(similarity_label, "Determines how closely the AI should adhere to the original voice when attempting to replicate it.")
        
        self.similarity_boost_var = tk.DoubleVar(value=0.75)
        self.similarity_boost_scale = ttk.Scale(
            similarity_frame,
            from_=0.0,
            to=1.0,
            variable=self.similarity_boost_var,
            orient=tk.HORIZONTAL,
            length=300
        )
        self.similarity_boost_scale.pack(anchor=tk.W, pady=(2, 0))
        
        self.similarity_value_label = ttk.Label(similarity_frame, text="0.75")
        self.similarity_value_label.pack(anchor=tk.W)
        
        self.similarity_boost_scale.configure(command=lambda val: self.similarity_value_label.configure(text=f"{float(val):.2f}"))
        
        # Style slider
        style_frame = ttk.Frame(voice_settings_frame)
        style_frame.pack(pady=5, fill=tk.X)
        
        style_label = ttk.Label(style_frame, text="Style:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE))
        style_label.pack(anchor=tk.W)
        
        # Add tooltip to the style label
        ToolTip(style_label, "Determines the style exaggeration of the voice. This setting attempts to amplify the style of the original speaker. It does consume additional computational resources and might increase latency if set to anything other than 0.")

        self.style_var = tk.DoubleVar(value=0.0)
        self.style_scale = ttk.Scale(
            style_frame,
            from_=0.0,
            to=1.0,
            variable=self.style_var,
            orient=tk.HORIZONTAL,
            length=300
        )
        self.style_scale.pack(anchor=tk.W, pady=(2, 0))
        
        self.style_value_label = ttk.Label(style_frame, text="0.0")
        self.style_value_label.pack(anchor=tk.W)
        
        self.style_scale.configure(command=lambda val: self.style_value_label.configure(text=f"{float(val):.2f}"))
        
        # Speed slider
        speed_frame = ttk.Frame(voice_settings_frame)
        speed_frame.pack(pady=5, fill=tk.X)
        
        speed_label = ttk.Label(speed_frame, text="Speed:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE))
        speed_label.pack(anchor=tk.W)
        
        # Add tooltip to the speed label
        ToolTip(speed_label, "Adjusts the speed of the voice. A value of 1.0 is the default speed, while values less than 1.0 slow down the speech, and values greater than 1.0 speed it up.")

        self.speed_var = tk.DoubleVar(value=1.0)
        self.speed_scale = ttk.Scale(
            speed_frame,
            from_=0.7,
            to=1.2,
            variable=self.speed_var,
            orient=tk.HORIZONTAL,
            length=300
        )
        self.speed_scale.pack(anchor=tk.W, pady=(2, 0))
        
        self.speed_value_label = ttk.Label(speed_frame, text="1.0")
        self.speed_value_label.pack(anchor=tk.W)
        
        self.speed_scale.configure(command=lambda val: self.speed_value_label.configure(text=f"{float(val):.2f}"))
        
        # Use Speaker Boost checkbox
        speaker_boost_frame = ttk.Frame(voice_settings_frame)
        speaker_boost_frame.pack(pady=5, fill=tk.X)

        self.use_speaker_boost_var = tk.BooleanVar(value=True)
        self.use_speaker_boost_checkbox = ttk.Checkbutton(
            speaker_boost_frame,
            text="Use Speaker Boost",
            variable=self.use_speaker_boost_var,
        )
        self.use_speaker_boost_checkbox.pack(anchor=tk.W)
        
        # Add tooltip to the speaker boost checkbox
        ToolTip(self.use_speaker_boost_checkbox, "This setting boosts the similarity to the original speaker. Using this setting requires a slightly higher computational load, which in turn increases latency.")
    
    def grid(self, **kwargs):
        """Grid the component frame."""
        self.frame.grid(**kwargs)
    
    def grid_remove(self):
        """Remove the component frame from grid."""
        self.frame.grid_remove()
    
    def load_settings(self):
        """Load settings from the application configuration."""
        config = self.app.get_service_config()
        self.api_key_var.set(config.get("api_key", ""))
        self.voice_id_var.set(config.get("voice_id", ""))
        self.model_id_var.set(config.get("model_id", "eleven_turbo_v2_5"))
        self.output_format_var.set(config.get("output_format", "mp3_22050_32"))
        
        # Load voice settings
        voice_settings = config.get("voice_settings", {})
        self.stability_var.set(voice_settings.get("stability", 0.5))
        self.similarity_boost_var.set(voice_settings.get("similarity_boost", 0.75))
        self.style_var.set(voice_settings.get("style", 0.0))
        self.speed_var.set(voice_settings.get("speed", 1.0))
        self.use_speaker_boost_var.set(voice_settings.get("use_speaker_boost", True))
        
        # Update value labels
        self.stability_value_label.configure(text=f"{self.stability_var.get():.2f}")
        self.similarity_value_label.configure(text=f"{self.similarity_boost_var.get():.2f}")
        self.style_value_label.configure(text=f"{self.style_var.get():.2f}")
        self.speed_value_label.configure(text=f"{self.speed_var.get():.2f}")
    
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
            "file_extension": ".mp3",
            "voice_settings": {
                "stability": self.stability_var.get(),
                "similarity_boost": self.similarity_boost_var.get(),
                "style": self.style_var.get(),
                "speed": self.speed_var.get(),
                "use_speaker_boost": self.use_speaker_boost_var.get()
            }
        }
