import customtkinter


class ScrollFrame(customtkinter.CTkScrollableFrame):
    """A scrollable frame component that can contain other widgets."""
    
    def __init__(self, parent):
        """Initialize the scrollable frame.
        
        Args:
            parent: The parent widget to contain this component
        """
        super().__init__(parent)
        self.viewPort = self


