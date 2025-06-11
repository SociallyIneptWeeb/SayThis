import tkinter as tk
from tkinter import ttk
from .constants import UIConstants


class ControlButtons:
    """Component for generate and clear action buttons."""
    
    def __init__(self, parent, on_generate_callback, on_clear_callback):
        """Initialize the control buttons component.
        
        Args:
            parent: The parent widget to contain this component
            on_generate_callback: Callback function for generate button
            on_clear_callback: Callback function for clear button
        """
        self.parent = parent
        self.on_generate_callback = on_generate_callback
        self.on_clear_callback = on_clear_callback
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the control button widgets."""
        # Button frame
        self.button_frame = ttk.Frame(self.parent)
        self.button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Generate button
        self.generate_button = ttk.Button(
            self.button_frame, 
            text=UIConstants.GENERATE_BUTTON_TEXT, 
            command=self.on_generate_callback
        )
        self.generate_button.pack(side=tk.RIGHT, padx=UIConstants.BUTTON_PADDING)
        
        # Clear button
        self.clear_button = ttk.Button(
            self.button_frame, 
            text=UIConstants.CLEAR_BUTTON_TEXT, 
            command=self.on_clear_callback
        )
        self.clear_button.pack(side=tk.RIGHT, padx=UIConstants.BUTTON_PADDING)
    
    def set_generate_enabled(self, enabled):
        """Enable or disable the generate button.
        
        Args:
            enabled (bool): Whether to enable the button
        """
        state = UIConstants.STATE_NORMAL if enabled else UIConstants.STATE_DISABLED
        self.generate_button.configure(state=state)
