import tkinter as tk


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
            self.tooltip_label = tk.Toplevel(self.widget)
            self.tooltip_label.wm_overrideredirect(True)
            self.tooltip_label.wm_geometry(f"+{x}+{y}")
            
            # Create the tooltip content
            label = tk.Label(
                self.tooltip_label, 
                text=self.text,
                background="lightyellow", 
                relief="solid", 
                borderwidth=1,
                wraplength=300,  # Wrap text for long tooltips
                justify="left",
                padx=5,
                pady=3
            )
            label.pack()
        except tk.TclError:
            # Handle case where widget is destroyed
            pass

    def hide_tooltip(self, event=None):
        """Hide the tooltip."""
        if self.tooltip_label:
            try:
                self.tooltip_label.destroy()
            except tk.TclError:
                # Handle case where tooltip is already destroyed
                pass
            finally:
                self.tooltip_label = None
