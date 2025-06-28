import tkinter as tk
from tkinter import ttk
from pathlib import Path
from ..constants import UIConstants


class AudioControls:
    """Component for audio playback controls."""
    
    def __init__(self, parent, on_play_callback, on_stop_callback, on_download_callback):
        """Initialize the audio controls component.
        
        Args:
            parent: The parent widget to contain this component
            on_play_callback: Callback function for play button
            on_stop_callback: Callback function for stop button
            on_download_callback: Callback function for download button
        """
        self.parent = parent
        self.on_play_callback = on_play_callback
        self.on_stop_callback = on_stop_callback
        self.on_download_callback = on_download_callback
        self.current_audio_file = None
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the audio control widgets."""
        # Audio playback controls frame
        self.audio_frame = ttk.LabelFrame(
            self.parent, 
            text=UIConstants.AUDIO_FRAME_TEXT, 
            padding=(10, 5)
        )
        self.audio_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(15, 0), ipady=5)
        
        # Audio control buttons frame
        self.audio_buttons_frame = ttk.Frame(self.audio_frame)
        self.audio_buttons_frame.pack(fill=tk.X, expand=True)
        
        # Play button
        self.play_button = ttk.Button(
            self.audio_buttons_frame,
            text=UIConstants.PLAY_BUTTON_TEXT,
            command=self.on_play_callback,
            state=UIConstants.STATE_DISABLED
        )
        self.play_button.pack(side=tk.LEFT, padx=UIConstants.BUTTON_PADDING)
        
        # Stop button
        self.stop_button = ttk.Button(
            self.audio_buttons_frame,
            text=UIConstants.STOP_BUTTON_TEXT,
            command=self.on_stop_callback,
            state=UIConstants.STATE_DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=UIConstants.BUTTON_PADDING)
        
        # Download button
        self.download_button = ttk.Button(
            self.audio_buttons_frame,
            text=UIConstants.DOWNLOAD_BUTTON_TEXT,
            command=self.on_download_callback,
            state=UIConstants.STATE_DISABLED
        )
        self.download_button.pack(side=tk.LEFT, padx=UIConstants.BUTTON_PADDING)
        
        # Audio file label
        self.audio_file_var = tk.StringVar(value=UIConstants.DEFAULT_AUDIO_FILE_STATUS)
        self.audio_file_label = ttk.Label(
            self.audio_frame,
            textvariable=self.audio_file_var,
            foreground="gray",
            wraplength=UIConstants.DEFAULT_WRAP_LENGTH
        )
        self.audio_file_label.pack(anchor=tk.W, pady=(5, 0), fill=tk.X)
    
    def set_audio_file(self, file_path):
        """Set the current audio file and enable playback.
        
        Args:
            file_path (str): Path to the audio file
        """
        self.current_audio_file = Path(file_path)
        self.audio_file_var.set(self.current_audio_file.name)
        self.play_button.configure(state=UIConstants.STATE_NORMAL)
        self.download_button.configure(state=UIConstants.STATE_NORMAL)
    
    def get_audio_file(self):
        """Get the current audio file path.
        
        Returns:
            Path: The current audio file path or None
        """
        return self.current_audio_file
    
    def set_playing_state(self):
        """Set the controls to playing state."""
        self.play_button.configure(state=UIConstants.STATE_DISABLED)
        self.stop_button.configure(state=UIConstants.STATE_NORMAL)
    
    def set_stopped_state(self):
        """Set the controls to stopped state."""
        self.play_button.configure(state=UIConstants.STATE_NORMAL)
        self.stop_button.configure(state=UIConstants.STATE_DISABLED)

