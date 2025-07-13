class UIConstants:
    """Constants used throughout the UI components."""
    
    # Window dimensions
    DEFAULT_WINDOW_WIDTH = 500
    DEFAULT_WINDOW_HEIGHT = 400
    MIN_WINDOW_WIDTH = DEFAULT_WINDOW_WIDTH
    MIN_WINDOW_HEIGHT = DEFAULT_WINDOW_HEIGHT
    
    # Padding and spacing
    FRAME_PADDING = 20
    BUTTON_PADDING = TEXT_PADDING = 5
    WINDOW_PADDING_ADJUST = 40  # Used to adjust wrap length on resize
    CORNER_RADIUS = 10
    
    # Font settings
    DEFAULT_FONT_SIZE = 11
    DEFAULT_FONT_FAMILY = "Arial"
    
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
    
    # Character usage labels
    UNSET_USAGE = "--"
    CHARACTER_USAGE_FORMAT = "Used: {} / {} characters"
    CHARACTER_USAGE_NOT_AVAILABLE = "Usage tracking not available for this service"


