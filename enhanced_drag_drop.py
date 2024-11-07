# Autor: Leon Gajtner
# Datum: 07.11.2024
# Enhanced Drag & Drop
# Version: 1.0.0

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class EnhancedDragDrop(QWidget):
    """Erweitertes Drag & Drop Widget mit verbesserter Benutzerführung"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)
        self.setup_ui()
        
    def setup_ui(self):
        """Initialisiert die Benutzeroberfläche des Drag & Drop Bereichs"""
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Drag & Drop Beschreibung
        self.label = QLabel("Ziehen Sie PDF-Dateien hierher oder klicken Sie zum Auswählen", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        layout.addWidget(self.label)
        
        # Minimale Größe setzen
        self.setMinimumHeight(150)
        
    def dragEnterEvent(self, event):
        """Behandelt das Drag-Enter Event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet("background-color: #e3f2fd;")
    
    def dragLeaveEvent(self, event):
        """Behandelt das Drag-Leave Event"""
        self.setStyleSheet("")
        
    def dropEvent(self, event):
        """Behandelt das Drop Event"""
        self.setStyleSheet("")
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.parent().handle_dropped_files(file_paths)
        
    def mousePressEvent(self, event):
        """Behandelt Mausklicks"""
        if event.button() == Qt.LeftButton:
            self.parent().open_file_dialog()