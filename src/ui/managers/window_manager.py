import tkinter as tk
from tkinter import ttk

from ..constants import UIConstants


class WindowManager:
    """Component for managing window setup, styling, and window-related operations."""
    
    def __init__(self):
        """Initialize the window manager."""
        self.root = None
    
    def setup_window(self):
        """Set up the main window properties.
        
        Returns:
            tk.Tk: The configured root window
        """
        self.root = tk.Tk()
        self.root.title(UIConstants.WINDOW_TITLE)
        self.root.geometry(
            f"{UIConstants.DEFAULT_WINDOW_WIDTH}x{UIConstants.DEFAULT_WINDOW_HEIGHT}"
        )
        self.root.minsize(UIConstants.MIN_WINDOW_WIDTH, UIConstants.MIN_WINDOW_HEIGHT)
        self.root.resizable(True, True)
        
        # Configure styles
        self._configure_styles()
        
        return self.root
    
    def _configure_styles(self):
        """Configure the ttk styles."""
        style = ttk.Style()
        style.configure(
            "TLabel", 
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)
        )
        style.configure(
            "TButton", 
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)
        )
        style.configure(
            "TEntry", 
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)
        )
    
    def center_window(self):
        """Center the window on the screen."""
        if not self.root:
            return
            
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def bind_resize_event(self, callback):
        """Bind window resize event to a callback.
        
        Args:
            callback: Function to call when window is resized
        """
        if self.root:
            self.root.bind("<Configure>", callback)
    
    def set_close_protocol(self, callback):
        """Set the window close protocol.
        
        Args:
            callback: Function to call when window is closed
        """
        if self.root:
            self.root.protocol("WM_DELETE_WINDOW", callback)
    
    def start_mainloop(self):
        """Start the GUI main loop."""
        if self.root:
            self.root.mainloop()
    
    def destroy(self):
        """Destroy the window."""
        if self.root:
            self.root.destroy()
    
    def update_idletasks(self):
        """Update idle tasks."""
        if self.root:
            self.root.update_idletasks()
