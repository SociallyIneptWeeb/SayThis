import tkinter as tk
from tkinter import ttk, messagebox
from ...constants import UIConstants


class SaveButton:
    """Component for the save settings button."""
    
    def __init__(self, parent, on_save):
        """Initialize the save button component.
        
        Args:
            parent: The parent widget to contain this component
            on_save: Callback function when save button is clicked
        """
        self.parent = parent
        self.on_save = on_save
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the save button widget."""
        save_button = ttk.Button(
            self.parent,
            text="Save Settings",
            command=self._handle_save,
            width=20,
        )
        save_button.pack(anchor=tk.CENTER)
    
    def _handle_save(self):
        """Handle save button click."""
        self.on_save()
    
    def show_dialog(self, message, is_error=False):
        """Show a dialog popup with the status message.
        
        Args:
            message (str): The message to display
            is_error (bool): Whether this is an error message (default: False)
        """
        if is_error:
            messagebox.showerror("Error", message)
        else:
            messagebox.showinfo("Success", message)
