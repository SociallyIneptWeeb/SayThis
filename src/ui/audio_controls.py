import tkinter as tk
from tkinter import ttk
import pygame
import os
from .constants import UIConstants


class AudioControls:
    """Component for audio playback controls."""
    
    def __init__(self, parent, status_label):
        """Initialize the audio controls component.
        
        Args:
            parent: The parent widget to contain this component
            status_label: Reference to the status label for updates
        """
        self.parent = parent
        self.status_label = status_label
        self.current_audio_file = None
        self._create_widgets()
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
    
    def _create_widgets(self):
        """Create the audio control widgets."""
        # Audio playback controls frame
        self.audio_frame = ttk.LabelFrame(
            self.parent, 
            text=UIConstants.AUDIO_FRAME_TEXT, 
            padding=(10, 5)
        )
        self.audio_frame.pack(fill=tk.X, pady=(15, 0), ipady=5)
        
        # Audio control buttons frame
        self.audio_buttons_frame = ttk.Frame(self.audio_frame)
        self.audio_buttons_frame.pack(fill=tk.X, expand=True)
        
        # Play button
        self.play_button = ttk.Button(
            self.audio_buttons_frame,
            text=UIConstants.PLAY_BUTTON_TEXT,
            command=self._play_audio,
            state="disabled"  # Initially disabled until audio is generated
        )
        self.play_button.pack(side=tk.LEFT, padx=UIConstants.BUTTON_PADDING)
        
        # Stop button
        self.stop_button = ttk.Button(
            self.audio_buttons_frame,
            text=UIConstants.STOP_BUTTON_TEXT,
            command=self._stop_audio,
            state="disabled"  # Initially disabled until audio is playing
        )
        self.stop_button.pack(side=tk.LEFT, padx=UIConstants.BUTTON_PADDING)
        
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
        self.current_audio_file = file_path
        self.audio_file_var.set(str(file_path))
        self.play_button.configure(state="normal")
    
    def _play_audio(self):
        """Play the generated audio file."""
        if self.current_audio_file and os.path.exists(self.current_audio_file):
            try:
                pygame.mixer.music.load(self.current_audio_file)
                pygame.mixer.music.play()
                
                # Update button states
                self.play_button.configure(state="disabled")
                self.stop_button.configure(state="normal")
                self.status_label.set_status(UIConstants.STATUS_PLAYING, "blue")
            except Exception as e:
                self.status_label.set_status(
                    UIConstants.STATUS_AUDIO_ERROR.format(str(e)), 
                    "red"
                )
        else:
            self.status_label.set_status(UIConstants.STATUS_NO_AUDIO_FILE, "orange")
    
    def _stop_audio(self):
        """Stop the audio playback."""
        pygame.mixer.music.stop()
        
        # Update button states
        self.play_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.set_status(UIConstants.STATUS_STOPPED, "gray")
    
    def cleanup(self):
        """Clean up audio resources."""
        # Stop any playing audio
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.quit()
