import tkinter as tk
from tkinter import ttk
from ...constants import UIConstants


class ControlButtons:
    """Component for generate and clear action buttons."""
    
    def __init__(self, parent, on_generate, on_clear):
        """Initialize the control buttons component.
        
        Args:
            parent: The parent widget to contain this component
            on_generate: Callback function for generate button click
            on_clear: Callback function for clear button click
        """
        self.parent = parent
        self.on_generate = on_generate
        self.on_clear = on_clear
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the control button widgets."""
        self.button_frame = ttk.Frame(self.parent)
        self.button_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.generate_button = ttk.Button(
            self.button_frame, 
            text="Generate Audio",
            command=self.on_generate
        )
        self.generate_button.pack(side=tk.RIGHT, padx=UIConstants.BUTTON_PADDING)
        
        self.clear_button = ttk.Button(
            self.button_frame, 
            text="Clear",
            command=self.on_clear
        )
        self.clear_button.pack(side=tk.RIGHT, padx=UIConstants.BUTTON_PADDING)
    
    def set_generate_enabled(self, enabled):
        """Enable or disable the generate button.
        
        Args:
            enabled (bool): Whether to enable the button
        """
        state = UIConstants.STATE_NORMAL if enabled else UIConstants.STATE_DISABLED
        self.generate_button.configure(state=state)
