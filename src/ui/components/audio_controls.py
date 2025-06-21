import tkinter as tk
from tkinter import ttk, filedialog
import pygame
import shutil
from pathlib import Path
from ..constants import UIConstants


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
        self.is_playing = False
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
            state=UIConstants.STATE_DISABLED
        )
        self.play_button.pack(side=tk.LEFT, padx=UIConstants.BUTTON_PADDING)
        
        # Stop button
        self.stop_button = ttk.Button(
            self.audio_buttons_frame,
            text=UIConstants.STOP_BUTTON_TEXT,
            command=self._stop_audio,
            state=UIConstants.STATE_DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=UIConstants.BUTTON_PADDING)
        
        # Download button
        self.download_button = ttk.Button(
            self.audio_buttons_frame,
            text=UIConstants.DOWNLOAD_BUTTON_TEXT,
            command=self._download_audio,
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
    
    def _play_audio(self):
        """Play the generated audio file."""
        if self.current_audio_file and self.current_audio_file.exists():
            try:
                pygame.mixer.music.load(self.current_audio_file)
                pygame.mixer.music.play()
                
                # Update button states
                self.play_button.configure(state=UIConstants.STATE_DISABLED)
                self.stop_button.configure(state=UIConstants.STATE_NORMAL)
                self.status_label.set_status(UIConstants.STATUS_PLAYING, UIConstants.STATUS_COLOR_PROCESSING)
                
                # Set playing flag and start monitoring playback
                self.is_playing = True
                self._monitor_playback()
            except Exception as e:
                self.status_label.set_error(f"Error playing audio: {str(e)}")
        else:
            self.status_label.set_status(UIConstants.STATUS_NO_AUDIO_FILE, UIConstants.STATUS_COLOR_WARNING)
    
    def _reset_controls(self, status_message):
        """Reset button states and playing flag with status update.
        
        Args:
            status_message (str): Status message to display
        """
        self.is_playing = False
        self.play_button.configure(state=UIConstants.STATE_NORMAL)
        self.stop_button.configure(state=UIConstants.STATE_DISABLED)
        
        self.status_label.set_status(status_message, UIConstants.STATUS_COLOR_READY)
    
    def _stop_audio(self):
        """Stop the audio playback."""
        pygame.mixer.music.stop()
        
        # Update button states and playing flag
        self._reset_controls(UIConstants.STATUS_STOPPED)

    def _monitor_playback(self):
        """Monitor audio playback and reset button states when finished."""
        if self.is_playing:
            # Check if audio is still playing
            if not pygame.mixer.music.get_busy():
                # Audio has finished playing naturally
                self._reset_controls(UIConstants.STATUS_READY)
            else:
                # Audio is still playing, check again after the monitoring interval
                self.parent.after(UIConstants.AUDIO_MONITOR_INTERVAL_MS, self._monitor_playback)
    
    def _download_audio(self):
        """Download the current audio file to a user-selected location."""
        if not self.current_audio_file or not self.current_audio_file.exists():
            self.status_label.set_status(UIConstants.STATUS_NO_AUDIO_FILE, UIConstants.STATUS_COLOR_WARNING)
            return
        
        # Get the file extension from the current audio file
        file_extension = self.current_audio_file.suffix
        
        # Open file dialog to choose download location
        save_path = filedialog.asksaveasfilename(
            title="Save Audio File",
            defaultextension=file_extension,
            filetypes=[
                ("Audio Files", f"*{file_extension}"),
            ],
            initialfile=self.current_audio_file.name
        )
        
        if save_path:
            try:
                # Copy the file to the selected location
                shutil.copy2(self.current_audio_file, save_path)
                self.status_label.set_status(UIConstants.STATUS_DOWNLOAD_SUCCESS, UIConstants.STATUS_COLOR_SUCCESS)
            except Exception as e:
                self.status_label.set_error(f"Error downloading audio: {str(e)}")
        else:
            # User cancelled the download
            self.status_label.set_status(UIConstants.STATUS_DOWNLOAD_CANCELLED, UIConstants.STATUS_COLOR_READY)

    def cleanup(self):
        """Clean up audio resources."""
        self.is_playing = False
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()

        pygame.mixer.quit()
