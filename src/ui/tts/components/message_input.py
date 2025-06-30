import tkinter as tk
from tkinter import ttk
from ...constants import UIConstants


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
        self.message_label = ttk.Label(
            self.parent, 
            text="Enter your message:",
        )
        self.message_label.pack(side=tk.TOP, anchor=tk.W, pady=(0, 5))
        
        self.message_frame = ttk.Frame(self.parent)
        self.message_frame.pack(side=tk.TOP, fill=tk.X, pady=(0, UIConstants.FRAME_PADDING))
        
        self.message_text = tk.Text(
            self.message_frame, 
            height=4,
            width=50,
            wrap=tk.WORD,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            padx=UIConstants.TEXT_PADDING,
            pady=UIConstants.TEXT_PADDING
        )
        self.message_text.pack(fill=tk.X, expand=True, side=tk.LEFT)
        
        self.scrollbar = ttk.Scrollbar(
            self.message_frame, 
            command=self.message_text.yview
        )
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text.config(yscrollcommand=self.scrollbar.set)
        
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
