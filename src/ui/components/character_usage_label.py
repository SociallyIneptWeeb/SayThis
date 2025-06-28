import tkinter as tk
from tkinter import ttk
from ..constants import UIConstants


class CharacterUsageLabel:
    """Component for displaying character usage information."""
    
    def __init__(self, parent):
        """Initialize the character usage label component.
        
        Args:
            parent: The parent widget to contain this component
        """
        self.parent = parent
        self.character_limit = None
        self._create_widgets()
    
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
