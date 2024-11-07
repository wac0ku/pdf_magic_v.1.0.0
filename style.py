# Autor: Leon Gajtner
# Datum: 07.11.2024
# PDF Magic Style
# Version: 1.0.0

from PyQt5.QtWidgets import QWidget

def apply_styles(widget: QWidget):
    """
    Wendet die definierten Styles auf das Widget und seine Unterkomponenten an.
    
    :param widget: Das Widget, auf das die Styles angewendet werden sollen
    """
    
    # Moderne Farbpalette
    PRIMARY_COLOR = "#2c3e50"      # Dunkelblau
    ACCENT_COLOR = "#3498db"       # Hellblau
    BACKGROUND_COLOR = "#f8f9fa"   # Helles Grau
    SECONDARY_BG = "#ffffff"       # Weiß
    TEXT_COLOR = "#2c3e50"         # Dunkelblau
    BORDER_COLOR = "#e9ecef"       # Hellgrau
    
    widget.setStyleSheet(f"""
        QWidget {{
            background-color: {BACKGROUND_COLOR};
            color: {TEXT_COLOR};
            font-family: 'Segoe UI', Arial, sans-serif;
        }}
        
        QLabel#welcome_label {{
            color: {PRIMARY_COLOR};
            font-weight: bold;
            padding: 20px;
        }}
        
        QLabel#instructions_label {{
            color: {PRIMARY_COLOR};
            padding: 10px;
        }}
        
        /* Style für den Drag & Drop Bereich */
        EnhancedDragDrop {{
            background-color: {SECONDARY_BG};
            border: 2px dashed {BORDER_COLOR};
            border-radius: 10px;
            padding: 20px;
            margin: 20px;
        }}
        
        EnhancedDragDrop:hover {{
            border-color: {ACCENT_COLOR};
            background-color: #f8f9fa;
        }}
        
        /* Style für das Log-Fenster */
        QTextEdit {{
            background-color: {SECONDARY_BG};
            border: 1px solid {BORDER_COLOR};
            border-radius: 8px;
            padding: 10px;
            font-size: 12px;
            color: {TEXT_COLOR};
        }}
        
        /* Style für die Fortschrittsanzeige */
        QProgressBar {{
            border: none;
            border-radius: 4px;
            text-align: center;
            height: 20px;
            background-color: {BORDER_COLOR};
        }}
        
        QProgressBar::chunk {{
            background-color: {ACCENT_COLOR};
            border-radius: 4px;
        }}
        
        /* Style für die Buttons */
        QPushButton {{
            background-color: {ACCENT_COLOR};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-size: 14px;
            min-width: 120px;
            margin: 5px;
        }}
        
        QPushButton:hover {{
            background-color: {PRIMARY_COLOR};
        }}
        
        QPushButton:pressed {{
            background-color: #1a252f;
        }}
        
        QPushButton:disabled {{
            background-color: {BORDER_COLOR};
            color: #95a5a6;
        }}
        
        /* Style für die Dateiliste */
        QListWidget {{
            background-color: {SECONDARY_BG};
            border: 1px solid {BORDER_COLOR};
            border-radius: 8px;
            padding: 5px;
        }}
        
        QListWidget::item {{
            padding: 5px;
            border-radius: 4px;
        }}
        
        QListWidget::item:selected {{
            background-color: {ACCENT_COLOR};
            color: white;
        }}
        
        QListWidget::item:hover {{
            background-color: {BORDER_COLOR};
        }}
        
        /* Style für die Statusleiste */
        QStatusBar {{
            background-color: {PRIMARY_COLOR};
            color: white;
            padding: 8px;
        }}
        
        /* Style für die Menüleiste */
        QMenuBar {{
            background-color: {PRIMARY_COLOR};
            color: white;
            padding: 2px;
        }}
        
        QMenuBar::item {{
            padding: 5px 10px;
            background-color: transparent;
        }}
        
        QMenuBar::item:selected {{
            background-color: {ACCENT_COLOR};
        }}
        
        QMenu {{
            background-color: {SECONDARY_BG};
            border: 1px solid {BORDER_COLOR};
        }}
        
        QMenu::item {{
            padding: 5px 30px 5px 20px;
        }}
        
        QMenu::item:selected {{
            background-color: {ACCENT_COLOR};
            color: white;
        }}
    """)

def get_drag_drop_style(is_dragging: bool = False) -> str:
    """
    Gibt den Style für den Drag & Drop Bereich zurück, abhängig vom Zustand.
    
    :param is_dragging: Bool, der angibt, ob gerade etwas gedraggt wird
    :return: String mit den CSS-Styles
    """
    base_style = """
        background-color: #ffffff;
        border: 2px dashed #cccccc;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
    """
    
    dragging_style = """
        background-color: #E3F2FD;
        border: 2px dashed #2196F3;
        border-radius: 10px;
        padding: 20px;
        margin: 10px;
    """
    
    return dragging_style if is_dragging else base_style

def get_button_style(is_primary: bool = True) -> str:
    """
    Gibt den Style für Buttons zurück, abhängig vom Typ.
    
    :param is_primary: Bool, der angibt, ob es sich um einen primären Button handelt
    :return: String mit den CSS-Styles
    """
    primary_style = """
        background-color: #2196F3;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 14px;
        min-width: 100px;
        margin: 5px;
    """
    
    secondary_style = """
        background-color: #757575;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 14px;
        min-width: 100px;
        margin: 5px;
    """
    
    return primary_style if is_primary else secondary_style

def get_log_window_style() -> str:
    """
    Gibt den Style für das Log-Fenster zurück.
    
    :return: String mit den CSS-Styles
    """
    return """
        background-color: #ffffff;
        border: 1px solid #cccccc;
        border-radius: 5px;
        padding: 5px;
        font-size: 12px;
        color: #333333;
    """

def get_progress_bar_style() -> str:
    """
    Gibt den Style für die Fortschrittsanzeige zurück.
    
    :return: String mit den CSS-Styles
    """
    return """
        QProgressBar {
            border: 1px solid #cccccc;
            border-radius: 5px;
            text-align: center;
            height: 20px;
        }
        
        QProgressBar::chunk {
            background-color: #2196F3;
            border-radius: 4px;
        }
    """