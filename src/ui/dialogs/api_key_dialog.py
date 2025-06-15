import tkinter as tk
from tkinter import ttk

from ..constants import UIConstants


class ApiKeyDialog:
    """Dialog for entering and updating the API key."""
    
    def __init__(self, parent, current_api_key):
        """Initialize the API key dialog.
        
        Args:
            parent: The parent window
            current_api_key (str): The current API key to display in the entry field
        """
        self.parent = parent
        self.current_api_key = current_api_key
        self.result = None
        # StringVar to hold the API key input
        self.api_key_var = tk.StringVar(value=current_api_key)
    
    def show(self):
        """Show the API key input dialog.
        
        Returns:
            str or None: The entered API key, or None if cancelled
        """
        # Create the dialog window
        dialog = tk.Toplevel(self.parent)
        dialog.title(UIConstants.API_KEY_DIALOG_TITLE)
        dialog.geometry(f"{UIConstants.API_KEY_DIALOG_WIDTH}x{UIConstants.API_KEY_DIALOG_HEIGHT}")
        dialog.resizable(False, False)
        dialog.transient(self.parent)
        dialog.grab_set()
        
        # Center the dialog on the parent window
        self._center_dialog(dialog)
        
        # Create the main frame
        main_frame = ttk.Frame(dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the label
        label = ttk.Label(
            main_frame, 
            text=UIConstants.API_KEY_DIALOG_LABEL,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)
        )
        label.pack(pady=(0, 10))
        
        # Create the entry field
        entry = ttk.Entry(
            main_frame,
            textvariable=self.api_key_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            width=UIConstants.API_KEY_ENTRY_WIDTH,
            show=UIConstants.API_KEY_ENTRY_SHOW_CHAR  # Hide the API key for security
        )
        entry.pack(pady=(0, 20), fill=tk.X)
        entry.focus()
        
        # Create button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        # Create buttons
        ok_button = ttk.Button(
            button_frame,
            text="OK",
            command=lambda: self._on_ok(dialog)
        )
        ok_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        cancel_button = ttk.Button(
            button_frame,
            text="Cancel",
            command=lambda: self._on_cancel(dialog)
        )
        cancel_button.pack(side=tk.RIGHT)
        
        dialog.bind('<Return>', lambda e: self._on_ok(dialog))
        dialog.bind('<Escape>', lambda e: self._on_cancel(dialog))
        
        # Wait for the dialog to close
        dialog.wait_window()
        
        return self.result
    
    def _center_dialog(self, dialog):
        """Center the dialog on the parent window.
        
        Args:
            dialog: The dialog window to center
        """
        dialog.update_idletasks()
        
        # Get parent window position and size
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        # Get dialog size
        dialog_width = dialog.winfo_width()
        dialog_height = dialog.winfo_height()
        
        # Calculate position to center dialog on parent
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        dialog.geometry(f"+{x}+{y}")
    
    def _on_ok(self, dialog):
        """Handle OK button click.
        
        Args:
            dialog: The dialog window
        """
        api_key = self.api_key_var.get().strip()
        self.result = api_key
        dialog.destroy()

    def _on_cancel(self, dialog):
        """Handle Cancel button click.
        
        Args:
            dialog: The dialog window
        """
        self.result = None
        dialog.destroy()
