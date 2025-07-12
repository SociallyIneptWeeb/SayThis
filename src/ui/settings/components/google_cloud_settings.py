import tkinter as tk
from tkinter import ttk, filedialog
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
        self.frame = ttk.Frame(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the Google Cloud settings widgets."""
        # Service Account JSON File Configuration Section
        file_frame = ttk.Frame(self.frame)
        file_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(file_frame, text="Google Cloud Service Account JSON File:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        # File path entry and browse button
        path_frame = ttk.Frame(file_frame)
        path_frame.pack(anchor=tk.W, pady=(0, 10), fill=tk.X)
        
        self.service_account_path_var = tk.StringVar()
        self.service_account_path_entry = ttk.Entry(
            path_frame,
            textvariable=self.service_account_path_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=40
        )
        self.service_account_path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.browse_button = ttk.Button(
            path_frame,
            text="Browse...",
            command=self._browse_service_account_file,
            width=10
        )
        self.browse_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # Voice Settings Configuration Section
        voice_settings_frame = ttk.LabelFrame(self.frame, text="Voice Settings", padding=(10, 5))
        voice_settings_frame.pack(pady=10, fill=tk.X)
        
        # Language Code
        ttk.Label(voice_settings_frame, text="Language Code:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        self.language_code_var = tk.StringVar()
        self.language_code_entry = ttk.Entry(
            voice_settings_frame,
            textvariable=self.language_code_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=15
        )
        self.language_code_entry.pack(anchor=tk.W, pady=(0, 10))
        
        # Voice Name
        ttk.Label(voice_settings_frame, text="Voice Name:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        self.voice_name_var = tk.StringVar()
        self.voice_name_entry = ttk.Entry(
            voice_settings_frame,
            textvariable=self.voice_name_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=30
        )
        self.voice_name_entry.pack(anchor=tk.W, pady=(0, 10))
        
        # Voice Gender
        ttk.Label(voice_settings_frame, text="Voice Gender:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        self.voice_gender_var = tk.StringVar()
        self.voice_gender_dropdown = ttk.Combobox(
            voice_settings_frame,
            textvariable=self.voice_gender_var,
            values=["NEUTRAL", "MALE", "FEMALE"],
            state="readonly",
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=15
        )
        self.voice_gender_dropdown.pack(anchor=tk.W, pady=(0, 10))
        
        # Audio Settings Configuration Section
        audio_settings_frame = ttk.LabelFrame(self.frame, text="Audio Settings", padding=(10, 5))
        audio_settings_frame.pack(pady=10, fill=tk.X)
        
        # File Format
        ttk.Label(audio_settings_frame, text="File Format:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        self.file_format_var = tk.StringVar()
        self.file_format_dropdown = ttk.Combobox(
            audio_settings_frame,
            textvariable=self.file_format_var,
            values=[".mp3", ".wav"],
            state="readonly",
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=15
        )
        self.file_format_dropdown.pack(anchor=tk.W, pady=(0, 10))
        
        # Speaking Rate
        speaking_rate_frame = ttk.Frame(audio_settings_frame)
        speaking_rate_frame.pack(pady=5, fill=tk.X)
        
        ttk.Label(speaking_rate_frame, text="Speaking Rate (0.25 - 2.0):", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W)
        
        self.speaking_rate_var = tk.DoubleVar(value=1.0)
        self.speaking_rate_scale = ttk.Scale(
            speaking_rate_frame,
            from_=0.25,
            to=2.0,
            variable=self.speaking_rate_var,
            orient=tk.HORIZONTAL,
            length=300
        )
        self.speaking_rate_scale.pack(anchor=tk.W, pady=(2, 0))
        
        self.speaking_rate_value_label = ttk.Label(speaking_rate_frame, text="1.0")
        self.speaking_rate_value_label.pack(anchor=tk.W)
        
        self.speaking_rate_scale.configure(command=lambda val: self.speaking_rate_value_label.configure(text=f"{float(val):.2f}"))
        
        # Pitch
        pitch_frame = ttk.Frame(audio_settings_frame)
        pitch_frame.pack(pady=5, fill=tk.X)
        
        ttk.Label(pitch_frame, text="Pitch (-20.0 to 20.0):", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W)
        
        self.pitch_var = tk.DoubleVar(value=0.0)
        self.pitch_scale = ttk.Scale(
            pitch_frame,
            from_=-20.0,
            to=20.0,
            variable=self.pitch_var,
            orient=tk.HORIZONTAL,
            length=300
        )
        self.pitch_scale.pack(anchor=tk.W, pady=(2, 0))
        
        self.pitch_value_label = ttk.Label(pitch_frame, text="0.0")
        self.pitch_value_label.pack(anchor=tk.W)
        
        self.pitch_scale.configure(command=lambda val: self.pitch_value_label.configure(text=f"{float(val):.2f}"))
        
        # Volume Gain
        volume_gain_frame = ttk.Frame(audio_settings_frame)
        volume_gain_frame.pack(pady=5, fill=tk.X)
        
        ttk.Label(volume_gain_frame, text="Volume Gain (-16.0 to 16.0 dB):", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W)
        
        self.volume_gain_var = tk.DoubleVar(value=0.0)
        self.volume_gain_scale = ttk.Scale(
            volume_gain_frame,
            from_=-16.0,
            to=16.0,
            variable=self.volume_gain_var,
            orient=tk.HORIZONTAL,
            length=300
        )
        self.volume_gain_scale.pack(anchor=tk.W, pady=(2, 0))
        
        self.volume_gain_value_label = ttk.Label(volume_gain_frame, text="0.0")
        self.volume_gain_value_label.pack(anchor=tk.W)
        
        self.volume_gain_scale.configure(command=lambda val: self.volume_gain_value_label.configure(text=f"{float(val):.1f}"))
    
    def _browse_service_account_file(self):
        """Open file dialog to browse for service account JSON file."""
        file_path = filedialog.askopenfilename(
            title="Select Google Cloud Service Account JSON File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if file_path:
            self.service_account_path_var.set(file_path)
    
    def pack(self, **kwargs):
        """Pack the component frame."""
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        """Hide the component frame."""
        self.frame.pack_forget()
    
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
