import tkinter as tk
from tkinter import ttk
from ..constants import UIConstants


class MessageInput:
    """Component for text message input with scrollbar."""
    
    def __init__(self, parent):
        """Initialize the message input component.
        
        Args:
            parent: The parent widget to contain this component
        """
        self.parent = parent
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the message input widgets."""
        # Message label
        self.message_label = ttk.Label(
            self.parent, 
            text=UIConstants.MESSAGE_LABEL_TEXT
        )
        self.message_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Message input field frame
        self.message_frame = ttk.Frame(self.parent)
        self.message_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Text widget
        self.message_text = tk.Text(
            self.message_frame, 
            height=UIConstants.TEXT_HEIGHT,
            width=UIConstants.TEXT_WIDTH,
            wrap=tk.WORD,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            padx=UIConstants.TEXT_PADDING,
            pady=UIConstants.TEXT_PADDING
        )
        self.message_text.pack(fill=tk.X, expand=True, side=tk.LEFT)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(
            self.message_frame, 
            command=self.message_text.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text.config(yscrollcommand=self.scrollbar.set)
        
        # Set initial focus to the text widget
        self.message_text.focus_set()
    
    def get_text(self):
        """Get the current text content.
        
        Returns:
            str: The text content without trailing newline
        """
        return self.message_text.get("1.0", "end-1c")
    
    def clear_text(self):
        """Clear the text input field."""
        self.message_text.delete("1.0", tk.END)
        self.message_text.focus_set()
    
    def is_empty(self):
        """Check if the message input is empty or contains only whitespace.
        
        Returns:
            bool: True if empty or whitespace only
        """
        return not self.get_text().strip()
