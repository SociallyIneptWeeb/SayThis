import tkinter as tk
from tkinter import ttk

from .constants import UIConstants
from .tts import TTSTab
from .settings import SettingsTab


class UI:
    """Main UI class that contains the TTS tab and Settings tab."""
    
    def __init__(self, app):
        """Initialize the main UI.
        
        Args:
            app: The Application instance that this UI will control
        """
        self.app = app
        
        # Create the main window
        self.root = tk.Tk()
        self._setup_window()
        
        # Create the notebook (tab container)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self._create_tabs()
        self._center_window()
    
    def _setup_window(self):
        """Configure the main window properties."""
        self.root.title("SayThis - Text to Speech")
        self.root.geometry(f"{UIConstants.DEFAULT_WINDOW_WIDTH}x{UIConstants.DEFAULT_WINDOW_HEIGHT}")
        self.root.minsize(UIConstants.MIN_WINDOW_WIDTH, UIConstants.MIN_WINDOW_HEIGHT)
    
    def _create_tabs(self):
        """Create all tabs for the application."""
        self.tts_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.tts_frame, text="Text to Speech")
        self.tts_tab = TTSTab(self.app, parent=self.tts_frame)

        self.settings_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_frame, text="Settings")
        self.settings_tab = SettingsTab(
            self.app, 
            parent=self.settings_frame,
        )
    
    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def run(self):
        """Start the GUI main loop."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()
    
    def _on_close(self):
        """Clean up resources and close the application."""
        self.tts_tab.on_close()
        self.root.destroy()
