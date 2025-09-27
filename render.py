import numpy as np
import cv2
from dataclasses import dataclass
from typing import List, Tuple, Optional, Dict
import skia
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.token import Token
import time
import gc  # For garbage collection
import platform

# Theme definitions
THEMES = {
    "monokai": {
        "background": 0xFF272822,
        "text": 0xFFF8F8F2,
        "cursor": 0xFFF8F8F2,
        "colors": {
            Token.Keyword: 0xFFF92672,                  # Pink
            Token.Keyword.Namespace: 0xFF66D9EF,        # Cyan
            Token.Name.Function: 0xFFA6E22E,            # Green
            Token.Name.Class: 0xFFA6E22E,               # Green
            Token.Name.Decorator: 0xFFA6E22E,           # Green
            Token.String: 0xFFE6DB74,                   # Yellow
            Token.String.Doc: 0xFF75715E,               # Gray (docstrings)
            Token.Literal.String: 0xFFE6DB74,           # Yellow
            Token.Literal.String.Double: 0xFFE6DB74,    # Yellow
            Token.Literal.String.Single: 0xFFE6DB74,    # Yellow
            Token.Literal.String.Affix: 0xFFE6DB74,     # Yellow (f-strings)
            Token.Literal.String.Interpol: 0xFFAE81FF,  # Purple (f-string brackets)
            Token.Number: 0xFFAE81FF,                   # Purple
            Token.Literal.Number: 0xFFAE81FF,           # Purple
            Token.Literal.Number.Integer: 0xFFAE81FF,   # Purple
            Token.Literal.Number.Float: 0xFFAE81FF,     # Purple
            Token.Comment: 0xFF75715E,                  # Gray
            Token.Comment.Single: 0xFF75715E,           # Gray
            Token.Comment.Multiline: 0xFF75715E,        # Gray
            Token.Operator: 0xFFF92672,                 # Pink
            Token.Operator.Word: 0xFFF92672,            # Pink (and, or, not)
            Token.Punctuation: 0xFFF8F8F2,              # White
            Token.Name: 0xFFF8F8F2,                     # White
            Token.Name.Variable: 0xFFF8F8F2,            # White
            Token.Name.Builtin: 0xFF66D9EF,             # Cyan
            Token.Name.Builtin.Pseudo: 0xFF66D9EF,      # Cyan (self, cls)
            Token.Name.Exception: 0xFFA6E22E,           # Green
            Token.Literal: 0xFFAE81FF,                  # Purple
            Token.Text: 0xFFF8F8F2,                     # White
            Token.Text.Whitespace: 0xFFF8F8F2,          # White (invisible)
        }
    },
    "dracula": {
        "background": 0xFF282A36,
        "text": 0xFFF8F8F2,
        "cursor": 0xFFF8F8F2,
        "colors": {
            Token.Keyword: 0xFFFF79C6,                  # Pink
            Token.Keyword.Namespace: 0xFF8BE9FD,        # Cyan
            Token.Name.Function: 0xFF50FA7B,            # Green
            Token.Name.Class: 0xFF50FA7B,               # Green
            Token.Name.Decorator: 0xFF50FA7B,           # Green
            Token.String: 0xFFF1FA8C,                   # Yellow
            Token.String.Doc: 0xFF6272A4,               # Comment
            Token.Literal.String: 0xFFF1FA8C,           # Yellow
            Token.Literal.String.Double: 0xFFF1FA8C,    # Yellow
            Token.Literal.String.Single: 0xFFF1FA8C,    # Yellow
            Token.Literal.String.Affix: 0xFFF1FA8C,     # Yellow
            Token.Literal.String.Interpol: 0xFFBD93F9,  # Purple
            Token.Number: 0xFFBD93F9,                   # Purple
            Token.Literal.Number: 0xFFBD93F9,           # Purple
            Token.Literal.Number.Integer: 0xFFBD93F9,   # Purple
            Token.Literal.Number.Float: 0xFFBD93F9,     # Purple
            Token.Comment: 0xFF6272A4,                  # Gray
            Token.Comment.Single: 0xFF6272A4,           # Gray
            Token.Comment.Multiline: 0xFF6272A4,        # Gray
            Token.Operator: 0xFFFF79C6,                 # Pink
            Token.Operator.Word: 0xFFFF79C6,            # Pink
            Token.Punctuation: 0xFFF8F8F2,              # White
            Token.Name: 0xFFF8F8F2,                     # White
            Token.Name.Variable: 0xFFF8F8F2,            # White
            Token.Name.Builtin: 0xFF8BE9FD,             # Cyan
            Token.Name.Builtin.Pseudo: 0xFF8BE9FD,      # Cyan
            Token.Name.Exception: 0xFF50FA7B,           # Green
            Token.Literal: 0xFFBD93F9,                  # Purple
            Token.Text: 0xFFF8F8F2,                     # White
            Token.Text.Whitespace: 0xFFF8F8F2,          # White
        }
    },
    "github_dark": {
        "background": 0xFF0D1117,
        "text": 0xFFC9D1D9,
        "cursor": 0xFFC9D1D9,
        "colors": {
            Token.Keyword: 0xFFFF7B72,                  # Red
            Token.Keyword.Namespace: 0xFF79C0FF,        # Blue
            Token.Name.Function: 0xFFD2A8FF,            # Purple
            Token.Name.Class: 0xFFD2A8FF,               # Purple
            Token.Name.Decorator: 0xFFD2A8FF,           # Purple
            Token.String: 0xFFA5D6FF,                   # Light Blue
            Token.String.Doc: 0xFF8B949E,               # Gray
            Token.Literal.String: 0xFFA5D6FF,           # Light Blue
            Token.Literal.String.Double: 0xFFA5D6FF,    # Light Blue
            Token.Literal.String.Single: 0xFFA5D6FF,    # Light Blue
            Token.Literal.String.Affix: 0xFFA5D6FF,     # Light Blue
            Token.Literal.String.Interpol: 0xFFD2A8FF,  # Purple
            Token.Number: 0xFF79C0FF,                   # Blue
            Token.Literal.Number: 0xFF79C0FF,           # Blue
            Token.Literal.Number.Integer: 0xFF79C0FF,   # Blue
            Token.Literal.Number.Float: 0xFF79C0FF,     # Blue
            Token.Comment: 0xFF8B949E,                  # Gray
            Token.Comment.Single: 0xFF8B949E,           # Gray
            Token.Comment.Multiline: 0xFF8B949E,        # Gray
            Token.Operator: 0xFFFF7B72,                 # Red
            Token.Operator.Word: 0xFFFF7B72,            # Red
            Token.Punctuation: 0xFFC9D1D9,              # White
            Token.Name: 0xFFC9D1D9,                     # White
            Token.Name.Variable: 0xFFC9D1D9,            # White
            Token.Name.Builtin: 0xFF79C0FF,             # Blue
            Token.Name.Builtin.Pseudo: 0xFF79C0FF,      # Blue
            Token.Name.Exception: 0xFFD2A8FF,           # Purple
            Token.Literal: 0xFF79C0FF,                  # Blue
            Token.Text: 0xFFC9D1D9,                     # White
            Token.Text.Whitespace: 0xFFC9D1D9,          # White
        }
    },
    "vscode_dark": {
        "background": 0xFF1E1E1E,
        "text": 0xFFD4D4D4,
        "cursor": 0xFFD4D4D4,
        "colors": {
            Token.Keyword: 0xFF569CD6,                  # Blue
            Token.Keyword.Namespace: 0xFF4EC9B0,        # Cyan
            Token.Name.Function: 0xFFDCDCAA,            # Light Yellow
            Token.Name.Class: 0xFF4EC9B0,               # Cyan
            Token.Name.Decorator: 0xFFDCDCAA,           # Light Yellow
            Token.String: 0xFFCE9178,                   # Orange
            Token.String.Doc: 0xFF6A9955,               # Green (comments)
            Token.Literal.String: 0xFFCE9178,           # Orange
            Token.Literal.String.Double: 0xFFCE9178,    # Orange
            Token.Literal.String.Single: 0xFFCE9178,    # Orange
            Token.Literal.String.Affix: 0xFFCE9178,     # Orange
            Token.Literal.String.Interpol: 0xFFDCDCAA,  # Light Yellow
            Token.Number: 0xFFB5CEA8,                   # Light Green
            Token.Literal.Number: 0xFFB5CEA8,           # Light Green
            Token.Literal.Number.Integer: 0xFFB5CEA8,   # Light Green
            Token.Literal.Number.Float: 0xFFB5CEA8,     # Light Green
            Token.Comment: 0xFF6A9955,                  # Green
            Token.Comment.Single: 0xFF6A9955,           # Green
            Token.Comment.Multiline: 0xFF6A9955,        # Green
            Token.Operator: 0xFFD4D4D4,                 # White
            Token.Operator.Word: 0xFF569CD6,            # Blue
            Token.Punctuation: 0xFFD4D4D4,              # White
            Token.Name: 0xFF9CDCFE,                     # Light Blue
            Token.Name.Variable: 0xFF9CDCFE,            # Light Blue
            Token.Name.Builtin: 0xFF569CD6,             # Blue
            Token.Name.Builtin.Pseudo: 0xFF569CD6,      # Blue
            Token.Name.Exception: 0xFF4EC9B0,           # Cyan
            Token.Literal: 0xFFB5CEA8,                  # Light Green
            Token.Text: 0xFFD4D4D4,                     # White
            Token.Text.Whitespace: 0xFFD4D4D4,          # White
        }
    },
    "solarized_dark": {
        "background": 0xFF002B36,
        "text": 0xFF839496,
        "cursor": 0xFF839496,
        "colors": {
            Token.Keyword: 0xFF859900,                  # Green
            Token.Keyword.Namespace: 0xFF268BD2,        # Blue
            Token.Name.Function: 0xFF268BD2,            # Blue
            Token.Name.Class: 0xFF268BD2,               # Blue
            Token.Name.Decorator: 0xFF268BD2,           # Blue
            Token.String: 0xFF2AA198,                   # Cyan
            Token.String.Doc: 0xFF586E75,               # Gray
            Token.Literal.String: 0xFF2AA198,           # Cyan
            Token.Literal.String.Double: 0xFF2AA198,    # Cyan
            Token.Literal.String.Single: 0xFF2AA198,    # Cyan
            Token.Literal.String.Affix: 0xFF2AA198,     # Cyan
            Token.Literal.String.Interpol: 0xFFB58900,  # Yellow
            Token.Number: 0xFF2AA198,                   # Cyan
            Token.Literal.Number: 0xFF2AA198,           # Cyan
            Token.Literal.Number.Integer: 0xFF2AA198,   # Cyan
            Token.Literal.Number.Float: 0xFF2AA198,     # Cyan
            Token.Comment: 0xFF586E75,                  # Gray
            Token.Comment.Single: 0xFF586E75,           # Gray
            Token.Comment.Multiline: 0xFF586E75,        # Gray
            Token.Operator: 0xFF859900,                 # Green
            Token.Operator.Word: 0xFF859900,            # Green
            Token.Punctuation: 0xFF839496,              # Base0
            Token.Name: 0xFF93A1A1,                     # Base1
            Token.Name.Variable: 0xFF93A1A1,            # Base1
            Token.Name.Builtin: 0xFFB58900,             # Yellow
            Token.Name.Builtin.Pseudo: 0xFFB58900,      # Yellow
            Token.Name.Exception: 0xFFCB4B16,           # Orange
            Token.Literal: 0xFF2AA198,                  # Cyan
            Token.Text: 0xFF839496,                     # Base0
            Token.Text.Whitespace: 0xFF839496,          # Base0
        }
    },
    "one_dark": {
        "background": 0xFF282C34,
        "text": 0xFFABB2BF,
        "cursor": 0xFF528BFF,
        "colors": {
            Token.Keyword: 0xFFC678DD,                  # Purple
            Token.Keyword.Namespace: 0xFFC678DD,        # Purple
            Token.Name.Function: 0xFF61AFEF,            # Blue
            Token.Name.Class: 0xFFE5C07B,               # Yellow
            Token.Name.Decorator: 0xFF61AFEF,           # Blue
            Token.String: 0xFF98C379,                   # Green
            Token.String.Doc: 0xFF5C6370,               # Gray
            Token.Literal.String: 0xFF98C379,           # Green
            Token.Literal.String.Double: 0xFF98C379,    # Green
            Token.Literal.String.Single: 0xFF98C379,    # Green
            Token.Literal.String.Affix: 0xFF98C379,     # Green
            Token.Literal.String.Interpol: 0xFFE06C75,  # Red
            Token.Number: 0xFFD19A66,                   # Orange
            Token.Literal.Number: 0xFFD19A66,           # Orange
            Token.Literal.Number.Integer: 0xFFD19A66,   # Orange
            Token.Literal.Number.Float: 0xFFD19A66,     # Orange
            Token.Literal.Number.Hex: 0xFFD19A66,       # Orange
            Token.Literal.Number.Bin: 0xFFD19A66,       # Orange
            Token.Comment: 0xFF5C6370,                  # Gray
            Token.Comment.Single: 0xFF5C6370,           # Gray
            Token.Comment.Multiline: 0xFF5C6370,        # Gray
            Token.Operator: 0xFF56B6C2,                 # Cyan
            Token.Operator.Word: 0xFFC678DD,            # Purple
            Token.Punctuation: 0xFFABB2BF,              # Text
            Token.Name: 0xFFE06C75,                     # Red
            Token.Name.Variable: 0xFFE06C75,            # Red
            Token.Name.Builtin: 0xFFE5C07B,             # Yellow
            Token.Name.Builtin.Pseudo: 0xFFE06C75,      # Red (self, cls)
            Token.Name.Exception: 0xFFE5C07B,           # Yellow
            Token.Literal: 0xFFD19A66,                  # Orange
            Token.Text: 0xFFABB2BF,                     # Text
            Token.Text.Whitespace: 0xFFABB2BF,          # Text
        }
    },
    "nord": {
        "background": 0xFF2E3440,
        "text": 0xFFD8DEE9,
        "cursor": 0xFF88C0D0,
        "colors": {
            Token.Keyword: 0xFF81A1C1,                  # Nord9 - Blue
            Token.Keyword.Namespace: 0xFF81A1C1,        # Blue
            Token.Name.Function: 0xFF88C0D0,            # Nord8 - Cyan
            Token.Name.Class: 0xFF8FBCBB,               # Nord7 - Teal
            Token.Name.Decorator: 0xFF5E81AC,           # Nord10 - Deep Blue
            Token.String: 0xFFA3BE8C,                   # Nord14 - Green
            Token.String.Doc: 0xFF616E88,               # Nord3 - Gray
            Token.Literal.String: 0xFFA3BE8C,           # Green
            Token.Literal.String.Double: 0xFFA3BE8C,    # Green
            Token.Literal.String.Single: 0xFFA3BE8C,    # Green
            Token.Literal.String.Affix: 0xFFA3BE8C,     # Green
            Token.Literal.String.Interpol: 0xFFEBCB8B,  # Nord13 - Yellow
            Token.Number: 0xFFB48EAD,                   # Nord15 - Purple
            Token.Literal.Number: 0xFFB48EAD,           # Purple
            Token.Literal.Number.Integer: 0xFFB48EAD,   # Purple
            Token.Literal.Number.Float: 0xFFB48EAD,     # Purple
            Token.Literal.Number.Hex: 0xFFB48EAD,       # Purple
            Token.Literal.Number.Bin: 0xFFB48EAD,       # Purple
            Token.Comment: 0xFF616E88,                  # Nord3 - Gray
            Token.Comment.Single: 0xFF616E88,           # Gray
            Token.Comment.Multiline: 0xFF616E88,        # Gray
            Token.Operator: 0xFF81A1C1,                 # Nord9 - Blue
            Token.Operator.Word: 0xFF81A1C1,            # Blue
            Token.Punctuation: 0xFFECEFF4,              # Nord6 - White
            Token.Name: 0xFFD8DEE9,                     # Nord4 - Light
            Token.Name.Variable: 0xFFD8DEE9,            # Light
            Token.Name.Builtin: 0xFF81A1C1,             # Nord9 - Blue
            Token.Name.Builtin.Pseudo: 0xFFBF616A,      # Nord11 - Red (self, cls)
            Token.Name.Exception: 0xFFD08770,           # Nord12 - Orange
            Token.Literal: 0xFFB48EAD,                  # Purple
            Token.Text: 0xFFD8DEE9,                     # Light
            Token.Text.Whitespace: 0xFFD8DEE9,          # Light
        }
    },
    "gruvbox_dark": {
        "background": 0xFF282828,
        "text": 0xFFEBDBB2,
        "cursor": 0xFFFE8019,
        "colors": {
            Token.Keyword: 0xFFFB4934,                  # Red
            Token.Keyword.Namespace: 0xFFFE8019,        # Orange
            Token.Name.Function: 0xFFB8BB26,            # Green
            Token.Name.Class: 0xFFFABD2F,               # Yellow
            Token.Name.Decorator: 0xFF83A598,           # Aqua
            Token.String: 0xFFB8BB26,                   # Green
            Token.String.Doc: 0xFF928374,               # Gray
            Token.Literal.String: 0xFFB8BB26,           # Green
            Token.Literal.String.Double: 0xFFB8BB26,    # Green
            Token.Literal.String.Single: 0xFFB8BB26,    # Green
            Token.Literal.String.Affix: 0xFFB8BB26,     # Green
            Token.Literal.String.Interpol: 0xFFFE8019,  # Orange
            Token.Number: 0xFFD3869B,                   # Purple
            Token.Literal.Number: 0xFFD3869B,           # Purple
            Token.Literal.Number.Integer: 0xFFD3869B,   # Purple
            Token.Literal.Number.Float: 0xFFD3869B,     # Purple
            Token.Literal.Number.Hex: 0xFFD3869B,       # Purple
            Token.Literal.Number.Bin: 0xFFD3869B,       # Purple
            Token.Comment: 0xFF928374,                  # Gray
            Token.Comment.Single: 0xFF928374,           # Gray
            Token.Comment.Multiline: 0xFF928374,        # Gray
            Token.Operator: 0xFF8EC07C,                 # Aqua
            Token.Operator.Word: 0xFFFB4934,            # Red
            Token.Punctuation: 0xFFA89984,              # Light Gray
            Token.Name: 0xFFEBDBB2,                     # Fg
            Token.Name.Variable: 0xFF83A598,            # Aqua
            Token.Name.Builtin: 0xFFFE8019,             # Orange
            Token.Name.Builtin.Pseudo: 0xFFFE8019,      # Orange (self, cls)
            Token.Name.Exception: 0xFFFB4934,           # Red
            Token.Literal: 0xFFD3869B,                  # Purple
            Token.Text: 0xFFEBDBB2,                     # Fg
            Token.Text.Whitespace: 0xFFEBDBB2,          # Fg
        }
    },
    "tokyo_night": {
        "background": 0xFF1A1B26,
        "text": 0xFFA9B1D6,
        "cursor": 0xFF7AA2F7,
        "colors": {
            Token.Keyword: 0xFF9D7CD8,                  # Purple
            Token.Keyword.Namespace: 0xFF9D7CD8,        # Purple
            Token.Name.Function: 0xFF7AA2F7,            # Blue
            Token.Name.Class: 0xFFFF9E64,               # Orange
            Token.Name.Decorator: 0xFF7DCFFF,           # Cyan
            Token.String: 0xFF9ECE6A,                   # Green
            Token.String.Doc: 0xFF565F89,               # Comment
            Token.Literal.String: 0xFF9ECE6A,           # Green
            Token.Literal.String.Double: 0xFF9ECE6A,    # Green
            Token.Literal.String.Single: 0xFF9ECE6A,    # Green
            Token.Literal.String.Affix: 0xFF9ECE6A,     # Green
            Token.Literal.String.Interpol: 0xFFF7768E,  # Red
            Token.Number: 0xFFFF9E64,                   # Orange
            Token.Literal.Number: 0xFFFF9E64,           # Orange
            Token.Literal.Number.Integer: 0xFFFF9E64,   # Orange
            Token.Literal.Number.Float: 0xFFFF9E64,     # Orange
            Token.Literal.Number.Hex: 0xFFFF9E64,       # Orange
            Token.Literal.Number.Bin: 0xFFFF9E64,       # Orange
            Token.Comment: 0xFF565F89,                  # Comment
            Token.Comment.Single: 0xFF565F89,           # Comment
            Token.Comment.Multiline: 0xFF565F89,        # Comment
            Token.Operator: 0xFF89DDFF,                 # Light Blue
            Token.Operator.Word: 0xFF9D7CD8,            # Purple
            Token.Punctuation: 0xFF89DDFF,              # Light Blue
            Token.Name: 0xFFC0CAF5,                     # Light Purple
            Token.Name.Variable: 0xFFC0CAF5,            # Light Purple
            Token.Name.Builtin: 0xFFE0AF68,             # Yellow
            Token.Name.Builtin.Pseudo: 0xFFF7768E,      # Red (self, cls)
            Token.Name.Exception: 0xFFF7768E,           # Red
            Token.Literal: 0xFFFF9E64,                  # Orange
            Token.Text: 0xFFA9B1D6,                     # Text
            Token.Text.Whitespace: 0xFFA9B1D6,          # Text
        }
    },
    "material_ocean": {
        "background": 0xFF0F111A,
        "text": 0xFF8F93A2,
        "cursor": 0xFF82AAFF,
        "colors": {
            Token.Keyword: 0xFFC792EA,                  # Purple
            Token.Keyword.Namespace: 0xFFC792EA,        # Purple
            Token.Name.Function: 0xFF82AAFF,            # Blue
            Token.Name.Class: 0xFFFFCB6B,               # Yellow
            Token.Name.Decorator: 0xFF82AAFF,           # Blue
            Token.String: 0xFFC3E88D,                   # Green
            Token.String.Doc: 0xFF464B5D,               # Gray
            Token.Literal.String: 0xFFC3E88D,           # Green
            Token.Literal.String.Double: 0xFFC3E88D,    # Green
            Token.Literal.String.Single: 0xFFC3E88D,    # Green
            Token.Literal.String.Affix: 0xFFC3E88D,     # Green
            Token.Literal.String.Interpol: 0xFFF78C6C,  # Orange
            Token.Number: 0xFFF78C6C,                   # Orange
            Token.Literal.Number: 0xFFF78C6C,           # Orange
            Token.Literal.Number.Integer: 0xFFF78C6C,   # Orange
            Token.Literal.Number.Float: 0xFFF78C6C,     # Orange
            Token.Literal.Number.Hex: 0xFFF78C6C,       # Orange
            Token.Literal.Number.Bin: 0xFFF78C6C,       # Orange
            Token.Comment: 0xFF464B5D,                  # Gray
            Token.Comment.Single: 0xFF464B5D,           # Gray
            Token.Comment.Multiline: 0xFF464B5D,        # Gray
            Token.Operator: 0xFF89DDFF,                 # Cyan
            Token.Operator.Word: 0xFFC792EA,            # Purple
            Token.Punctuation: 0xFF89DDFF,              # Cyan
            Token.Name: 0xFFB2CCD6,                     # Light Blue
            Token.Name.Variable: 0xFFB2CCD6,            # Light Blue
            Token.Name.Builtin: 0xFFFFCB6B,             # Yellow
            Token.Name.Builtin.Pseudo: 0xFFF07178,      # Red (self, cls)
            Token.Name.Exception: 0xFFF07178,           # Red
            Token.Literal: 0xFFF78C6C,                  # Orange
            Token.Text: 0xFF8F93A2,                     # Text
            Token.Text.Whitespace: 0xFF8F93A2,          # Text
        }
    }
}

def calculate_auto_font_size(width: int, height: int) -> int:
    """Calculate appropriate font size based on resolution"""
    # Specific font sizes for common resolutions
    if height >= 2160:  # 4K (3840x2160)
        return 66
    elif height >= 1440:  # 2K/QHD (2560x1440)
        return 33
    elif height >= 1080:  # Full HD (1920x1080)
        return 28
    else:  # HD (1280x720) and below
        return 24

@dataclass
class RenderConfig:
    width: int = 1920
    height: int = 1080
    fps: int = 60
    quality: str = "high"  # low, medium, high, ultra
    font_size: int = None  # None means auto
    font_family: str = "Monaco"
    padding: int = 40
    line_height: float = 1.5
    typing_speed: float = 15.0  # chars per second
    theme: str = "monokai"  # Theme name
    auto_font_size: bool = True  # Enable auto font sizing
    scroll_enabled: bool = True  # Enable automatic scrolling for long code
    show_line_numbers: bool = False  # Show line numbers in the video
    viewport_pixel_snap: bool = True  # Snap positions to pixel boundaries to reduce jitter
    hide_cursor_near_edges: bool = True  # Hide cursor near viewport edges
    downscale_filter: str = "area"  # Downscale filter: "lanczos4" or "area"
    line_wrap: bool = True  # Enable automatic line wrapping for long lines
    wrap_indent: int = 4  # Number of spaces to indent wrapped lines

    @property
    def quality_settings(self):
        presets = {
            "low": {"fps": 30, "antialiasing": False, "motion_blur": False, "bitrate": "2M"},
            "medium": {"fps": 30, "antialiasing": True, "motion_blur": False, "bitrate": "5M"},
            "high": {"fps": 60, "antialiasing": True, "motion_blur": True, "bitrate": "10M"},
            "ultra": {"fps": 60, "antialiasing": True, "motion_blur": True, "bitrate": "20M", "supersampling": 1.25}  # Reduced to 1.25 for better memory usage
        }
        return presets.get(self.quality, presets["high"])

class ModernCodeRenderer:
    def __init__(self, config: RenderConfig):
        self.config = config
        self.settings = config.quality_settings

        # Auto calculate font size if needed
        if config.auto_font_size or config.font_size is None:
            config.font_size = calculate_auto_font_size(config.width, config.height)
            print(f"Auto font size: {config.font_size}px for {config.width}x{config.height}")

        # Supersampling for ultra quality
        self.render_scale = float(self.settings.get("supersampling", 1))
        self.render_width = int(config.width * self.render_scale)
        self.render_height = int(config.height * self.render_scale)

        # Initialize Skia
        self.surface = skia.Surface(self.render_width, self.render_height)
        self.canvas = self.surface.getCanvas()

        # Font setup - Use monospace font for better alignment
        try:
            self.typeface = skia.Typeface('Monaco' if platform.system() == 'Darwin' else 'Consolas')
        except:
            self.typeface = skia.Typeface(config.font_family)

        self.font = skia.Font(self.typeface, config.font_size * self.render_scale)
        self.font.setSubpixel(True)  # Better text rendering
        if self.settings["antialiasing"]:
            self.font.setEdging(skia.Font.Edging.kAntiAlias)

        # Get proper font metrics for accurate line spacing
        self.font_metrics = self.font.getMetrics()
        # Calculate proper line height from font metrics
        # Use ascent + descent + leading for accurate baseline-to-baseline distance
        font_height = abs(self.font_metrics.fAscent) + abs(self.font_metrics.fDescent)
        font_leading = abs(self.font_metrics.fLeading) if self.font_metrics.fLeading else font_height * 0.2

        # Store the actual baseline-to-baseline distance
        self.baseline_distance = (font_height + font_leading) * config.line_height
        self.text_ascent = abs(self.font_metrics.fAscent)

        # Setup emoji font for color emoji support
        try:
            system = platform.system()
            if system == 'Darwin':
                # macOS emoji font
                self.emoji_typeface = skia.Typeface('Apple Color Emoji')
            elif system == 'Windows':
                # Windows emoji font
                self.emoji_typeface = skia.Typeface('Segoe UI Emoji')
            else:
                # Linux emoji font
                self.emoji_typeface = skia.Typeface('Noto Color Emoji')

            self.emoji_font = skia.Font(self.emoji_typeface, config.font_size * self.render_scale)
            self.emoji_font.setSubpixel(True)
            if self.settings["antialiasing"]:
                self.emoji_font.setEdging(skia.Font.Edging.kAntiAlias)
        except:
            # Fallback to regular font if emoji font not available
            self.emoji_typeface = self.typeface
            self.emoji_font = self.font

        # Calculate fixed character width for monospace
        # Use average width of common characters for better spacing
        test_blob = skia.TextBlob('x', self.font)  # Use 'x' as reference character
        self.char_width = test_blob.bounds().width() * 0.5  # Balanced spacing for better readability

        # Paint objects for different token types
        self.paints = self._create_paints()

        # Viewport and scrolling state
        self.viewport_position = 0.0  # Current viewport position (pixels)
        self.viewport_velocity = 0.0  # Current velocity (pixels/frame)

        # Viewport dimensions
        self.visible_lines = int((self.render_height - 2 * config.padding * self.render_scale) /
                                 (config.font_size * config.line_height * self.render_scale))

        # State tracking
        self.current_typing_y = 0.0  # Y position of current typing
        self.scroll_active = False  # Is scrolling currently happening
        self.prev_spacing_compensation = 1.0  # For smooth spacing transitions

    def _create_paints(self):
        """Create Skia Paint objects for syntax highlighting using theme"""
        # Get theme colors
        theme = THEMES.get(self.config.theme, THEMES["monokai"])
        theme_colors = theme["colors"]

        paints = {}

        # Create paint for each token type
        for token_type, color in theme_colors.items():
            paint = skia.Paint()
            paint.setAntiAlias(self.settings["antialiasing"])
            paint.setColor(color)
            paints[token_type] = paint

        # Default paint for unmatched tokens
        default_paint = skia.Paint()
        default_paint.setAntiAlias(self.settings["antialiasing"])
        default_paint.setColor(theme["text"])
        paints[None] = default_paint

        # Store theme for background and cursor colors
        self.theme = theme

        return paints

    def _tokenize_code(self, code: str, language: str):
        """Tokenize code with Pygments"""
        from pygments import lex
        lexer = get_lexer_by_name(language)

        # Get tokens directly from lexer
        tokens = []
        for token_type, text in lex(code, lexer):
            tokens.append((token_type, text))

        return tokens


    def _calculate_smooth_scroll(self, current_y, line_height, frame_num=0):
        """CHUNK-BASED scrolling - moves in fixed steps, no smooth animation"""
        if not self.config.scroll_enabled:
            return self.viewport_position

        # CHUNK SCROLLING CONFIGURATION
        SCROLL_CHUNK_PERCENT = 0.3  # Scroll 30% of screen at once
        TRIGGER_ZONE_PERCENT = 0.25  # Trigger when cursor is in bottom 25% of screen
        MIN_FRAMES_BETWEEN_SCROLLS = 30  # Debounce: ~0.5 sec at 60fps

        # Initialize last scroll frame if not exists
        if not hasattr(self, 'last_scroll_frame'):
            self.last_scroll_frame = -100

        # Calculate chunk size and trigger zone
        scroll_chunk = self.render_height * SCROLL_CHUNK_PERCENT
        trigger_zone = self.render_height * TRIGGER_ZONE_PERCENT

        # Calculate viewport boundaries
        viewport_top = self.viewport_position
        viewport_bottom = viewport_top + self.render_height

        # Calculate trigger line (bottom X% of viewport)
        trigger_line = viewport_bottom - trigger_zone

        # Check if we need to scroll
        if current_y > trigger_line:
            # Check debounce
            frames_since_scroll = frame_num - self.last_scroll_frame

            if frames_since_scroll >= MIN_FRAMES_BETWEEN_SCROLLS:
                # PERFORM CHUNK SCROLL
                # Position cursor at 40% from top after scrolling
                ideal_position = self.render_height * 0.4
                new_position = current_y - ideal_position

                # Snap to line boundaries for perfect alignment
                if self.config.viewport_pixel_snap:
                    new_position = round(new_position / line_height) * line_height

                # Update position INSTANTLY (no animation)
                self.viewport_position = max(0, new_position)
                self.last_scroll_frame = frame_num

                # Reset velocity
                self.viewport_velocity = 0
                self.scroll_active = True
        else:
            # No scroll needed
            self.scroll_active = False

        # Store current typing position
        self.current_typing_y = current_y

        return self.viewport_position

    def _draw_line_number(self, line_num: int, y_pos: float, digits: int):
        """Draw line number on the left side"""
        # Create paint for line numbers (dimmed color)
        line_num_paint = skia.Paint()
        line_num_paint.setAntiAlias(self.settings["antialiasing"])
        # Use a dimmed version of text color
        line_num_paint.setColor(0xFF606060)  # Gray color for line numbers

        # Format line number with proper padding
        line_num_str = str(line_num).rjust(digits)

        # Calculate position
        x_pos = self.config.padding * self.render_scale

        # Draw line number
        self.canvas.drawString(
            line_num_str,
            x_pos,
            y_pos,
            self.font,
            line_num_paint
        )

    def _is_emoji(self, char):
        """Check if character is an emoji"""
        # Basic emoji detection - covers most common emoji ranges
        code_point = ord(char)
        return (
            # Emoticons
            (0x1F600 <= code_point <= 0x1F64F) or
            # Miscellaneous Symbols
            (0x1F300 <= code_point <= 0x1F5FF) or
            # Transport and Map Symbols
            (0x1F680 <= code_point <= 0x1F6FF) or
            # Additional Emoticons
            (0x1F900 <= code_point <= 0x1F9FF) or
            # Supplemental Symbols and Pictographs
            (0x1F1E6 <= code_point <= 0x1F1FF) or
            # Miscellaneous Symbols and Arrows
            (0x2600 <= code_point <= 0x26FF) or
            # Dingbats
            (0x2700 <= code_point <= 0x27BF) or
            # Various other emoji ranges
            code_point in [0x2764, 0x2728, 0x2B50, 0x2B55, 0x2705, 0x2744, 0x2747]
        )

    def _render_frame(self, tokens: List[Tuple], chars_to_show: int, recreate_surface: bool = False, frame_num: int = 0) -> np.ndarray:
        """Render a single frame with Skia"""
        # Optionally recreate surface to prevent memory accumulation
        if recreate_surface:
            self.surface = skia.Surface(self.render_width, self.render_height)
            self.canvas = self.surface.getCanvas()

        # Clear canvas with theme background
        self.canvas.clear(self.theme["background"])

        # Calculate space for line numbers if enabled
        line_number_width = 0
        if self.config.show_line_numbers:
            # Calculate max line number width (e.g., for 100 lines need 3 chars)
            max_lines = len(''.join(text for _, text in tokens).split('\n')) + 1
            line_number_digits = len(str(max_lines))
            line_number_width = (line_number_digits + 2) * self.char_width  # +2 for spacing

        # Initial position (before applying scroll offset)
        initial_x = (self.config.padding * self.render_scale) + line_number_width
        initial_y = self.config.padding * self.render_scale + self.config.font_size * self.render_scale

        # Calculate maximum x position for line wrapping
        max_x = self.render_width - (self.config.padding * self.render_scale)
        max_chars_per_line = int((max_x - initial_x) / self.char_width) if self.config.line_wrap else float('inf')

        x = initial_x
        y = initial_y

        # Use the proper baseline distance calculated from font metrics
        line_height = self.baseline_distance
        current_line_number = 1  # Track current line number

        # Advanced line spacing preservation formula
        # Maintains consistent visual spacing across all typing speeds
        spacing_compensation = 1.0

        # Calculate typing speed factor (normalized 0-1)
        typing_speed_normalized = min(1.0, self.config.typing_speed / 100.0)

        # Dynamic compensation based on multiple factors
        if self.scroll_active and abs(self.viewport_velocity) > 0.1:
            # 1. Velocity-based compensation
            velocity_factor = min(1.0, abs(self.viewport_velocity) / (line_height * 2))

            # 2. Typing speed compensation
            # Faster typing needs more spacing compensation to prevent compression
            speed_compensation = 0.03 + (0.07 * typing_speed_normalized)  # 3-10% range

            # 3. Frame timing compensation
            # Account for render timing differences at different speeds
            timing_factor = 1.0 / (1.0 + self.config.typing_speed * 0.001)

            # 4. Combined formula with weighted factors
            spacing_compensation = 1.0 + (speed_compensation * velocity_factor * timing_factor)

            # 5. Smooth transition for scroll start/stop
            if hasattr(self, 'prev_spacing_compensation'):
                # Smooth transition using exponential moving average
                alpha = 0.3  # Smoothing factor
                spacing_compensation = (alpha * spacing_compensation +
                                       (1 - alpha) * self.prev_spacing_compensation)

        # Store for smooth transitions
        self.prev_spacing_compensation = spacing_compensation

        # Track the actual Y position for scrolling calculation (without scroll offset)
        actual_y = initial_y

        # Cursor tracking - simple and direct
        cursor_x = initial_x
        cursor_y = initial_y
        cursor_visible = False  # Start with cursor not visible

        # Character counting
        total_chars_processed = 0

        # Draw first line number if enabled
        if self.config.show_line_numbers:
            self._draw_line_number(1, initial_y - self.viewport_position, line_number_digits)

        for token_type, text in tokens:
            if total_chars_processed >= chars_to_show:
                break

            # Get paint for this token type
            paint = None

            # First try exact match
            if token_type in self.paints:
                paint = self.paints[token_type]
            else:
                # Try parent token types
                current = token_type
                while paint is None and current != Token:
                    if current in self.paints:
                        paint = self.paints[current]
                        break
                    if hasattr(current, 'parent'):
                        current = current.parent
                    else:
                        break

            # If still no match, use default
            if paint is None:
                paint = self.paints.get(None, self.paints[Token.Text])

            # Calculate how many chars to render from this token
            chars_remaining = chars_to_show - total_chars_processed
            text_to_render = text[:chars_remaining]

            # Handle newlines
            lines = text_to_render.split('\n')

            for i, line in enumerate(lines):
                if i > 0:
                    # Process newline character
                    total_chars_processed += 1

                    # Check if cursor should be at end of previous line
                    if total_chars_processed == chars_to_show:
                        cursor_x = x
                        cursor_y = actual_y
                        # Don't show cursor at beginning of line
                        cursor_visible = x > initial_x

                    x = initial_x

                    # Apply consistent line spacing with advanced compensation
                    # Use baseline-to-baseline distance for proper spacing
                    base_spacing = line_height

                    # Apply compensation with typing speed awareness
                    if self.scroll_active:
                        # Extra compensation for new lines during scrolling
                        # This prevents the "compressed" look when scrolling starts
                        newline_boost = 1.0 + (0.02 * typing_speed_normalized)
                        adjusted_line_height = base_spacing * spacing_compensation * newline_boost
                    else:
                        adjusted_line_height = base_spacing

                    # Ensure minimum spacing to prevent compression
                    # Minimum is higher for faster typing speeds
                    min_spacing_factor = 0.95 + (0.03 * typing_speed_normalized)  # 95-98% minimum
                    min_spacing = self.baseline_distance * min_spacing_factor

                    if adjusted_line_height < min_spacing:
                        adjusted_line_height = min_spacing

                    # Apply maximum limit to prevent excessive spacing
                    max_spacing = self.baseline_distance * 1.15
                    if adjusted_line_height > max_spacing:
                        adjusted_line_height = max_spacing

                    y += adjusted_line_height
                    actual_y += adjusted_line_height
                    current_line_number += 1  # Increment line number

                    # Draw line number for new line if enabled
                    if self.config.show_line_numbers:
                        self._draw_line_number(current_line_number, y - self.viewport_position, line_number_digits)

                # Calculate rendered Y position with scroll offset
                # Apply baseline adjustment for proper text positioning
                baseline_y = y  # This is the baseline position
                # AGGRESSIVE pixel snapping
                if self.config.viewport_pixel_snap:
                    # Round both values independently for maximum stability
                    rendered_y = round(baseline_y) - round(self.viewport_position)
                else:
                    rendered_y = baseline_y - self.viewport_position

                # Render the line character by character
                if line:
                    # Replace tabs with spaces
                    line = line.replace('\t', '    ')

                    # Track original indentation for wrapped lines
                    original_indent = len(line) - len(line.lstrip())
                    wrap_indent_x = initial_x + (original_indent + self.config.wrap_indent) * self.char_width

                    for char_idx, char in enumerate(line):
                        # Check if we've rendered all characters we need
                        if total_chars_processed >= chars_to_show:
                            break

                        # Check if we need to wrap
                        if self.config.line_wrap and x + self.char_width > max_x:
                            # Wrap to next line
                            x = wrap_indent_x
                            y += line_height
                            actual_y += line_height

                            # Update rendered_y for new line
                            baseline_y = y
                            if self.config.viewport_pixel_snap:
                                rendered_y = round(baseline_y) - round(self.viewport_position)
                            else:
                                rendered_y = baseline_y - self.viewport_position

                        # Render character if in viewport
                        if rendered_y >= -line_height and rendered_y <= self.render_height:
                            # Shadow effect for high/ultra quality
                            if self.config.quality in ["high", "ultra"] and char != ' ':
                                shadow_paint = skia.Paint(paint)
                                shadow_paint.setColor(0x40000000)
                                shadow_font = self.emoji_font if self._is_emoji(char) else self.font
                                self.canvas.drawString(char, x + 2, rendered_y + 2, shadow_font, shadow_paint)

                            # Main text
                            if char != ' ':
                                if self._is_emoji(char):
                                    self.canvas.drawString(char, x, rendered_y, self.emoji_font, paint)
                                else:
                                    self.canvas.drawString(char, x, rendered_y, self.font, paint)

                        # Move to next character position
                        x += self.char_width
                        total_chars_processed += 1

                        # Update cursor position if this is the last character to show
                        if total_chars_processed == chars_to_show:
                            cursor_x = x
                            cursor_y = actual_y
                            # Check if we're not on whitespace/tabs or at line start
                            current_char = char if char_idx < len(line) else ''
                            is_whitespace = current_char in [' ', '\t']
                            is_line_start = (x - initial_x) < self.char_width
                            # Hide cursor at line start or on whitespace
                            cursor_visible = not is_whitespace and not is_line_start
                            # Apply smooth scrolling
                            self.current_typing_y = cursor_y
                            self._calculate_smooth_scroll(cursor_y, line_height, frame_num)

                else:
                    # Empty line - just track it
                    pass

            # If we've processed all characters for this token, stop
            if total_chars_processed >= chars_to_show:
                break

        # Add cursor (always visible when typing)
        if cursor_visible:
            # Blinking effect only for high/ultra quality
            if self.config.quality in ["high", "ultra"]:
                cursor_alpha = int(128 + 127 * np.sin(time.time() * 3))
            else:
                cursor_alpha = 255  # Solid cursor for lower quality

            cursor_paint = skia.Paint()
            # Use theme cursor color with alpha
            cursor_base_color = self.theme["cursor"] & 0x00FFFFFF
            cursor_paint.setColor((cursor_alpha << 24) | cursor_base_color)
            cursor_paint.setStyle(skia.Paint.kFill_Style)

            # Apply scroll offset to cursor position
            if self.config.viewport_pixel_snap:
                rendered_cursor_y = round(cursor_y - self.viewport_position)
            else:
                rendered_cursor_y = cursor_y - self.viewport_position

            # Draw cursor if it's within the viewport
            if rendered_cursor_y >= 0 and rendered_cursor_y <= self.render_height:
                # Draw a simple vertical line cursor
                cursor_width = 2 * self.render_scale
                cursor_height = self.config.font_size * self.render_scale
                self.canvas.drawRect(
                    skia.Rect(cursor_x,
                             rendered_cursor_y - cursor_height * 0.8,
                             cursor_x + cursor_width,
                             rendered_cursor_y + cursor_height * 0.2),
                    cursor_paint
                )

        # Get pixel data
        image = self.surface.makeImageSnapshot()

        # Convert to numpy array
        pixels = image.tobytes()
        frame = np.frombuffer(pixels, dtype=np.uint8).reshape(
            (self.render_height, self.render_width, 4)
        )

        # Convert RGBA to BGR for OpenCV
        frame = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR)

        # Downscale if using supersampling
        if self.render_scale > 1:
            # Use INTER_AREA for more stable downsampling (less ringing)
            if self.config.downscale_filter == "area":
                interpolation = cv2.INTER_AREA
            else:
                interpolation = cv2.INTER_LANCZOS4
            frame = cv2.resize(frame, (self.config.width, self.config.height),
                              interpolation=interpolation)

        return frame

    def create_animation(self, code: str, language: str, output_path: str, progress_callback=None):
        """Create the animation video with optional progress callback"""
        tokens = self._tokenize_code(code, language)
        total_chars = sum(len(text) for _, text in tokens)

        # Calculate video duration
        duration = total_chars / self.config.typing_speed
        total_frames = int(duration * self.settings["fps"])

        # Estimate memory usage and warn if high
        frame_size_mb = (self.config.width * self.config.height * 3) / (1024 * 1024)
        estimated_peak_memory_mb = frame_size_mb * 3  # Current + previous + working
        if self.config.quality == "ultra":
            estimated_peak_memory_mb *= 1.25 * 1.25  # Account for supersampling

        if estimated_peak_memory_mb > 500:
            print(f"⚠️ Warning: Estimated peak memory usage: {estimated_peak_memory_mb:.0f} MB")
            print(f"  Consider using lower quality or resolution for very long videos.")

        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, self.settings["fps"],
                            (self.config.width, self.config.height))

        print(f"Rendering {total_frames} frames at {self.config.quality} quality...")
        start_time = time.time()

        # Generate frames - OPTIMIZED: Only keep previous frame for motion blur
        previous_frame = None
        # Recreate surface periodically for very long videos to prevent memory buildup
        recreate_every = 100 if total_frames > 500 else None

        for frame_num in range(total_frames):
            progress = frame_num / total_frames
            chars_to_show = int(total_chars * progress)

            # Recreate surface periodically for memory management
            should_recreate = recreate_every and frame_num % recreate_every == 0 and frame_num > 0
            frame = self._render_frame(tokens, chars_to_show, recreate_surface=should_recreate, frame_num=frame_num)

            # Motion blur for smoother animation (high/ultra quality)
            if self.settings.get("motion_blur") and previous_frame is not None:
                frame = cv2.addWeighted(frame, 0.7, previous_frame, 0.3, 0)

            out.write(frame)

            # Only keep the current frame for next iteration's motion blur
            previous_frame = frame.copy() if self.settings.get("motion_blur") else None

            # Periodic garbage collection for long videos
            if frame_num % 50 == 0 and frame_num > 0:
                gc.collect()

            # Progress indicator
            if frame_num % 10 == 0:
                elapsed = time.time() - start_time
                fps_actual = frame_num / elapsed if elapsed > 0 else 0
                print(f"Progress: {frame_num}/{total_frames} ({progress*100:.1f}%) - {fps_actual:.1f} fps", end='\r')

                # Call progress callback if provided
                if progress_callback:
                    progress_callback(frame_num, total_frames, progress * 100)

        # Add a pause at the end showing complete code
        final_frame = self._render_frame(tokens, total_chars)
        for _ in range(self.settings["fps"]):  # 1 second pause
            out.write(final_frame)

        out.release()

        elapsed = time.time() - start_time
        print(f"\nCompleted in {elapsed:.1f}s - Average {total_frames/elapsed:.1f} fps")

        # Skip FFmpeg optimization if not available
        # Video works fine without it, just slightly larger file size

        # Return the output path for confirmation
        return output_path



def create_animation(code: str, language: str = "python",
                    output: str = "output.mp4", quality: str = "high"):
    """Simple API for creating animations"""
    config = RenderConfig(quality=quality)
    renderer = ModernCodeRenderer(config)
    renderer.create_animation(code, language, output)
    return output