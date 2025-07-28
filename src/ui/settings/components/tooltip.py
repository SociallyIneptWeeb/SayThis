import customtkinter


class ToolTip:
    """A tooltip component for displaying helpful information on hover."""
    
    def __init__(self, widget, text):
        """Initialize the tooltip.
        
        Args:
            widget: The widget to attach the tooltip to
            text: The text to display in the tooltip
        """
        self.widget = widget
        self.text = text
        self.tooltip_label = None
        self.widget.bind("<Enter>", self.show_tooltip)
        self.widget.bind("<Leave>", self.hide_tooltip)

    def show_tooltip(self, event=None):
        """Show the tooltip."""
        try:
            # Get widget position and dimensions
            x = self.widget.winfo_rootx() + 20  # Adjust offset as needed
            y = self.widget.winfo_rooty() + 20  # Adjust offset as needed

            # Create tooltip label
            self.tooltip_label = customtkinter.CTkToplevel(self.widget)
            self.tooltip_label.geometry(f"+{x}+{y}")
            
            # Create the tooltip content
            label = customtkinter.CTkLabel(
                self.tooltip_label, 
                text=self.text,
                fg_color="lightyellow", 
                wraplength=300,  # Wrap text for long tooltips
            )
            label.pack()
        except Exception:
            # Handle case where widget is destroyed
            pass

    def hide_tooltip(self, event=None):
        """Hide the tooltip."""
        if self.tooltip_label:
            try:
                self.tooltip_label.destroy()
            except Exception:
                # Handle case where tooltip is already destroyed
                pass
            finally:
                self.tooltip_label = None


