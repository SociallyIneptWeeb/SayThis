import tkinter as tk
from tkinter import ttk
from ...constants import UIConstants


class StatusLabel:
    """Component for displaying status messages."""
    
    def __init__(self, parent):
        """Initialize the status label component.
        
        Args:
            parent: The parent widget to contain this component
        """
        self.parent = parent
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the status label widget."""
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            self.parent, 
            textvariable=self.status_var,
            foreground=UIConstants.STATUS_COLOR_READY,
            wraplength=UIConstants.DEFAULT_WRAP_LENGTH,
        )
        self.status_label.pack(side=tk.TOP, anchor=tk.W, pady=(10, 0), fill=tk.X)
    
    def set_status(self, message, color="gray"):
        """Set the status message and color.
        
        Args:
            message (str): The status message to display
            color (str): The text color (default: "gray")
        """
        self.status_var.set(message)
        self.status_label.configure(foreground=color)
    
    def set_error(self, error_message):
        """Set an error status message.
        
        Args:
            error_message (str): The error message to display
        """
        self.set_status(f"❌ {error_message}", UIConstants.STATUS_COLOR_ERROR)
    
    def update_wrap_length(self, width):
        """Update the wrap length based on window width.
        
        Args:
            width (int): The new width for wrapping
        """
        self.status_label.configure(wraplength=width)
