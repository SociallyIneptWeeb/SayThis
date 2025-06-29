import tkinter as tk
from tkinter import ttk
from ...constants import UIConstants


class ControlButtons:
    """Component for generate and clear action buttons with integrated TTS handling."""
    
    def __init__(self, parent, app, message_input, status_label, character_usage_label, audio_controls):
        """Initialize the control buttons component.
        
        Args:
            parent: The parent widget to contain this component
            app: The Application instance
            message_input: The message input component
            status_label: The status label component
            character_usage_label: The character usage label component
            audio_controls: The audio controls component
        """
        self.parent = parent
        self.app = app
        self.message_input = message_input
        self.status_label = status_label
        self.character_usage_label = character_usage_label
        self.audio_controls = audio_controls
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the control button widgets."""
        # Button frame
        self.button_frame = ttk.Frame(self.parent)
        self.button_frame.pack(fill=tk.X)
        
        # Generate button
        self.generate_button = ttk.Button(
            self.button_frame, 
            text=UIConstants.GENERATE_BUTTON_TEXT, 
            command=self._on_generate
        )
        self.generate_button.pack(side=tk.RIGHT, padx=UIConstants.BUTTON_PADDING)
        
        # Clear button
        self.clear_button = ttk.Button(
            self.button_frame, 
            text=UIConstants.CLEAR_BUTTON_TEXT, 
            command=self._on_clear
        )
        self.clear_button.pack(side=tk.RIGHT, padx=UIConstants.BUTTON_PADDING)
    
    def set_generate_enabled(self, enabled):
        """Enable or disable the generate button.
        
        Args:
            enabled (bool): Whether to enable the button
        """
        state = UIConstants.STATE_NORMAL if enabled else UIConstants.STATE_DISABLED
        self.generate_button.configure(state=state)
    
    def _on_generate(self):
        """Handle generate button click."""
        message = self.message_input.get_text()
        
        if not message or not message.strip():
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
            self.audio_controls.stop_and_unload_audio()
            
            self.set_generate_enabled(False)
            self.status_label.set_status(
                UIConstants.STATUS_GENERATING, 
                UIConstants.STATUS_COLOR_PROCESSING
            )
            self.character_usage_label.set_loading()

            # Update UI to show the status change
            self.parent.update_idletasks()

            output_path = self.app.generate_audio(message)
            
            # Show success message and enable playback
            self.audio_controls.set_audio_file(output_path)
            self.status_label.set_status(
                UIConstants.STATUS_GENERATE_SUCCESS, 
                UIConstants.STATUS_COLOR_SUCCESS
            )
            
            # Update character usage after successful generation (delayed to allow API to update)
            self.character_usage_label.schedule_usage_update(self.parent)
            
        except RuntimeError as e:
            self.status_label.set_error(str(e))
        except Exception as e:
            self.status_label.set_error(f"Unexpected error: {str(e)}")
        finally:
            self.set_generate_enabled(True)
    
    def _on_clear(self):
        """Handle clear button click."""
        self.message_input.clear_text()
