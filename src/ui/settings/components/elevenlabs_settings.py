import customtkinter

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
        self.frame = customtkinter.CTkFrame(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the ElevenLabs settings widgets."""
        # API Key Configuration Section
        api_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        api_frame.pack(pady=10, fill=customtkinter.X)
        
        # API Key label and entry
        customtkinter.CTkLabel(api_frame, text="ElevenLabs API Key:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W, pady=(0, 5))
        
        # API Key entry field
        self.api_key_var = customtkinter.StringVar()
        self.api_key_entry = customtkinter.CTkEntry(
            api_frame,
            textvariable=self.api_key_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            show=UIConstants.API_KEY_ENTRY_SHOW_CHAR,
            width=40,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.api_key_entry.pack(anchor=customtkinter.W)
        
        # Voice ID Configuration Section
        voice_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        voice_frame.pack(pady=10, fill=customtkinter.X)
        
        customtkinter.CTkLabel(voice_frame, text="Voice ID:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W, pady=(0, 5))
        
        self.voice_id_var = customtkinter.StringVar()
        voice_id_entry = customtkinter.CTkEntry(
            voice_frame,
            textvariable=self.voice_id_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=40,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        voice_id_entry.pack(anchor=customtkinter.W)
        
        # Model ID Configuration Section
        model_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        model_frame.pack(pady=10, fill=customtkinter.X)
        
        # Model ID label and entry
        customtkinter.CTkLabel(model_frame, text="Model ID:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W, pady=(0, 5))
        
        # Model ID dropdown field
        self.model_id_var = customtkinter.StringVar()
        self.model_id_dropdown = customtkinter.CTkOptionMenu(
            model_frame,
            variable=self.model_id_var,
            values=["eleven_turbo_v2_5", "eleven_flash_v2_5", "eleven_multilingual_v2", "eleven_v3"],
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=38,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.model_id_dropdown.pack(anchor=customtkinter.W)
        
        # Output Format Configuration Section
        output_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        output_frame.pack(pady=10, fill=customtkinter.X)
        
        # Output Format label and dropdown
        customtkinter.CTkLabel(output_frame, text="Output Format:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W, pady=(0, 5))
        
        # Output Format dropdown field
        self.output_format_var = customtkinter.StringVar()
        self.output_format_dropdown = customtkinter.CTkOptionMenu(
            output_frame,
            variable=self.output_format_var,
            values=[
                "mp3_22050_32",
                "mp3_44100_32",
                "mp3_44100_64",
                "mp3_44100_96",
                "mp3_44100_128",
                "mp3_44100_192"
            ],
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=38,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.output_format_dropdown.pack(anchor=customtkinter.W)
        
        # Voice Settings Configuration Section
        voice_settings_frame = customtkinter.CTkFrame(self.frame, corner_radius=UIConstants.CORNER_RADIUS)
        voice_settings_frame.pack(pady=10, fill=customtkinter.X)
        
        customtkinter.CTkLabel(voice_settings_frame, text="Voice Settings", 
                               font=customtkinter.CTkFont(weight="bold")).pack(anchor=customtkinter.W, padx=10, pady=(5, 0))

        # Stability slider
        stability_frame = customtkinter.CTkFrame(voice_settings_frame, fg_color="transparent")
        stability_frame.pack(pady=5, fill=customtkinter.X, padx=10)
        
        stability_label = customtkinter.CTkLabel(stability_frame, text="Stability:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE))
        stability_label.pack(anchor=customtkinter.W)
        
        # Add tooltip to the stability label
        ToolTip(stability_label, "Determines how stable the voice is and the randomness between each generation. Lower values introduce broader emotional range for the voice. Higher values can result in a monotonous voice with limited emotion.")

        self.stability_var = customtkinter.DoubleVar(value=0.5)
        self.stability_scale = customtkinter.CTkSlider(
            stability_frame,
            from_=0.0,
            to=1.0,
            variable=self.stability_var,
            command=lambda val: self.stability_value_label.configure(text=f"{float(val):.2f}"),
        )
        self.stability_scale.pack(anchor=customtkinter.W, pady=(2, 0))
        
        self.stability_value_label = customtkinter.CTkLabel(stability_frame, text="0.5")
        self.stability_value_label.pack(anchor=customtkinter.W)
        
        
        # Similarity Boost slider
        similarity_frame = customtkinter.CTkFrame(voice_settings_frame, fg_color="transparent")
        similarity_frame.pack(pady=5, fill=customtkinter.X, padx=10)
        
        similarity_label = customtkinter.CTkLabel(similarity_frame, text="Similarity Boost:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE))
        similarity_label.pack(anchor=customtkinter.W)
        
        # Add tooltip to the similarity boost label
        ToolTip(similarity_label, "Determines how closely the AI should adhere to the original voice when attempting to replicate it.")
        
        self.similarity_boost_var = customtkinter.DoubleVar(value=0.75)
        self.similarity_boost_scale = customtkinter.CTkSlider(
            similarity_frame,
            from_=0.0,
            to=1.0,
            variable=self.similarity_boost_var,
            command=lambda val: self.similarity_value_label.configure(text=f"{float(val):.2f}"),
        )
        self.similarity_boost_scale.pack(anchor=customtkinter.W, pady=(2, 0))
        
        self.similarity_value_label = customtkinter.CTkLabel(similarity_frame, text="0.75")
        self.similarity_value_label.pack(anchor=customtkinter.W)
        
        
        # Style slider
        style_frame = customtkinter.CTkFrame(voice_settings_frame, fg_color="transparent")
        style_frame.pack(pady=5, fill=customtkinter.X, padx=10)
        
        style_label = customtkinter.CTkLabel(style_frame, text="Style:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE))
        style_label.pack(anchor=customtkinter.W)
        
        # Add tooltip to the style label
        ToolTip(style_label, "Determines the style exaggeration of the voice. This setting attempts to amplify the style of the original speaker. It does consume additional computational resources and might increase latency if set to anything other than 0.")

        self.style_var = customtkinter.DoubleVar(value=0.0)
        self.style_scale = customtkinter.CTkSlider(
            style_frame,
            from_=0.0,
            to=1.0,
            variable=self.style_var,
            command=lambda val: self.style_value_label.configure(text=f"{float(val):.2f}"),
        )
        self.style_scale.pack(anchor=customtkinter.W, pady=(2, 0))
        
        self.style_value_label = customtkinter.CTkLabel(style_frame, text="0.0")
        self.style_value_label.pack(anchor=customtkinter.W)
        
        
        # Speed slider
        speed_frame = customtkinter.CTkFrame(voice_settings_frame, fg_color="transparent")
        speed_frame.pack(pady=5, fill=customtkinter.X, padx=10)
        
        speed_label = customtkinter.CTkLabel(speed_frame, text="Speed:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE))
        speed_label.pack(anchor=customtkinter.W)
        
        # Add tooltip to the speed label
        ToolTip(speed_label, "Adjusts the speed of the voice. A value of 1.0 is the default speed, while values less than 1.0 slow down the speech, and values greater than 1.0 speed it up.")

        self.speed_var = customtkinter.DoubleVar(value=1.0)
        self.speed_scale = customtkinter.CTkSlider(
            speed_frame,
            from_=0.7,
            to=1.2,
            variable=self.speed_var,
            command=lambda val: self.speed_value_label.configure(text=f"{float(val):.2f}"),
        )
        self.speed_scale.pack(anchor=customtkinter.W, pady=(2, 0))
        
        self.speed_value_label = customtkinter.CTkLabel(speed_frame, text="1.0")
        self.speed_value_label.pack(anchor=customtkinter.W)
        
        
        # Use Speaker Boost checkbox
        speaker_boost_frame = customtkinter.CTkFrame(voice_settings_frame, fg_color="transparent")
        speaker_boost_frame.pack(pady=5, fill=customtkinter.X, padx=10)

        self.use_speaker_boost_var = customtkinter.BooleanVar(value=True)
        self.use_speaker_boost_checkbox = customtkinter.CTkCheckBox(
            speaker_boost_frame,
            text="Use Speaker Boost",
            variable=self.use_speaker_boost_var,
        )
        self.use_speaker_boost_checkbox.pack(anchor=customtkinter.W)
        
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


