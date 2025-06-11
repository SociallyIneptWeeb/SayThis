import tkinter as tk
from tkinter import ttk
import pygame
import os


class UI:
    """Tkinter UI for the SayThis application."""
    
    # UI Constants
    DEFAULT_WINDOW_WIDTH = 500
    DEFAULT_WINDOW_HEIGHT = 400
    MIN_WINDOW_WIDTH = 400
    MIN_WINDOW_HEIGHT = 350
    FRAME_PADDING = 20
    DEFAULT_FONT_SIZE = 11
    DEFAULT_FONT_FAMILY = "Arial"
    BUTTON_PADDING = 5
    TEXT_HEIGHT = 4
    TEXT_WIDTH = 50
    TEXT_PADDING = 5
    WINDOW_PADDING_ADJUST = 40  # Used to adjust wraplength on resize
    DEFAULT_WRAP_LENGTH = DEFAULT_WINDOW_WIDTH - WINDOW_PADDING_ADJUST

    def __init__(self, app):
        """Initialize the GUI.
        
        Args:
            app: The Application instance that this GUI will control
        """
        self.app = app

        self.root = tk.Tk()
        self.root.title("SayThis - Text to Speech")
        self.root.geometry(f"{self.DEFAULT_WINDOW_WIDTH}x{self.DEFAULT_WINDOW_HEIGHT}")
        self.root.minsize(self.MIN_WINDOW_WIDTH, self.MIN_WINDOW_HEIGHT)
        self.root.resizable(True, True)
        
        # Initialize pygame mixer for audio playback
        pygame.mixer.init()
        self.current_audio_file = None
        
        self._create_widgets()
        self._center_window()
        
        # Bind resize event to update wrap length
        self.root.bind("<Configure>", self._on_window_resize)
        
    def _create_widgets(self):
        """Create and layout all GUI widgets."""
        # Main frame
        main_frame = ttk.Frame(
            self.root,
            padding=f"{self.FRAME_PADDING} {self.FRAME_PADDING} {self.FRAME_PADDING} {self.FRAME_PADDING}")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Style configuration
        style = ttk.Style()
        style.configure("TLabel", font=(self.DEFAULT_FONT_FAMILY, self.DEFAULT_FONT_SIZE))
        style.configure("TButton", font=(self.DEFAULT_FONT_FAMILY, self.DEFAULT_FONT_SIZE))
        style.configure("TEntry", font=(self.DEFAULT_FONT_FAMILY, self.DEFAULT_FONT_SIZE))
        
        # Message label
        message_label = ttk.Label(main_frame, text="Enter your message:")
        message_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Message input field
        message_frame = ttk.Frame(main_frame)
        message_frame.pack(fill=tk.X, pady=(0, 25))
        
        self.message_text = tk.Text(
            message_frame, 
            height=self.TEXT_HEIGHT,
            width=self.TEXT_WIDTH,
            wrap=tk.WORD,
            font=(self.DEFAULT_FONT_FAMILY, self.DEFAULT_FONT_SIZE),
            padx=self.TEXT_PADDING,
            pady=self.TEXT_PADDING
        )
        self.message_text.pack(fill=tk.X, expand=True, side=tk.LEFT)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(message_frame, command=self.message_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.message_text.config(yscrollcommand=scrollbar.set)
        
        # Set initial focus to the text widget
        self.message_text.focus_set()
        
        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Generate button
        self.generate_button = ttk.Button(
            button_frame, 
            text="Generate Audio", 
            command=self._on_generate
        )
        self.generate_button.pack(side=tk.RIGHT, padx=self.BUTTON_PADDING)
        
        # Clear button
        clear_button = ttk.Button(
            button_frame, 
            text="Clear", 
            command=self._clear_text_input
        )
        clear_button.pack(side=tk.RIGHT, padx=self.BUTTON_PADDING)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(
            main_frame, 
            textvariable=self.status_var,
            foreground="gray",
            wraplength=self.DEFAULT_WRAP_LENGTH,  # Set wrap length slightly less than window width
            justify=tk.LEFT
        )
        self.status_label.pack(anchor=tk.W, pady=(10, 0), fill=tk.X, expand=True)
        
        # Audio playback controls
        audio_frame = ttk.LabelFrame(main_frame, text="Audio Playback", padding=(10, 5))
        audio_frame.pack(fill=tk.X, pady=(15, 0), ipady=5)
        
        # Audio control buttons
        audio_buttons_frame = ttk.Frame(audio_frame)
        audio_buttons_frame.pack(fill=tk.X, expand=True)
        
        # Play button
        self.play_button = ttk.Button(
            audio_buttons_frame,
            text="▶️ Play",
            command=self._play_audio,
            state="disabled"  # Initially disabled until audio is generated
        )
        self.play_button.pack(side=tk.LEFT, padx=self.BUTTON_PADDING)
        
        # Stop button
        self.stop_button = ttk.Button(
            audio_buttons_frame,
            text="⏹️ Stop",
            command=self._stop_audio,
            state="disabled"  # Initially disabled until audio is playing
        )
        self.stop_button.pack(side=tk.LEFT, padx=self.BUTTON_PADDING)
        
        # Audio file label
        self.audio_file_var = tk.StringVar(value="No audio file generated yet")
        audio_file_label = ttk.Label(
            audio_frame,
            textvariable=self.audio_file_var,
            foreground="gray",
            wraplength=self.DEFAULT_WRAP_LENGTH
        )
        audio_file_label.pack(anchor=tk.W, pady=(5, 0), fill=tk.X)

    def _on_generate(self):
        """Handle generate button click."""
        message = self.message_text.get("1.0", "end-1c")  # end-1c removes the trailing newline
        
        if not message.strip():  # Check if message is empty or just whitespace
            self.status_var.set("⚠️ Please enter a message to convert to speech.")
            self.status_label.configure(foreground="orange")
            return
        
        try:
            self.generate_button.configure(state="disabled")
            self.status_var.set("⏳ Generating audio...")
            self.status_label.configure(foreground="blue")
            self.root.update_idletasks()

            output_path = self.app.generate_audio(message)
            
            # Show success message with file path
            self.audio_file_var.set(output_path)
            self.status_var.set(f"✅ Audio generated successfully!")
            self.status_label.configure(foreground="green")
            
            # Enable playback controls
            self.current_audio_file = output_path
            self.play_button.configure(state="normal")
        except RuntimeError as e:
            self.status_var.set(f"❌ Error: {str(e)}")
            self.status_label.configure(foreground="red")
        finally:
            self.generate_button.configure(state="normal")
    
    def _play_audio(self):
        """Play the generated audio file."""
        if self.current_audio_file and os.path.exists(self.current_audio_file):
            try:
                pygame.mixer.music.load(self.current_audio_file)
                pygame.mixer.music.play()
                
                # Update button states
                self.play_button.configure(state="disabled")
                self.stop_button.configure(state="normal")
                self.status_var.set("▶️ Playing audio...")
                self.status_label.configure(foreground="blue")
            except Exception as e:
                self.status_var.set(f"❌ Error playing audio: {str(e)}")
                self.status_label.configure(foreground="red")
        else:
            self.status_var.set("⚠️ No audio file found to play.")
            self.status_label.configure(foreground="orange")
    
    def _stop_audio(self):
        """Stop the audio playback."""
        pygame.mixer.music.stop()
        
        # Update button states
        self.play_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_var.set("⏹️ Audio stopped.")
        self.status_label.configure(foreground="gray")
    
    def _center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def _on_window_resize(self, event):
        """Handle window resize event to update status label wrap length.
        
        Args:
            event: The Configure event triggered by window resize
        """
        # Only process if the event is from the main window
        if event.widget == self.root:
            # Update wrap length to be slightly less than the window width
            new_width = event.width - self.WINDOW_PADDING_ADJUST  # Subtract padding
            self.status_label.configure(wraplength=new_width)
    
    def _clear_text_input(self):
        """Clear the text input field."""
        self.message_text.delete("1.0", tk.END)
        self.message_text.focus_set()
    
    def run(self):
        """Start the GUI main loop."""
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)  # Handle window close
        self.root.mainloop()
        
    def _on_close(self):
        """Clean up resources and close the application."""
        # Stop any playing audio
        if pygame.mixer.get_init() and pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
        pygame.mixer.quit()
        
        # Destroy the window
        self.root.destroy()
