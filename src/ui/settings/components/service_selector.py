import customtkinter

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
        customtkinter.CTkLabel(self.parent, text="TTS Service:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=customtkinter.W, pady=(0, 5))
        
        self.service_var = customtkinter.StringVar(value=self.app.get_selected_service())
        self.service_dropdown = customtkinter.CTkOptionMenu(
            self.parent,
            variable=self.service_var,
            values=["ElevenLabs", "Google Cloud"],
            command=self._on_selection_changed,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)
        )
        self.service_dropdown.pack(anchor=customtkinter.W, pady=(0, 10))
    
    def _on_selection_changed(self, selected_service):
        """Handle service selection change."""
        self.on_service_changed(selected_service)
    
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


