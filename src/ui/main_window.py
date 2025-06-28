import tkinter as tk
from tkinter import ttk

from .constants import UIConstants
from .components import MessageInput, ControlButtons, StatusLabel, AudioControls, CharacterUsageLabel
from .managers import WindowManager, MenuManager, EventHandler


class MainWindow:
    """Main window that coordinates all UI components."""
    
    def __init__(self, app):
        """Initialize the main window.
        
        Args:
            app: The Application instance that this window will control
        """
        self.app = app
        
        # Initialize managers and components
        self.window_manager = WindowManager()
        self.root = self.window_manager.setup_window()
        
        # Create UI components first
        self._create_components()
        
        # Initialize managers that depend on components
        self.menu_manager = MenuManager(self.root, self.app, self.status_label, self._on_api_key_updated)
        self.event_handler = EventHandler(
            self.app,
            self.root,
            self.message_input, 
            self.control_buttons, 
            self.status_label, 
            self.audio_controls,
            self.character_usage_label
        )
        
        # Setup menu and window features
        self.menu_manager.create_menu_bar()
        self.window_manager.center_window()
        
        # Bind events
        self.window_manager.bind_resize_event(self._on_window_resize)
    
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
        self.character_usage_label = CharacterUsageLabel(self.main_frame)
        self.status_label = StatusLabel(self.main_frame)
        self.audio_controls = AudioControls(
            self.main_frame, 
            self._on_play_audio, 
            self._on_stop_audio, 
            self._on_download_audio
        )
    
    def _on_generate(self):
        """Handle generate button click."""
        self.event_handler.on_generate()
    
    def _on_clear(self):
        """Handle clear button click."""
        self.event_handler.on_clear()
    
    def _on_play_audio(self):
        """Handle play audio button click."""
        self.event_handler.on_play_audio()
    
    def _on_stop_audio(self):
        """Handle stop audio button click."""
        self.event_handler.on_stop_audio()
    
    def _on_download_audio(self):
        """Handle download audio button click."""
        self.event_handler.on_download_audio()

    def _on_window_resize(self, event):
        """Handle window resize event to update status label wrap length.
        
        Args:
            event: The Configure event triggered by window resize
        """
        self.event_handler.on_window_resize(event)
    
    def refresh_character_usage(self):
        """Refresh the character usage display."""
        self.event_handler.load_character_usage()

    def _on_api_key_updated(self):
        """Handle API key being updated to refresh character usage."""
        self.refresh_character_usage()
    
    def run(self):
        """Start the GUI main loop."""
        self.window_manager.set_close_protocol(self._on_close)
        self.window_manager.start_mainloop()
    
    def _on_close(self):
        """Clean up resources and close the application."""
        self.event_handler.on_close()
        self.window_manager.destroy()
