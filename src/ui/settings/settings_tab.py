import tkinter as tk
from tkinter import ttk, messagebox

from ..constants import UIConstants
from .components import (
    CharacterUsageLabel, 
    ServiceSelector, 
    ElevenLabsSettings, 
    IBMWatsonSettings
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
        # Create main canvas and scrollbar for scrollable content
        main_canvas = tk.Canvas(self.root)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=main_canvas.yview)
        self.scrollable_frame = ttk.Frame(main_canvas)
        
        # Configure scrolling
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: main_canvas.configure(scrollregion=main_canvas.bbox("all"))
        )
        
        canvas_frame = main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        main_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Bind canvas width to frame width
        def configure_canvas_width(event):
            canvas_width = event.width
            main_canvas.itemconfig(canvas_frame, width=canvas_width)
        
        main_canvas.bind('<Configure>', configure_canvas_width)
        
        # Enable mouse wheel scrolling
        def on_mousewheel(event):
            # Handle different platforms and event types
            if event.delta:
                # Windows
                main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            elif event.num == 4:
                # Linux - scroll up
                main_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                # Linux - scroll down
                main_canvas.yview_scroll(1, "units")
        
        # Bind mouse wheel to canvas and all child widgets
        def bind_mousewheel(widget):
            # Windows mouse wheel
            widget.bind("<MouseWheel>", on_mousewheel)
            # Linux mouse wheel
            widget.bind("<Button-4>", on_mousewheel)
            widget.bind("<Button-5>", on_mousewheel)
            
            # Recursively bind to all children
            for child in widget.winfo_children():
                bind_mousewheel(child)
        
        # Bind mouse wheel events
        main_canvas.bind("<MouseWheel>", on_mousewheel)
        self.scrollable_frame.bind("<MouseWheel>", on_mousewheel)
        
        # Make canvas focusable and bind enter/leave events
        main_canvas.bind("<Enter>", lambda e: main_canvas.focus_set())
        
        # Pack canvas and scrollbar
        main_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # TTS Service Selection Section
        service_frame = ttk.Frame(self.scrollable_frame)
        service_frame.pack(pady=(UIConstants.FRAME_PADDING, 0), padx=UIConstants.FRAME_PADDING, fill=tk.X)
        
        self.service_selector = ServiceSelector(service_frame, self.app, self._on_service_changed)
        
        # Character usage section
        usage_frame = ttk.Frame(self.scrollable_frame)
        usage_frame.pack(padx=UIConstants.FRAME_PADDING, fill=tk.X)
        
        self.character_usage = CharacterUsageLabel(
            usage_frame, 
            self.app, 
        )
        
        # Settings container frame
        self.settings_container = ttk.Frame(self.scrollable_frame)
        self.settings_container.pack(pady=10, padx=UIConstants.FRAME_PADDING, fill=tk.BOTH, expand=True)
        
        # Create settings components for each service
        self.elevenlabs_settings = ElevenLabsSettings(self.settings_container, self.app)
        self.ibm_watson_settings = IBMWatsonSettings(self.settings_container, self.app)
        
        # Save button at the bottom
        save_frame = ttk.Frame(self.scrollable_frame)
        save_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.save_button = ttk.Button(
            save_frame,
            text="Save Settings",
            command=self._on_save_settings,
            width=20,
        )
        self.save_button.pack(anchor=tk.CENTER)

        # Bind mouse wheel to all child widgets after creation
        bind_mousewheel(self.scrollable_frame)

        # Show initial service settings
        self._show_settings(self.app.get_selected_service())
    
    def _on_service_changed(self, selected_service):
        """Handle TTS service selection change."""
        self.app.set_selected_service(selected_service)
        self._show_settings(selected_service)
    
    def _show_settings(self, service):
        """Show settings for the selected TTS service."""
        # Hide all service frames
        self.elevenlabs_settings.pack_forget()
        self.ibm_watson_settings.pack_forget()
        
        self.character_usage.load_character_usage()

        # Show the selected service frame and load its settings
        if service == "ElevenLabs":
            self.elevenlabs_settings.load_settings()
            self.elevenlabs_settings.pack(fill=tk.BOTH, expand=True)
        elif service == "IBM Watson":
            self.ibm_watson_settings.load_settings()
            self.ibm_watson_settings.pack(fill=tk.BOTH, expand=True)
    
    def _on_save_settings(self):
        """Handle save settings button click."""
        try:
            service = self.app.get_selected_service()
            if service == "ElevenLabs":
                config = self.elevenlabs_settings.get_settings()
                self.app.set_service_config(config)
            elif service == "IBM Watson":
                config = self.ibm_watson_settings.get_settings()
                self.app.set_service_config(config)
                        
            self.character_usage.load_character_usage()
            messagebox.showinfo("Success", "Settings saved successfully!")

        except Exception as e:
            # Handle save error
            messagebox.showerror("Error", f"Error saving settings: {str(e)}")
