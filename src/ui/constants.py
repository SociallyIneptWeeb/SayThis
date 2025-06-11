class UIConstants:
    """Constants used throughout the UI components."""
    
    # Window dimensions
    DEFAULT_WINDOW_WIDTH = 500
    DEFAULT_WINDOW_HEIGHT = 400
    MIN_WINDOW_WIDTH = 400
    MIN_WINDOW_HEIGHT = 350
    
    # Padding and spacing
    FRAME_PADDING = 20
    BUTTON_PADDING = 5
    TEXT_PADDING = 5
    WINDOW_PADDING_ADJUST = 40  # Used to adjust wraplength on resize
    
    # Font settings
    DEFAULT_FONT_SIZE = 11
    DEFAULT_FONT_FAMILY = "Arial"
    
    # Text widget dimensions
    TEXT_HEIGHT = 4
    TEXT_WIDTH = 50
    
    # Calculated values
    DEFAULT_WRAP_LENGTH = DEFAULT_WINDOW_WIDTH - WINDOW_PADDING_ADJUST
    MIN_WRAP_LENGTH = 100  # Minimum reasonable wrap length
    
    # UI text labels
    WINDOW_TITLE = "SayThis - Text to Speech"
    MESSAGE_LABEL_TEXT = "Enter your message:"
    GENERATE_BUTTON_TEXT = "Generate Audio"
    CLEAR_BUTTON_TEXT = "Clear"
    AUDIO_FRAME_TEXT = "Audio Playback"
    PLAY_BUTTON_TEXT = "▶️ Play"
    STOP_BUTTON_TEXT = "⏹️ Stop"
    
    # Status messages
    STATUS_READY = "Ready"
    STATUS_GENERATING = "⏳ Generating audio..."
    STATUS_SUCCESS = "✅ Audio generated successfully!"
    STATUS_PLAYING = "▶️ Playing audio..."
    STATUS_STOPPED = "⏹️ Audio stopped."
    STATUS_EMPTY_MESSAGE = "⚠️ Please enter a message to convert to speech."
    STATUS_NO_AUDIO_FILE = "⚠️ No audio file found to play."
    STATUS_AUDIO_ERROR = "❌ Error playing audio: {}"
    STATUS_GENERATION_ERROR = "❌ Error: {}"
    
    # Default values
    DEFAULT_AUDIO_FILE_STATUS = "No audio file generated yet"
