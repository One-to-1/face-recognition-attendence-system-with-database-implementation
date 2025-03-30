"""
Icons for the Face Recognition Attendance System UI.
This file contains SVG icons encoded in Base64 format.
"""

import base64
from PyQt5.QtGui import QIcon, QPixmap

def get_icon_from_base64(base64_string):
    """Convert a Base64 string to a QIcon"""
    pixmap = QPixmap()
    pixmap.loadFromData(base64.b64decode(base64_string))
    return QIcon(pixmap)

# User plus icon (for registration)
USER_PLUS_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
<circle cx="8.5" cy="7" r="4"></circle>
<line x1="20" y1="8" x2="20" y2="14"></line>
<line x1="23" y1="11" x2="17" y2="11"></line>
</svg>
"""

# Camera icon (for attendance)
CAMERA_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"></path>
<circle cx="12" cy="13" r="4"></circle>
</svg>
"""

# Chart icon (for analytics)
CHART_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<line x1="18" y1="20" x2="18" y2="10"></line>
<line x1="12" y1="20" x2="12" y2="4"></line>
<line x1="6" y1="20" x2="6" y2="14"></line>
</svg>
"""

# Save icon
SAVE_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"></path>
<polyline points="17 21 17 13 7 13 7 21"></polyline>
<polyline points="7 3 7 8 15 8"></polyline>
</svg>
"""

# Check icon (for success)
CHECK_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<polyline points="20 6 9 17 4 12"></polyline>
</svg>
"""

# Close icon (for cancellation)
CLOSE_ICON = """
<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" 
stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
<line x1="18" y1="6" x2="6" y2="18"></line>
<line x1="6" y1="6" x2="18" y2="18"></line>
</svg>
"""

# Helper functions to get icons
def get_user_plus_icon():
    return get_icon_from_base64(base64.b64encode(USER_PLUS_ICON.encode()).decode())

def get_camera_icon():
    return get_icon_from_base64(base64.b64encode(CAMERA_ICON.encode()).decode())

def get_chart_icon():
    return get_icon_from_base64(base64.b64encode(CHART_ICON.encode()).decode())

def get_save_icon():
    return get_icon_from_base64(base64.b64encode(SAVE_ICON.encode()).decode())

def get_check_icon():
    return get_icon_from_base64(base64.b64encode(CHECK_ICON.encode()).decode())

def get_close_icon():
    return get_icon_from_base64(base64.b64encode(CLOSE_ICON.encode()).decode())