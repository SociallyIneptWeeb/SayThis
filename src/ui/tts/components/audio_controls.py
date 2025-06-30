import tkinter as tk
from tkinter import ttk, filedialog
import pygame
import shutil
from pathlib import Path
from ...constants import UIConstants


class AudioControls:
    """Component for audio playback controls with integrated audio handling."""
    
    def __init__(self, parent, on_error):
        """Initialize the audio controls component.
        
        Args:
            parent: The parent widget to contain this component
            on_error: Callback function for playback error handling
        """
        self.parent = parent
        self.on_error = on_error
        self.current_audio_file = None
        self.is_playing = False
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the audio control widgets."""
        # Audio playback controls frame
        self.audio_frame = ttk.LabelFrame(
            self.parent, 
            text="Audio Playback",
            padding=(10, 5)
        )
        self.audio_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Audio control buttons frame
        self.audio_buttons_frame = ttk.Frame(self.audio_frame)
        self.audio_buttons_frame.pack(fill=tk.X, expand=True)
        
        # Play button
        self.play_button = ttk.Button(
            self.audio_buttons_frame,
            text="▶️ Play",
            command=self._on_play,
            state=UIConstants.STATE_DISABLED
        )
        self.play_button.pack(side=tk.LEFT, padx=UIConstants.BUTTON_PADDING)
        
        # Stop button
        self.stop_button = ttk.Button(
            self.audio_buttons_frame,
            text="⏹️ Stop",
            command=self._on_stop,
            state=UIConstants.STATE_DISABLED
        )
        self.stop_button.pack(side=tk.LEFT, padx=UIConstants.BUTTON_PADDING)
        
        # Download button
        self.download_button = ttk.Button(
            self.audio_buttons_frame,
            text="📥 Download",
            command=self._on_download,
            state=UIConstants.STATE_DISABLED,
            width=15
        )
        self.download_button.pack(side=tk.LEFT, padx=UIConstants.BUTTON_PADDING)
        
        # Audio file label
        self.audio_file_var = tk.StringVar(value="No audio file generated yet")
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
    
    def set_playing_state(self):
        """Set the controls to playing state."""
        self.play_button.configure(state=UIConstants.STATE_DISABLED)
        self.stop_button.configure(state=UIConstants.STATE_NORMAL)
    
    def set_stopped_state(self):
        """Set the controls to stopped state."""
        self.play_button.configure(state=UIConstants.STATE_NORMAL)
        self.stop_button.configure(state=UIConstants.STATE_DISABLED)
    
    def _on_play(self):
        """Handle play button click."""
        if self.current_audio_file and self.current_audio_file.exists():
            try:
                pygame.mixer.music.load(self.current_audio_file)
                pygame.mixer.music.play()
                
                # Update UI state
                self.set_playing_state()
                
                # Set playing flag and start monitoring playback
                self.is_playing = True
                self._monitor_playback()
            except Exception as e:
                self._reset_audio_controls()
                self.on_error(f"Audio playback error: {str(e)}")
    
    def _on_stop(self):
        """Handle stop button click."""
        pygame.mixer.music.stop()
        self._reset_audio_controls()
    
    def _on_download(self):
        """Handle download button click."""
        if not self.current_audio_file or not self.current_audio_file.exists():
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
            except Exception as e:
                self.on_error(f"Download failed: {str(e)}")
    
    def stop_and_unload_audio(self):
        """Stop and unload any currently playing audio."""
        if self.is_playing:
            pygame.mixer.music.stop()
            self.is_playing = False
        
        # Unload any previously loaded audio to free resources
        if pygame.mixer.music.get_busy() or pygame.mixer.get_init():
            pygame.mixer.music.unload()
        
        # Reset audio controls to default state
        self.set_stopped_state()
    
    def _reset_audio_controls(self):
        """Reset audio control states and playing flag."""
        self.is_playing = False
        self.set_stopped_state()
    
    def _monitor_playback(self):
        """Monitor audio playback and reset control states when finished."""
        if self.is_playing:
            # Check if audio is still playing
            if not pygame.mixer.music.get_busy():
                # Audio has finished playing naturally
                self._reset_audio_controls()
            else:
                # Audio is still playing, check again after the monitoring interval
                self.parent.after(UIConstants.AUDIO_MONITOR_INTERVAL_MS, self._monitor_playback)
    
    def cleanup(self):
        """Clean up audio resources."""
        self.is_playing = False
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.quit()
