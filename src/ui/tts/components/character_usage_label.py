import tkinter as tk
from tkinter import ttk
from ...constants import UIConstants


class CharacterUsageLabel:
    """Component for displaying character usage information with integrated handling."""
    
    def __init__(self, parent, app, status_label):
        """Initialize the character usage label component.
        
        Args:
            parent: The parent widget to contain this component
            app: The Application instance for fetching usage data
            status_label: The status label component for displaying errors
        """
        self.parent = parent
        self.app = app
        self.status_label = status_label
        self.character_limit = None
        self._create_widgets()
        
        # Load initial character usage only if API key is configured
        if self.app.get_api_key():
            self.load_character_usage()
    
    def _create_widgets(self):
        """Create the character usage label widget."""
        placeholder_text = UIConstants.CHARACTER_USAGE_FORMAT.format(UIConstants.UNSET_USAGE, UIConstants.UNSET_USAGE)
        self.usage_var = tk.StringVar(value=placeholder_text)
        self.usage_label = ttk.Label(
            self.parent, 
            textvariable=self.usage_var,
            foreground="gray",
        )
        self.usage_label.pack(anchor=tk.E, pady=(UIConstants.TEXT_PADDING, 0))
    
    def update_usage(self, character_count, character_limit):
        """Update the character usage display.
        
        Args:
            character_count (int): Current character count used
            character_limit (int): Maximum character limit
        """
        usage_text = UIConstants.CHARACTER_USAGE_FORMAT.format(character_count, character_limit)
        self.usage_var.set(usage_text)
        self.character_limit = character_limit
    
    def set_loading(self):
        """Set the label to show loading state."""
        self.usage_var.set(UIConstants.CHARACTER_USAGE_FORMAT.format(
            UIConstants.UNSET_USAGE,
            self.character_limit if self.character_limit else UIConstants.UNSET_USAGE
        ))
    
    def set_error(self):
        """Set the label to show error state (same as loading)."""
        self.set_loading()
    
    def load_character_usage(self):
        """Load and display character usage information."""
        try:
            character_count, character_limit = self.app.get_character_usage()
            self.update_usage(character_count, character_limit)
        except Exception as e:
            self.set_error()
            self.status_label.set_error(f"Unable to load character usage: {str(e)}")
    
    def schedule_usage_update(self, root, delay_ms=8000):
        """Schedule a character usage update after a delay.
        
        Args:
            root: The root widget for scheduling callbacks
            delay_ms (int): Delay in milliseconds before updating
        """
        root.after(delay_ms, self.load_character_usage)
