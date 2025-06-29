import tkinter as tk
from tkinter import ttk

from ..constants import UIConstants
from .components import MessageInput, ControlButtons, StatusLabel, AudioControls, CharacterUsageLabel


class TTSTab:
    """TTS tab that coordinates all UI components in tab mode."""
    
    def __init__(self, app, parent):
        """Initialize the TTS tab.
        
        Args:
            app: The Application instance that this tab will control
            parent: The parent widget (tab frame)
        """
        self.app = app
        self.root = parent
        
        # Create UI components first
        self._create_components()
    
    def _create_components(self):
        """Create and layout all UI components."""
        # TTS frame
        self.tts_frame = ttk.Frame(
            self.root,
            padding=f"{UIConstants.FRAME_PADDING} {UIConstants.FRAME_PADDING} "
                    f"{UIConstants.FRAME_PADDING} {UIConstants.FRAME_PADDING}"
        )
        self.tts_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create components with their dependencies
        self.status_label = StatusLabel(self.tts_frame)
        self.audio_controls = AudioControls(self.tts_frame, self.status_label)
        self.message_input = MessageInput(self.tts_frame)
        self.character_usage_label = CharacterUsageLabel(self.tts_frame, self.app, self.status_label)
        self.control_buttons = ControlButtons(
            self.tts_frame, 
            self.app,
            self.message_input,
            self.status_label,
            self.character_usage_label,
            self.audio_controls
        )
    
    def refresh_character_usage(self):
        """Refresh the character usage display."""
        self.character_usage_label.load_character_usage()
    
    def on_close(self):
        """Clean up resources."""
        self.audio_controls.cleanup()
