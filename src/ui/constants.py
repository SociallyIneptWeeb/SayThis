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
    WINDOW_PADDING_ADJUST = 40  # Used to adjust wrap length on resize
    
    # Font settings
    DEFAULT_FONT_SIZE = 11
    DEFAULT_FONT_FAMILY = "Arial"
    
    # Text widget dimensions
    TEXT_HEIGHT = 4
    TEXT_WIDTH = 50
    
    # Calculated values
    DEFAULT_WRAP_LENGTH = DEFAULT_WINDOW_WIDTH - WINDOW_PADDING_ADJUST

    # Colors
    STATUS_COLOR_READY = "gray"
    STATUS_COLOR_PROCESSING = "blue"
    STATUS_COLOR_SUCCESS = "green"
    STATUS_COLOR_ERROR = "red"
    STATUS_COLOR_WARNING = "orange"
    
    # Button states
    STATE_DISABLED = "disabled"
    STATE_NORMAL = "normal"
    
    # Audio playback settings
    AUDIO_MONITOR_INTERVAL_MS = 100  # Interval for checking audio playback status
    
    # UI text labels
    WINDOW_TITLE = "SayThis - Text to Speech"
    MESSAGE_LABEL_TEXT = "Enter your message:"
    GENERATE_BUTTON_TEXT = "Generate Audio"
    CLEAR_BUTTON_TEXT = "Clear"
    AUDIO_FRAME_TEXT = "Audio Playback"
    PLAY_BUTTON_TEXT = "▶️ Play"
    STOP_BUTTON_TEXT = "⏹️ Stop"
    DOWNLOAD_BUTTON_TEXT = "📥 Download"
    
    # Status messages
    STATUS_READY = "Ready"
    STATUS_GENERATING = "⏳ Generating audio..."
    STATUS_GENERATE_SUCCESS = "✅ Audio generated successfully!"
    STATUS_PLAYING = "▶️ Playing audio..."
    STATUS_STOPPED = "⏹️ Audio stopped."
    STATUS_EMPTY_MESSAGE = "⚠️ Please enter a message to convert to speech."
    STATUS_NO_AUDIO_FILE = "⚠️ No audio file found to play."
    STATUS_ERROR = "❌ {}"
    STATUS_DOWNLOAD_SUCCESS = "📥 Audio file downloaded successfully!"
    STATUS_DOWNLOAD_CANCELLED = "Download cancelled."
    
    # Character usage labels
    UNSET_USAGE = "--"
    CHARACTER_USAGE_FORMAT = "Used: {} / {} characters"

    # Default values
    DEFAULT_AUDIO_FILE_STATUS = "No audio file generated yet"

    # Dialog dimensions
    API_KEY_DIALOG_WIDTH = 400
    API_KEY_DIALOG_HEIGHT = 150
    
    # Entry widget settings
    API_KEY_ENTRY_WIDTH = 50
    API_KEY_ENTRY_SHOW_CHAR = "*"
    
    # Menu bar text
    MENU_SETTINGS = "Settings"
    MENU_API_KEY = "API Key..."
    API_KEY_DIALOG_TITLE = "Configure API Key"
    API_KEY_DIALOG_LABEL = "Enter your ElevenLabs API Key:"
    API_KEY_SUCCESS_MESSAGE = "✅ API key updated successfully!"
    API_KEY_REQUIRED_MESSAGE = "⚠️ Please configure an API key through Settings > API Key to generate audio."
