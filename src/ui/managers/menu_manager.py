import tkinter as tk

from ..constants import UIConstants
from ..dialogs import ApiKeyDialog


class MenuManager:
    """Component for managing menu bar creation and menu-related functionality."""
    
    def __init__(self, root, app, status_label, on_api_key_updated):
        """Initialize the menu manager.
        
        Args:
            root: The root window
            app: The Application instance
            status_label: The status label component for displaying messages
            on_api_key_updated: Callback function to call when API key is updated
        """
        self.root = root
        self.app = app
        self.status_label = status_label
        self.on_api_key_updated = on_api_key_updated
    
    def create_menu_bar(self):
        """Create the menu bar with Settings menu."""
        # Create the menu bar
        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)
        
        # Create Settings menu
        settings_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(
            label=UIConstants.MENU_SETTINGS, 
            menu=settings_menu
        )
        
        # Add API Key menu item
        settings_menu.add_command(
            label=UIConstants.MENU_API_KEY,
            command=self._on_api_key_config
        )
    
    def _on_api_key_config(self):
        """Handle API key configuration menu selection."""
        dialog = ApiKeyDialog(self.root, self.app.get_api_key())
        api_key = dialog.show()
        
        if api_key is not None:
            try:
                self.app.update_api_key(api_key)
                self.status_label.set_status(
                    UIConstants.API_KEY_SUCCESS_MESSAGE, 
                    UIConstants.STATUS_COLOR_SUCCESS
                )
                
                self.on_api_key_updated()
            except Exception as e:
                self.status_label.set_error(f"Error updating API key: {str(e)}")
