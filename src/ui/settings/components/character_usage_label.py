import customtkinter

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
  
    def _create_widgets(self):
        """Create the character usage label widget and refresh button."""
        self.usage_frame = customtkinter.CTkFrame(self.parent, fg_color="transparent")
        self.usage_frame.pack(anchor=customtkinter.W, pady=(UIConstants.TEXT_PADDING, 0), fill=customtkinter.X)
        
        self.usage_var = customtkinter.StringVar()
        self.usage_label = customtkinter.CTkLabel(
            self.usage_frame, 
            textvariable=self.usage_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            anchor="w",
        )
        self.usage_label.pack(side=customtkinter.LEFT, anchor=customtkinter.W)
        
        self.button_frame = customtkinter.CTkFrame(self.parent, fg_color="transparent")
        self.button_frame.pack(anchor=customtkinter.W, pady=(UIConstants.BUTTON_PADDING, 0), fill=customtkinter.X)
        
        self.refresh_button = customtkinter.CTkButton(
            self.button_frame,
            text="Refresh Usage",
            command=self._refresh_usage,
            corner_radius=UIConstants.CORNER_RADIUS,
        )
        self.refresh_button.pack(side=customtkinter.LEFT, anchor=customtkinter.W)

    def _show_refresh_button(self):
        """Show the refresh button."""
        self.button_frame.pack(anchor=customtkinter.W, pady=(UIConstants.BUTTON_PADDING, 0), fill=customtkinter.X)

    def _hide_refresh_button(self):
        """Hide the refresh button."""
        self.button_frame.pack_forget()

    def set_label(self, message, color="black"):
        """Set the label text and color."""
        self.usage_var.set(message)
        self.usage_label.configure(text_color=color)

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
        if not self.app.is_service_initialized():
            self.character_limit = None
            self.set_label(UIConstants.CHARACTER_USAGE_FORMAT.format(UIConstants.UNSET_USAGE, UIConstants.UNSET_USAGE))
            return

        try:
            character_count, character_limit = self.app.get_character_usage()
            
            # Handle case where usage tracking is not available
            if character_count == -1 and character_limit == -1:
                self.set_label(UIConstants.CHARACTER_USAGE_NOT_AVAILABLE, color="gray")
                self._hide_refresh_button()
            else:
                usage_text = UIConstants.CHARACTER_USAGE_FORMAT.format(character_count, character_limit)
                self.set_label(usage_text)
                self.character_limit = character_limit
                self._show_refresh_button()
        except Exception as e:
            self.set_label(f"Error loading usage: {str(e)}", color="red")
            self._show_refresh_button()


