"""
Stylesheet definitions for the Face Recognition Attendance System UI.
"""

# Main application style
MAIN_STYLE = """
    QMainWindow {
        background-color: #f5f5f7;
    }
    
    QWidget {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 11pt;
    }
    
    QLineEdit {
        border: 1px solid #d1d1d1;
        border-radius: 4px;
        padding: 8px;
        background-color: white;
        selection-background-color: #0078d7;
    }
    
    QLineEdit:focus {
        border: 2px solid #0078d7;
    }
"""

# Title style for section headers
TITLE_STYLE = """
    font-size: 16pt;
    font-weight: bold;
    color: #0078d7;
    margin: 10px 0px;
"""

# Subtitle style
SUBTITLE_STYLE = """
    font-size: 12pt;
    font-weight: bold;
    color: #323130;
"""

# Main button style used across application
MAIN_BUTTON_STYLE = """
    QPushButton {
        background-color: #0078d7;
        color: white;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: bold;
        text-align: left;
        min-height: 40px;
    }
    QPushButton:hover {
        background-color: #106ebe;
    }
    QPushButton:pressed {
        background-color: #005a9e;
    }
    QPushButton:disabled {
        background-color: #cccccc;
        color: #999999;
    }
"""

# Secondary button style (for less important actions)
SECONDARY_BUTTON_STYLE = """
    background-color: #f0f0f0;
    color: #323130;
    border: 1px solid #d1d1d1;
    border-radius: 4px;
    padding: 10px;
    min-height: 40px;
"""

# Danger button style (for destructive actions)
DANGER_BUTTON_STYLE = """
    background-color: #d13438;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px;
    font-weight: bold;
    min-height: 40px;
"""

# Success button style
SUCCESS_BUTTON_STYLE = """
    background-color: #107c10;
    color: white;
    border: none;
    border-radius: 4px;
    padding: 10px;
    font-weight: bold;
    min-height: 40px;
"""

# Card container style
CARD_STYLE = """
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    margin: 10px;
    border: 1px solid #f0f0f0;
"""