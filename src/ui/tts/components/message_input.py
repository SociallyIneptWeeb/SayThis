import customtkinter

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
        self.message_label = customtkinter.CTkLabel(
            self.parent, 
            text="Enter your message:",
        )
        self.message_label.pack(side=customtkinter.TOP, anchor=customtkinter.W, pady=(0, 5))
        
        self.message_text = customtkinter.CTkTextbox(
            self.parent, 
            height=4,
            wrap="word",
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.message_text.pack(fill=customtkinter.BOTH, expand=True, pady=(0, UIConstants.FRAME_PADDING))
        
        self.message_text.focus_set()
    
    def get_text(self):
        """Get the current text content.
        
        Returns:
            str: The text content without trailing newline
        """
        return self.message_text.get("1.0", "end")
    
    def clear_text(self):
        """Clear the text input field."""
        self.message_text.delete("1.0", "end")
        self.message_text.focus_set()
    
    def is_empty(self):
        """Check if the message input is empty or contains only whitespace.
        
        Returns:
            bool: True if empty or whitespace only
        """
        return not self.get_text().strip()


