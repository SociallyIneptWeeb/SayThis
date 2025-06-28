import pygame
import shutil
from pathlib import Path
from tkinter import filedialog
from ..constants import UIConstants


class EventHandler:
    """Component for handling all event callbacks and business logic for the main window."""
    
    def __init__(self, app, root, message_input, control_buttons, status_label, audio_controls, character_usage_label):
        """Initialize the event handler.
        
        Args:
            app: The Application instance
            root: The root window
            message_input: The message input component
            control_buttons: The control buttons component
            status_label: The status label component
            audio_controls: The audio controls component
            character_usage_label: The character usage label component
        """
        self.app = app
        self.root = root
        self.message_input = message_input
        self.control_buttons = control_buttons
        self.status_label = status_label
        self.audio_controls = audio_controls
        self.character_usage_label = character_usage_label
        
        # Audio playback state
        self.is_playing = False
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        
        # Load initial character usage only if API key is configured
        if self.app.get_api_key():
            self.load_character_usage()
    
    def load_character_usage(self):
        """Load and display character usage information."""
        try:
            character_count, character_limit = self.app.get_character_usage()
            self.character_usage_label.update_usage(character_count, character_limit)
        except Exception as e:
            self.character_usage_label.set_error()
            self.status_label.set_error(f"Unable to load character usage: {str(e)}")
    
    def on_generate(self):
        """Handle generate button click."""
        if self.message_input.is_empty():
            self.status_label.set_status(
                UIConstants.STATUS_EMPTY_MESSAGE, 
                UIConstants.STATUS_COLOR_WARNING
            )
            return

        if not self.app.get_api_key():
            self.status_label.set_status(
                UIConstants.API_KEY_REQUIRED_MESSAGE, 
                UIConstants.STATUS_COLOR_WARNING
            )
            return
        
        try:
            # Stop and unload any currently playing audio
            if self.is_playing:
                pygame.mixer.music.stop()
                self.is_playing = False
            
            # Unload any previously loaded audio to free resources
            if pygame.mixer.music.get_busy() or pygame.mixer.get_init():
                pygame.mixer.music.unload()
            
            # Reset audio controls to default state
            self.audio_controls.set_stopped_state()
            
            self.control_buttons.set_generate_enabled(False)
            self.status_label.set_status(
                UIConstants.STATUS_GENERATING, 
                UIConstants.STATUS_COLOR_PROCESSING
            )
            self.character_usage_label.set_loading()

            # Update UI to show the status change
            self.root.update_idletasks()

            message = self.message_input.get_text()
            output_path = self.app.generate_audio(message)
            
            # Show success message and enable playback
            self.audio_controls.set_audio_file(output_path)
            self.status_label.set_status(
                UIConstants.STATUS_GENERATE_SUCCESS, 
                UIConstants.STATUS_COLOR_SUCCESS
            )
            
            # Update character usage after successful generation (delayed to allow API to update)
            self.root.after(8000, self.load_character_usage)
            
        except RuntimeError as e:
            self.status_label.set_error(str(e))
        except Exception as e:
            self.status_label.set_error(f"Unexpected error: {str(e)}")
        finally:
            self.control_buttons.set_generate_enabled(True)
    
    def on_clear(self):
        """Handle clear button click."""
        self.message_input.clear_text()
    
    def on_window_resize(self, event):
        """Handle window resize event to update status label wrap length.
        
        Args:
            event: The Configure event triggered by window resize
        """
        # Only process if the event is from the main window
        if event.widget == self.root:
            # Update wrap length to be slightly less than the window width
            new_width = event.width - UIConstants.WINDOW_PADDING_ADJUST
            self.status_label.update_wrap_length(new_width)
    
    def on_close(self):
        """Clean up resources and close the application."""
        # Clean up audio resources
        self.is_playing = False
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.quit()
    
    def on_play_audio(self):
        """Handle play button click."""
        audio_file = self.audio_controls.get_audio_file()
        if audio_file and audio_file.exists():
            try:
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                
                # Update UI state
                self.audio_controls.set_playing_state()
                self.status_label.set_status(UIConstants.STATUS_PLAYING, UIConstants.STATUS_COLOR_PROCESSING)
                
                # Set playing flag and start monitoring playback
                self.is_playing = True
                self._monitor_playback()
            except Exception as e:
                self.status_label.set_error(f"Error playing audio: {str(e)}")
        else:
            self.status_label.set_status(UIConstants.STATUS_NO_AUDIO_FILE, UIConstants.STATUS_COLOR_WARNING)
    
    def on_stop_audio(self):
        """Handle stop button click."""
        pygame.mixer.music.stop()
        
        # Update UI state and playing flag
        self._reset_audio_controls(UIConstants.STATUS_STOPPED)
    
    def on_download_audio(self):
        """Handle download button click."""
        audio_file = self.audio_controls.get_audio_file()
        if not audio_file or not audio_file.exists():
            self.status_label.set_status(UIConstants.STATUS_NO_AUDIO_FILE, UIConstants.STATUS_COLOR_WARNING)
            return
        
        # Get the file extension from the current audio file
        file_extension = audio_file.suffix
        
        # Open file dialog to choose download location
        save_path = filedialog.asksaveasfilename(
            title="Save Audio File",
            defaultextension=file_extension,
            filetypes=[
                ("Audio Files", f"*{file_extension}"),
            ],
            initialfile=audio_file.name
        )
        
        if save_path:
            try:
                # Copy the file to the selected location
                shutil.copy2(audio_file, save_path)
                self.status_label.set_status(UIConstants.STATUS_DOWNLOAD_SUCCESS, UIConstants.STATUS_COLOR_SUCCESS)
            except Exception as e:
                self.status_label.set_error(f"Error downloading audio: {str(e)}")
        else:
            # User cancelled the download
            self.status_label.set_status(UIConstants.STATUS_DOWNLOAD_CANCELLED, UIConstants.STATUS_COLOR_READY)
    
    def _reset_audio_controls(self, status_message):
        """Reset audio control states and playing flag with status update.
        
        Args:
            status_message (str): Status message to display
        """
        self.is_playing = False
        self.audio_controls.set_stopped_state()
        self.status_label.set_status(status_message, UIConstants.STATUS_COLOR_READY)
    
    def _monitor_playback(self):
        """Monitor audio playback and reset control states when finished."""
        if self.is_playing:
            # Check if audio is still playing
            if not pygame.mixer.music.get_busy():
                # Audio has finished playing naturally
                self._reset_audio_controls(UIConstants.STATUS_READY)
            else:
                # Audio is still playing, check again after the monitoring interval
                self.root.after(UIConstants.AUDIO_MONITOR_INTERVAL_MS, self._monitor_playback)
