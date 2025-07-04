import tkinter as tk
from tkinter import ttk
from ...constants import UIConstants


class CharacterUsageLabel:
    """Component for displaying character usage information."""
    
    def __init__(self, parent, app):
        """Initialize the character usage label component.
        
        Args:
            parent: The parent widget to contain this component
            app: The Application instance for fetching usage data
        """
        self.parent = parent
        self.app = app
        self.character_limit = None
        self._create_widgets()
    
    def _has_api_key(self):
        """Check if the current service has an API key configured."""
        config = self.app.get_service_config()
        return bool(config.get("api_key", "").strip())
  
    def _create_widgets(self):
        """Create the character usage label widget and refresh button."""
        self.usage_frame = ttk.Frame(self.parent)
        self.usage_frame.pack(anchor=tk.W, pady=(UIConstants.TEXT_PADDING, 0), fill=tk.X)
        
        self.usage_var = tk.StringVar()
        self.usage_label = ttk.Label(
            self.usage_frame, 
            textvariable=self.usage_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
        )
        self.usage_label.pack(side=tk.LEFT, anchor=tk.W)
        
        self.button_frame = ttk.Frame(self.parent)
        self.button_frame.pack(anchor=tk.W, pady=(UIConstants.BUTTON_PADDING, 0), fill=tk.X)
        
        self.refresh_button = ttk.Button(
            self.button_frame,
            text="Refresh Usage",
            command=self._refresh_usage
        )
        self.refresh_button.pack(side=tk.LEFT, anchor=tk.W)

    def set_label(self, message, color="black"):
        """Set the label text and color."""
        self.usage_var.set(message)
        self.usage_label.config(foreground=color)

    def _refresh_usage(self):
        """Refresh character usage with loading state."""
        self.set_label(UIConstants.CHARACTER_USAGE_FORMAT.format(
            UIConstants.UNSET_USAGE,
            self.character_limit if self.character_limit else UIConstants.UNSET_USAGE
        ))
        self.usage_frame.update_idletasks()
        self.load_character_usage()

    def load_character_usage(self):
        """Load and display character usage information."""
        if not self._has_api_key():
            self.character_limit = None
            self.set_label(UIConstants.CHARACTER_USAGE_FORMAT.format(
                UIConstants.UNSET_USAGE,
                self.character_limit if self.character_limit else UIConstants.UNSET_USAGE
            ))
            return

        try:
            character_count, character_limit = self.app.get_character_usage()
            usage_text = UIConstants.CHARACTER_USAGE_FORMAT.format(character_count, character_limit)
            self.set_label(usage_text)
            self.character_limit = character_limit
        except Exception as e:
            self.set_label(f"Error loading usage: {str(e)}", color="red")
