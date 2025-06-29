import tkinter as tk
from tkinter import ttk

from .constants import UIConstants


class SettingsWindow:
    """Settings window that coordinates all settings UI components in tab mode."""
    
    def __init__(self, app, parent, on_api_key_updated=None):
        """Initialize the settings window.
        
        Args:
            app: The Application instance that this window will control
            parent: The parent widget (tab frame)
            on_api_key_updated: Callback function to call when API key is updated
        """
        self.app = app
        self.root = parent
        self.on_api_key_updated = on_api_key_updated
        
        # Create UI components
        self._create_components()
    
    def _create_components(self):
        """Create and layout all settings UI components."""
        # TTS Service Selection Section
        service_frame = ttk.Frame(self.root)
        service_frame.pack(pady=UIConstants.FRAME_PADDING, padx=UIConstants.FRAME_PADDING, fill=tk.X)
        
        # Service selection label and dropdown
        ttk.Label(service_frame, text="TTS Service:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        self.service_var = tk.StringVar(value="ElevenLabs")
        self.service_dropdown = ttk.Combobox(
            service_frame,
            textvariable=self.service_var,
            values=["ElevenLabs", "IBM Watson"],
            state="readonly",
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)
        )
        self.service_dropdown.pack(anchor=tk.W, pady=(0, 10))
        self.service_dropdown.bind("<<ComboboxSelected>>", self._on_service_changed)
        
        # Settings container frame
        self.settings_container = ttk.Frame(self.root)
        self.settings_container.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Create settings for each service
        self._create_elevenlabs_settings()
        self._create_ibm_watson_settings()
        
        # Show initial service settings
        self._show_service_settings("ElevenLabs")
        
        # Save button at the bottom
        save_frame = ttk.Frame(self.root)
        save_frame.pack(pady=20, padx=20, fill=tk.X)
        
        save_button = ttk.Button(
            save_frame,
            text="Save Settings",
            command=self._on_save_settings
        )
        save_button.pack(anchor=tk.CENTER)
    
    def _create_elevenlabs_settings(self):
        """Create ElevenLabs specific settings."""
        self.elevenlabs_frame = ttk.Frame(self.settings_container)
        
        # API Key Configuration Section
        api_frame = ttk.Frame(self.elevenlabs_frame)
        api_frame.pack(pady=10, fill=tk.X)
        
        # API Key label and entry
        ttk.Label(api_frame, text="ElevenLabs API Key:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        # API Key entry field
        self.api_key_var = tk.StringVar(value=self.app.get_api_key())
        self.api_key_entry = ttk.Entry(
            api_frame,
            textvariable=self.api_key_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            show=UIConstants.API_KEY_ENTRY_SHOW_CHAR,
            width=40
        )
        self.api_key_entry.pack(anchor=tk.W, pady=(0, 10))
    
    def _create_ibm_watson_settings(self):
        """Create IBM Watson specific settings."""
        self.ibm_frame = ttk.Frame(self.settings_container)
        
        # API Key Configuration Section
        api_frame = ttk.Frame(self.ibm_frame)
        api_frame.pack(pady=10, fill=tk.X)
        
        ttk.Label(api_frame, text="IBM Watson API Key:", 
                  font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE)).pack(anchor=tk.W, pady=(0, 5))
        
        self.ibm_api_key_var = tk.StringVar()
        ibm_api_entry = ttk.Entry(
            api_frame,
            textvariable=self.ibm_api_key_var,
            font=(UIConstants.DEFAULT_FONT_FAMILY, UIConstants.DEFAULT_FONT_SIZE),
            show="*",
            width=40
        )
        ibm_api_entry.pack(anchor=tk.W, pady=(0, 10))
    
    def _on_service_changed(self, event=None):
        """Handle TTS service selection change."""
        selected_service = self.service_var.get()
        self._show_service_settings(selected_service)
    
    def _show_service_settings(self, service):
        """Show settings for the selected TTS service."""
        # Hide all service frames
        self.elevenlabs_frame.pack_forget()
        self.ibm_frame.pack_forget()
        
        # Show the selected service frame
        if service == "ElevenLabs":
            self.elevenlabs_frame.pack(fill=tk.BOTH, expand=True)
        elif service == "IBM Watson":
            self.ibm_frame.pack(fill=tk.BOTH, expand=True)
    
    def _on_save_settings(self):
        """Handle save settings button click."""
        # TODO: Implement settings save functionality
        pass
