import tkinter as tk
from tkinter import ttk
from ...constants import UIConstants


class ServiceSelector:
    """Component for selecting the TTS service."""
    
    def __init__(self, parent, app, on_service_changed):
        """Initialize the service selector component.
        
        Args:
            parent: The parent widget to contain this component
            app: The Application instance
            on_service_changed: Callback function when service changes
        """
        self.parent = parent
        self.app = app
        self.on_service_changed = on_service_changed
        self._create_widgets()
    
    def _create_widgets(self):
        """Create the service selector widgets."""
        # Service selection label and dropdown
        ttk.Label(self.parent, text="TTS Service:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        self.service_var = tk.StringVar(value=self.app.get_selected_service())
        self.service_dropdown = ttk.Combobox(
            self.parent,
            textvariable=self.service_var,
            values=["ElevenLabs", "IBM Watson"],
            state="readonly",
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)
        )
        self.service_dropdown.pack(anchor=tk.W, pady=(0, 10))
        self.service_dropdown.bind("<<ComboboxSelected>>", self._on_selection_changed)
    
    def _on_selection_changed(self, event=None):
        """Handle service selection change."""
        self.on_service_changed(self.service_var.get())
    
    def get_selected_service(self):
        """Get the currently selected service.
        
        Returns:
            str: The selected service name
        """
        return self.service_var.get()
    
    def set_selected_service(self, service):
        """Set the selected service.
        
        Args:
            service (str): The service name to select
        """
        self.service_var.set(service)
