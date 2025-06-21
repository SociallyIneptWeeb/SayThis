from ..constants import UIConstants


class EventHandler:
    """Component for handling all event callbacks and business logic for the main window."""
    
    def __init__(self, app, root, message_input, control_buttons, status_label, audio_controls):
        """Initialize the event handler.
        
        Args:
            app: The Application instance
            root: The root window
            message_input: The message input component
            control_buttons: The control buttons component
            status_label: The status label component
            audio_controls: The audio controls component
        """
        self.app = app
        self.root = root
        self.message_input = message_input
        self.control_buttons = control_buttons
        self.status_label = status_label
        self.audio_controls = audio_controls
    
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
            self.control_buttons.set_generate_enabled(False)
            self.status_label.set_status(
                UIConstants.STATUS_GENERATING, 
                UIConstants.STATUS_COLOR_PROCESSING
            )
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
        self.audio_controls.cleanup()
