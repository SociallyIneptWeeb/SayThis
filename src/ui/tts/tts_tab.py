import tkinter as tk
from tkinter import ttk

from ..constants import UIConstants
from .components import MessageInput, ControlButtons, StatusLabel, AudioControls


class TTSTab:
    """TTS tab that coordinates all TTS UI components."""
    
    def __init__(self, app, parent):
        """Initialize the TTS tab.
        
        Args:
            app: The Application instance that this tab will control
            parent: The parent widget (tab frame)
        """
        self.app = app
        self.root = parent
        
        self._create_components()
    
    def _create_components(self):
        """Create and layout all UI components."""
        self.tts_frame = ttk.Frame(
            self.root,
            padding=f"{UIConstants.FRAME_PADDING} {UIConstants.FRAME_PADDING} "
                    f"{UIConstants.FRAME_PADDING} {UIConstants.FRAME_PADDING}"
        )
        self.tts_frame.pack(fill=tk.BOTH, expand=True)
        
        self.message_input = MessageInput(self.tts_frame)
        self.control_buttons = ControlButtons(self.tts_frame, self._handle_generate, self._handle_clear)
        self.audio_controls = AudioControls(self.tts_frame, self._handle_audio_error)
        self.status_label = StatusLabel(self.tts_frame)
        
        # Bind window resize event to update text wrapping
        self.tts_frame.bind("<Configure>", self._on_frame_configure)
    
    def on_close(self):
        """Clean up resources."""
        self.audio_controls.cleanup()
    
    def _handle_generate(self):
        """Handle a request to generate audio."""
        message = self.message_input.get_text()
        
        if not message or not message.strip():
            self.status_label.set_status(
                "⚠️ Please enter a message to convert to speech.", 
                UIConstants.STATUS_COLOR_WARNING
            )
            return
        
        try:
            # Stop and unload any currently playing audio
            self.audio_controls.stop_and_unload_audio()
            
            self.control_buttons.set_generate_enabled(False)
            self.status_label.set_status(
                "⏳ Generating audio...", 
                UIConstants.STATUS_COLOR_PROCESSING
            )

            # Update UI to show the status change
            self.tts_frame.update_idletasks()

            output_path = self.app.generate_audio(message)
            
            # Show success message and enable playback
            self.audio_controls.set_audio_file(output_path)
            self.status_label.set_status(
                "✅ Audio generated successfully!", 
                UIConstants.STATUS_COLOR_SUCCESS
            )
            
        except RuntimeError as e:
            self.status_label.set_error(str(e))
        except Exception as e:
            self.status_label.set_error(f"Unexpected error: {str(e)}")
        finally:
            self.control_buttons.set_generate_enabled(True)
    
    def _handle_clear(self):
        """Handle a request to clear the message input."""
        self.message_input.clear_text()
    
    def _handle_audio_error(self, error_message):
        """Handle errors from audio controls.
        
        Args:
            error_message (str): The error message to display
        """
        self.status_label.set_error(error_message)

    def _on_frame_configure(self, event):
        """Handle the frame configure event to update text wrapping.
        
        Args:
            event: The configure event
        """
        if event.widget == self.tts_frame:
            self.status_label.update_wrap_length(event.width - UIConstants.WINDOW_PADDING_ADJUST)
