import tkinter as tk
from tkinter import ttk

from .constants import UIConstants
from .message_input import MessageInput
from .control_buttons import ControlButtons
from .status_label import StatusLabel
from .audio_controls import AudioControls


class MainWindow:
    """Main window that coordinates all UI components."""
    
    def __init__(self, app):
        """Initialize the main window.
        
        Args:
            app: The Application instance that this window will control
        """
        self.app = app
        self._setup_window()
        self._create_components()
        self._center_window()
        
        # Bind resize event to update wrap length
        self.root.bind("<Configure>", self._on_window_resize)
    
    def _setup_window(self):
        """Set up the main window properties."""
        self.root = tk.Tk()
        self.root.title(UIConstants.WINDOW_TITLE)
        self.root.geometry(
            f"{UIConstants.DEFAULT_WINDOW_WIDTH}x{UIConstants.DEFAULT_WINDOW_HEIGHT}"
        )
        self.root.minsize(UIConstants.MIN_WINDOW_WIDTH, UIConstants.MIN_WINDOW_HEIGHT)
        self.root.resizable(True, True)
        
        # Configure styles
        self._configure_styles()
    
    def _configure_styles(self):
        """Configure the ttk styles."""
        style = ttk.Style()
        style.configure(
            "TLabel", 
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)
        )
        style.configure(
            "TButton", 
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)
        )
        style.configure(
            "TEntry", 
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)
        )
    
    def _create_components(self):
        """Create and layout all UI components."""
        # Main frame
        self.main_frame = ttk.Frame(
            self.root,
            padding=f"{UIConstants.FRAME_PADDING} {UIConstants.FRAME_PADDING} "
                    f"{UIConstants.FRAME_PADDING} {UIConstants.FRAME_PADDING}"
        )
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create components
        self.message_input = MessageInput(self.main_frame)
        self.control_buttons = ControlButtons(
            self.main_frame, 
            self._on_generate, 
            self._on_clear
        )
        self.status_label = StatusLabel(self.main_frame)
        self.audio_controls = AudioControls(self.main_frame, self.status_label)
    
    def _on_generate(self):
        """Handle generate button click."""
        if self.message_input.is_empty():
            self.status_label.set_empty_message_warning()
            return
        
        try:
            self.control_buttons.set_generate_enabled(False)
            self.status_label.set_generating()
            self.root.update_idletasks()

            message = self.message_input.get_text()
            output_path = self.app.generate_audio(message)
            
            # Show success message and enable playback
            self.audio_controls.set_audio_file(output_path)
            self.status_label.set_success()
            
        except RuntimeError as e:
            self.status_label.set_error(str(e))
        except Exception as e:
            self.status_label.set_error(f"Unexpected error: {str(e)}")
        finally:
            self.control_buttons.set_generate_enabled(True)
    
    def _on_clear(self):
        """Handle clear button click."""
        self.message_input.clear_text()
    
    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _on_window_resize(self, event):
        """Handle window resize event to update status label wrap length.
        
        Args:
            event: The Configure event triggered by window resize
        """
        # Only process if the event is from the main window
        if event.widget == self.root:
            # Update wrap length to be slightly less than the window width
            new_width = event.width - UIConstants.WINDOW_PADDING_ADJUST
            self.status_label.update_wrap_length(new_width)
    
    def run(self):
        """Start the GUI main loop."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()
    
    def _on_close(self):
        """Clean up resources and close the application."""
        self.audio_controls.cleanup()
        self.root.destroy()
