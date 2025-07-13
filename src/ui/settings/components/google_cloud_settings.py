import customtkinter
from customtkinter import filedialog

from ...constants import UIConstants


class GoogleCloudSettings:
    """Component for Google Cloud-specific settings."""
    
    def __init__(self, parent, app):
        """Initialize the Google Cloud settings component.
        
        Args:
            parent: The parent widget to contain this component
            app: The Application instance
        """
        self.parent = parent
        self.app = app
        self.frame = customtkinter.CTkFrame(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the Google Cloud settings widgets."""
        # Service Account JSON File Configuration Section
        file_frame = customtkinter.CTkFrame(self.frame, fg_color="transparent")
        file_frame.pack(pady=10, fill=customtkinter.X)
        
        customtkinter.CTkLabel(file_frame, text="Google Cloud Service Account JSON File:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W, pady=(0, 5))
        
        # File path entry and browse button
        path_frame = customtkinter.CTkFrame(file_frame, fg_color="transparent")
        path_frame.pack(anchor=customtkinter.W, pady=(0, 10), fill=customtkinter.X)
        
        self.service_account_path_var = customtkinter.StringVar()
        self.service_account_path_entry = customtkinter.CTkEntry(
            path_frame,
            textvariable=self.service_account_path_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=40,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.service_account_path_entry.pack(side=customtkinter.LEFT, fill=customtkinter.X, expand=True)
        
        self.browse_button = customtkinter.CTkButton(
            path_frame,
            text="Browse...",
            command=self._browse_service_account_file,
            width=10,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.browse_button.pack(side=customtkinter.RIGHT, padx=(5, 0))
        
        # Voice Settings Configuration Section
        voice_settings_frame = customtkinter.CTkFrame(self.frame, corner_radius=UIConstants.CORNER_RADIUS)
        voice_settings_frame.pack(pady=10, fill=customtkinter.X)
        
        customtkinter.CTkLabel(voice_settings_frame, text="Voice Settings", 
                               font=customtkinter.CTkFont(weight="bold")).pack(anchor=customtkinter.W, padx=10, pady=(5, 0))

        # Language Code
        customtkinter.CTkLabel(voice_settings_frame, text="Language Code:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W, pady=(0, 5), padx=10)
        
        self.language_code_var = customtkinter.StringVar()
        self.language_code_entry = customtkinter.CTkEntry(
            voice_settings_frame,
            textvariable=self.language_code_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=15,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.language_code_entry.pack(anchor=customtkinter.W, pady=(0, 10), padx=10)
        
        # Voice Name
        customtkinter.CTkLabel(voice_settings_frame, text="Voice Name:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W, pady=(0, 5), padx=10)
        
        self.voice_name_var = customtkinter.StringVar()
        self.voice_name_entry = customtkinter.CTkEntry(
            voice_settings_frame,
            textvariable=self.voice_name_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=30,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.voice_name_entry.pack(anchor=customtkinter.W, pady=(0, 10), padx=10)
        
        # Voice Gender
        customtkinter.CTkLabel(voice_settings_frame, text="Voice Gender:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W, pady=(0, 5), padx=10)
        
        self.voice_gender_var = customtkinter.StringVar()
        self.voice_gender_dropdown = customtkinter.CTkOptionMenu(
            voice_settings_frame,
            variable=self.voice_gender_var,
            values=["NEUTRAL", "MALE", "FEMALE"],
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=15,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.voice_gender_dropdown.pack(anchor=customtkinter.W, pady=(0, 10), padx=10)
        
        # Audio Settings Configuration Section
        audio_settings_frame = customtkinter.CTkFrame(self.frame, corner_radius=UIConstants.CORNER_RADIUS)
        audio_settings_frame.pack(pady=10, fill=customtkinter.X)
        
        customtkinter.CTkLabel(audio_settings_frame, text="Audio Settings", 
                               font=customtkinter.CTkFont(weight="bold")).pack(anchor=customtkinter.W, padx=10, pady=(5, 0))

        # File Format
        customtkinter.CTkLabel(audio_settings_frame, text="File Format:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W, pady=(0, 5), padx=10)
        
        self.file_format_var = customtkinter.StringVar()
        self.file_format_dropdown = customtkinter.CTkOptionMenu(
            audio_settings_frame,
            variable=self.file_format_var,
            values=[".mp3", ".wav"],
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=15,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.file_format_dropdown.pack(anchor=customtkinter.W, pady=(0, 10), padx=10)
        
        # Speaking Rate
        speaking_rate_frame = customtkinter.CTkFrame(audio_settings_frame, fg_color="transparent")
        speaking_rate_frame.pack(pady=5, fill=customtkinter.X, padx=10)
        
        customtkinter.CTkLabel(speaking_rate_frame, text="Speaking Rate (0.25 - 2.0):", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W)
        
        self.speaking_rate_var = customtkinter.DoubleVar(value=1.0)
        self.speaking_rate_scale = customtkinter.CTkSlider(
            speaking_rate_frame,
            from_=0.25,
            to=2.0,
            variable=self.speaking_rate_var,
            command=lambda val: self.speaking_rate_value_label.configure(text=f"{float(val):.2f}"),
        )
        self.speaking_rate_scale.pack(anchor=customtkinter.W, pady=(2, 0))
        
        self.speaking_rate_value_label = customtkinter.CTkLabel(speaking_rate_frame, text="1.0")
        self.speaking_rate_value_label.pack(anchor=customtkinter.W)
        
        
        # Pitch
        pitch_frame = customtkinter.CTkFrame(audio_settings_frame, fg_color="transparent")
        pitch_frame.pack(pady=5, fill=customtkinter.X, padx=10)
        
        customtkinter.CTkLabel(pitch_frame, text="Pitch (-20.0 to 20.0):", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W)
        
        self.pitch_var = customtkinter.DoubleVar(value=0.0)
        self.pitch_scale = customtkinter.CTkSlider(
            pitch_frame,
            from_=-20.0,
            to=20.0,
            variable=self.pitch_var,
            command=lambda val: self.pitch_value_label.configure(text=f"{float(val):.2f}"),
        )
        self.pitch_scale.pack(anchor=customtkinter.W, pady=(2, 0))
        
        self.pitch_value_label = customtkinter.CTkLabel(pitch_frame, text="0.0")
        self.pitch_value_label.pack(anchor=customtkinter.W)
        
        
        # Volume Gain
        volume_gain_frame = customtkinter.CTkFrame(audio_settings_frame, fg_color="transparent")
        volume_gain_frame.pack(pady=5, fill=customtkinter.X, padx=10)
        
        customtkinter.CTkLabel(volume_gain_frame, text="Volume Gain (-16.0 to 16.0 dB):", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W)
        
        self.volume_gain_var = customtkinter.DoubleVar(value=0.0)
        self.volume_gain_scale = customtkinter.CTkSlider(
            volume_gain_frame,
            from_=-16.0,
            to=16.0,
            variable=self.volume_gain_var,
            command=lambda val: self.volume_gain_value_label.configure(text=f"{float(val):.1f}"),
        )
        self.volume_gain_scale.pack(anchor=customtkinter.W, pady=(2, 0))
        
        self.volume_gain_value_label = customtkinter.CTkLabel(volume_gain_frame, text="0.0")
        self.volume_gain_value_label.pack(anchor=customtkinter.W)
    
    def _browse_service_account_file(self):
        """Open file dialog to browse for service account JSON file."""
        file_path = filedialog.askopenfilename(
            title="Select Google Cloud Service Account JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.service_account_path_var.set(file_path)

    def grid(self, **kwargs):
        """Grid the component frame."""
        self.frame.grid(**kwargs)
    
    def grid_remove(self):
        """Remove the component frame from grid."""
        self.frame.grid_remove()
    
    def load_settings(self):
        """Load settings from the application configuration."""
        config = self.app.get_service_config()
        self.service_account_path_var.set(config.get("service_account_json_path", ""))
        self.language_code_var.set(config.get("language_code", "en-US"))
        self.voice_name_var.set(config.get("voice_name", "en-US-Wavenet-D"))
        self.voice_gender_var.set(config.get("voice_gender", "NEUTRAL"))
        
        # Map audio encoding to file format for display
        audio_encoding = config.get("audio_encoding", "MP3")
        if audio_encoding == "MP3":
            file_format = ".mp3"
        elif audio_encoding == "LINEAR16":
            file_format = ".wav"
        else:
            file_format = ".mp3"  # Default
        self.file_format_var.set(file_format)
        
        self.speaking_rate_var.set(config.get("speaking_rate", 1.0))
        self.pitch_var.set(config.get("pitch", 0.0))
        self.volume_gain_var.set(config.get("volume_gain_db", 0.0))
        
        # Update value labels
        self.speaking_rate_value_label.configure(text=f"{self.speaking_rate_var.get():.2f}")
        self.pitch_value_label.configure(text=f"{self.pitch_var.get():.2f}")
        self.volume_gain_value_label.configure(text=f"{self.volume_gain_var.get():.1f}")
    
    def get_settings(self):
        """Get the current settings from the UI.
        
        Returns:
            dict: Dictionary containing the Google Cloud settings
        """
        # Map file format to audio encoding and file extension
        file_format = self.file_format_var.get()
        if file_format == ".mp3":
            audio_encoding = "MP3"
        elif file_format == ".wav":
            audio_encoding = "LINEAR16"
        else:
            audio_encoding = "MP3"  # Default

        return {
            "service_account_json_path": self.service_account_path_var.get(),
            "language_code": self.language_code_var.get(),
            "voice_name": self.voice_name_var.get(),
            "voice_gender": self.voice_gender_var.get(),
            "audio_encoding": audio_encoding,
            "speaking_rate": self.speaking_rate_var.get(),
            "pitch": self.pitch_var.get(),
            "volume_gain_db": self.volume_gain_var.get(),
            "file_extension": file_format
        }


