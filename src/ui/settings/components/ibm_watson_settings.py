import tkinter as tk
from tkinter import ttk
from ...constants import UIConstants


class IBMWatsonSettings:
    """Component for IBM Watson-specific settings."""
    
    def __init__(self, parent, app):
        """Initialize the IBM Watson settings component.
        
        Args:
            parent: The parent widget to contain this component
            app: The Application instance
        """
        self.parent = parent
        self.app = app
        self.frame = ttk.Frame(parent)
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the IBM Watson settings widgets."""
        # API Key Configuration Section
        api_frame = ttk.Frame(self.frame)
        api_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(api_frame, text="IBM Watson API Key:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        self.api_key_var = tk.StringVar()
        self.api_key_entry = ttk.Entry(
            api_frame,
            textvariable=self.api_key_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            show=UIConstants.API_KEY_ENTRY_SHOW_CHAR,
            width=40
        )
        self.api_key_entry.pack(anchor=tk.W, pady=(0, 10))
    
    def pack(self, **kwargs):
        """Pack the component frame."""
        self.frame.pack(**kwargs)
    
    def pack_forget(self):
        """Hide the component frame."""
        self.frame.pack_forget()
    
    def load_settings(self):
        """Load settings from the application configuration."""
        config = self.app.get_service_config()
        self.api_key_var.set(config.get("api_key", ""))
    
    def get_settings(self):
        """Get the current settings from the UI.
        
        Returns:
            dict: Dictionary containing the IBM Watson settings
        """
        return {
            "api_key": self.api_key_var.get(),
            "file_extension": ".wav"
        }
