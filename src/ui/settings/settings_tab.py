import tkinter as tk
from tkinter import ttk, messagebox

from ..constants import UIConstants
from .components import (
    CharacterUsageLabel, 
    ServiceSelector, 
    ElevenLabsSettings, 
    GoogleCloudSettings,
    ScrollFrame
)


class SettingsTab:
    """Settings window that coordinates all settings UI components in tab mode."""
    
    def __init__(self, app, parent):
        """Initialize the settings window.
        
        Args:
            app: The Application instance that this window will control
            parent: The parent widget (tab frame)
        """
        self.app = app
        self.root = parent
        
        # Create UI components
        self._create_components()
    
    def _create_components(self):
        """Create and layout all settings UI components."""
        # Create scrollable frame
        self.scroll_frame = ScrollFrame(self.root)
        self.scroll_frame.pack(fill=tk.BOTH, expand=True)
        
        # All components will be added to the scroll_frame's viewPort
        container = self.scroll_frame.viewPort
        
        # TTS Service Selection Section
        service_frame = ttk.Frame(container)
        service_frame.pack(pady=(UIConstants.FRAME_PADDING, 0), padx=UIConstants.FRAME_PADDING, fill=tk.X)
        
        self.service_selector = ServiceSelector(service_frame, self.app, self._on_service_changed)
        
        # Character usage section
        usage_frame = ttk.Frame(container)
        usage_frame.pack(padx=UIConstants.FRAME_PADDING, fill=tk.X)
        
        self.character_usage = CharacterUsageLabel(
            usage_frame, 
            self.app, 
        )
        
        # Settings container frame
        self.settings_container = ttk.Frame(container)
        self.settings_container.pack(pady=10, padx=UIConstants.FRAME_PADDING, fill=tk.BOTH, expand=True)
        
        self.settings_container.grid_rowconfigure(0, weight=1)
        self.settings_container.grid_columnconfigure(0, weight=1)
        
        # Create settings components for each service
        self.elevenlabs_settings = ElevenLabsSettings(self.settings_container, self.app)
        self.google_cloud_settings = GoogleCloudSettings(self.settings_container, self.app)
        
        # Save button at the bottom
        save_frame = ttk.Frame(container)
        save_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.save_button = ttk.Button(
            save_frame,
            text="Save Settings",
            command=self._on_save_settings,
            width=20,
        )
        self.save_button.pack(anchor=tk.CENTER)

        # Show initial service settings
        self._show_settings(self.app.get_selected_service())
    
    def _on_service_changed(self, selected_service):
        """Handle TTS service selection change."""
        self.app.set_selected_service(selected_service)
        self._show_settings(selected_service)
    
    def _show_settings(self, service):
        """Show settings for the selected TTS service."""
        self.elevenlabs_settings.grid_remove()
        self.google_cloud_settings.grid_remove()
        
        self.character_usage.load_character_usage()

        # Show the selected service frame and load its settings
        if service == "ElevenLabs":
            self.elevenlabs_settings.load_settings()
            self.elevenlabs_settings.grid(row=0, column=0, sticky="nsew")
        elif service == "Google Cloud":
            self.google_cloud_settings.load_settings()
            self.google_cloud_settings.grid(row=0, column=0, sticky="nsew")
    
    def _on_save_settings(self):
        """Handle save settings button click."""
        try:
            service = self.app.get_selected_service()
            if service == "ElevenLabs":
                config = self.elevenlabs_settings.get_settings()
                self.app.set_service_config(config)
            elif service == "Google Cloud":
                config = self.google_cloud_settings.get_settings()
                self.app.set_service_config(config)
                        
            self.character_usage.load_character_usage()
            messagebox.showinfo("Success", "Settings saved successfully!")

        except Exception as e:
            # Handle save error
            messagebox.showerror("Error", f"Error saving settings: {str(e)}")
