# Autor: Leon Gajtner 
# Datum: 07.11.2024
# PDF Magic Enhanced Drag and Drop Module
# Version: 2.1

import os
import logging
import types
from typing import List, Set
from datetime import datetime

from PyQt5.QtWidgets import (QWidget, QLabel, QVBoxLayout, 
                            QApplication, QStyle, QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import (QDragEnterEvent, QDropEvent, QDragLeaveEvent)

class EnhancedDragDrop(QWidget):
    """
    Verbesserte Drag & Drop Komponente mit umfassender Fehlerbehandlung 
    und Benutzer-Feedback
    """
    
    # Signals für verschiedene Events
    fileDropped = pyqtSignal(list)  # Signal für erfolgreich gedropte Dateien
    errorOccurred = pyqtSignal(str)  # Signal für Fehlermeldungen
    warningOccurred = pyqtSignal(str)  # Signal für Warnungen
    progressUpdated = pyqtSignal(int)  # Signal für Fortschrittsanzeige

    def __init__(self, parent=None):
        """Initialisiert das EnhancedDragDrop Widget"""
        super().__init__(parent)
        
        # Grundlegende Konfiguration
        self.parent_widget = parent
        self.accepted_extensions: Set[str] = {'.pdf'}
        self.max_file_size: int = 100 * 1024 * 1024  # 100 MB
        self.max_files: int = 50
        self.min_file_size: int = 1024  # 1 KB
        self.is_dragging: bool = False
        self.processed_files: Set[str] = set()
        
        # UI Initialisierung
        self.init_ui()
        self.setup_logging()
        self.setup_styles()

    def init_ui(self):
        """Initialisiert die Benutzeroberfläche"""
        self.setAcceptDrops(True)
        self.setMinimumSize(400, 200)
        
        # Hauptlayout
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Icon
        self.icon_label = QLabel()
        icon = QApplication.style().standardIcon(QStyle.SP_DialogOpenButton)
        self.icon_label.setPixmap(icon.pixmap(QSize(48, 48)))
        layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        
        # Haupttext
        self.main_label = QLabel("PDF-Dateien hier ablegen")
        self.main_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.main_label)
        
        # Untertext
        self.sub_label = QLabel(
            f"Maximale Dateigröße: {self.max_file_size/1024/1024:.0f}MB\n"
            f"Unterstützte Formate: {', '.join(self.accepted_extensions)}"
        )
        self.sub_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.sub_label)
        
        # Fortschrittsanzeige
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.setLayout(layout)

    def setup_logging(self):
        """Konfiguriert das Logging-System"""
        self.logger = logging.getLogger('EnhancedDragDrop')
        self.logger.setLevel(logging.DEBUG)
        
        # Erstelle einen FileHandler
        log_file = f'drag_drop_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def setup_styles(self):
        """Definiert und setzt die Styles für das Widget"""
        self.normal_style = """
            QWidget {
                background-color: #ffffff;
                border: 2px dashed #cccccc;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                color: #666666;
                font-size: 14px;
            }
        """
        
        self.drag_style = """
            QWidget {
                background-color: #e3f2fd;
                border: 2px dashed #2196f3;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                color: #2196f3;
                font-size: 14px;
            }
        """
        
        self.error_style = """
            QWidget {
                background-color: #ffebee;
                border: 2px dashed #f44336;
                border-radius: 10px;
                padding: 20px;
            }
            QLabel {
                color: #f44336;
                font-size: 14px;
            }
        """
        
        self.setStyleSheet(self.normal_style)

    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Behandelt das DragEnter-Event mit Validierung"""
        try:
            if not event.mimeData().hasUrls():
                self.show_warning("Nur Dateien können hier abgelegt werden")
                event.ignore()
                return

            urls = event.mimeData().urls()
            if self.validate_dragged_files(urls):
                self.is_dragging = True
                self.update_appearance(True)
                event.acceptProposedAction()
            else:
                self.update_appearance(False, error=True)
                event.ignore()

        except Exception as e:
            self.logger.error(f"Fehler in dragEnterEvent: {str(e)}")
            self.show_error(f"Unerwarteter Fehler: {str(e)}")
            event.ignore()

    def dragLeaveEvent(self, event: QDragLeaveEvent) -> None:
        """Behandelt das DragLeave-Event"""
        self.is_dragging = False
        self.update_appearance(False)
        self.progress_bar.setVisible(False)

    def dropEvent(self, event: QDropEvent) -> None:
        """Behandelt das Drop-Event mit umfassender Validierung und Fehlerbehandlung"""
        try:
            self.is_dragging = False
            self.update_appearance(False)
            
            if not event.mimeData().hasUrls():
                self.show_warning("Keine gültigen Dateien gefunden")
                event.ignore()
                return

            urls = event.mimeData().urls()
            file_paths = [url.toLocalFile() for url in urls]
            
            # Validiere die Dateien
            valid_files = self.process_dropped_files(file_paths)
            
            if valid_files:
                self.fileDropped.emit(valid_files)
                event.acceptProposedAction()
                self.show_success(f"{len(valid_files)} Datei(en) erfolgreich hinzugefügt")
            else:
                self.show_warning("Keine gültigen Dateien zum Hinzufügen gefunden")
                event.ignore()

        except Exception as e:
            self.logger.error(f"Unerwarteter Fehler in dropEvent: {str(e)}")
            self.show_error(f"Unerwarteter Fehler beim Verarbeiten der Dateien: {str(e)}")
            event.ignore()
        finally:
            self.progress_bar.setVisible(False)

    def process_dropped_files(self, file_paths: List[str]) -> List[str]:
        """Verarbeitet und validiert die gedropten Dateien"""
        valid_files = []
        total_files = len(file_paths)
        
        self.progress_bar.setVisible(True)
        self.progress_bar.setMaximum(total_files)
        
        for index, file_path in enumerate(file_paths):
            try:
                if file_path in self.processed_files:
                    self.show_warning(f"Datei bereits verarbeitet: {file_path}")
                    continue

                if not os.path.exists(file_path):
                    self.show_warning(f"Datei nicht gefunden: {file_path}")
                    continue

                if not os.access(file_path, os.R_OK):
                    self.show_warning(f"Keine Leserechte für: {file_path}")
                    continue

                if self.is_hidden_file(file_path):
                    self.show_warning(f"Versteckte Datei ignoriert: {file_path}")
                    continue

                file_size = os.path.getsize(file_path)
                if file_size == 0:
                    self.show_warning(f"Leere Datei gefunden: {file_path}")
                    continue

                if file_size > self.max_file_size:
                    self.show_warning(f"Datei zu groß (max. {self.max_file_size/1024/1024:.0f}MB): {file_path}")
                    continue

                if file_size < self.min_file_size:
                    self.show_warning(f"Datei zu klein (min. {self.min_file_size/1024:.0f}KB): {file_path}")
                    continue

                if not any(file_path.lower().endswith(ext) for ext in self.accepted_extensions):
                    self.show_warning(f"Ungültiges Dateiformat: {file_path}")
                    continue

                valid_files.append(file_path)
                self.processed_files.add(file_path)

            except Exception as e:
                self.logger.error(f"Fehler bei der Verarbeitung von {file_path}: {str(e)}")
                self.show_error(f"Fehler bei der Verarbeitung von {os.path.basename(file_path)}")

            finally:
                self.progress_bar.setValue(index + 1)
                self.progressUpdated.emit(int((index + 1) / total_files * 100))

        return valid_files

    def is_hidden_file(self, file_path: str) -> bool:
        """Überprüft, ob eine Datei versteckt ist"""
        return os.path.basename(file_path).startswith('.') or \
               (os.name == 'nt' and os.stat(file_path).st_file_attributes & 2)

    def update_appearance(self, is_dragging: bool, error: bool = False) -> None:
        """Aktualisiert das Erscheinungsbild basierend auf dem Zustand"""
        if error:
            self.setStyleSheet(self.error_style)
            self.main_label.setText("Fehler beim Hinzufügen der Dateien")
        elif is_dragging:
            self.setStyleSheet(self.drag_style)
            self.main_label.setText("Dateien hier ablegen")
        else:
            self.setStyleSheet(self.normal_style)
            self.main_label.setText("PDF-Dateien hier ablegen")

    def show_warning(self, message: str) -> None:
        """Zeigt eine Warnung an und emittiert ein Warn-Signal"""
        self.logger.warning(message)
        self.warningOccurred.emit(message)

    def show_error(self, message: str) -> None:
        """Zeigt einen Fehler an und emittiert ein Fehler-Signal"""
        self.logger.error(message)
        self.errorOccurred.emit(message)
        self.update_appearance(False, error=True)

    def show_success(self, message: str) -> None:
        """Zeigt eine Erfolgsmeldung an"""
        self.logger.info(message)
        self.main_label.setText(message)
        self.update_appearance(False)

    def reset(self) -> None:
        """Setzt den Zustand des Widgets zurück"""
        self.processed_files.clear()
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        self.update_appearance(False)

    def set_accepted_extensions(self, extensions: Set[str]) -> None:
        """Setzt die akzeptierten Dateierweiterungen"""
        self.accepted_extensions = extensions
        self.update_info_label()

    def set_max_file_size(self, size: int) -> None:
        """Setzt die maximale Dateigröße in Bytes"""
        self.max_file_size = size
        self.update_info_label()

    def set_max_files(self, count: int) -> None:
        """Setzt die maximale Anzahl von Dateien"""
        self.max_files = count

    def update_info_label(self) -> None:
        """Aktualisiert den Infotext mit den aktuellen Einstellungen"""
        self.sub_label.setText(
            f"Maximale Dateigröße: {self.max_file_size/1024/1024:.0f}MB\n"
            f"Unterstützte Formate: {', '.join(self.accepted_extensions)}\n"
            f"Maximale Anzahl Dateien: {self.max_files}"
        )

def apply_enhanced_drag_drop(app):
    """
    Wendet die verbesserte Drag & Drop Funktionalität auf die bestehende App an.
    
    :param app: Die Instanz der PDFMagicApp
    """
    if hasattr(app, 'drag_drop_widget'):
        old_widget = app.drag_drop_widget
        app.drag_drop_widget = EnhancedDragDrop(app)
        app.drag_drop_widget.fileDropped.connect(app.handle_dropped_files)
        app.drag_drop_widget.warningOccurred.connect(app.show_warning_dialog)
        app.drag_drop_widget.errorOccurred.connect(app.show_error_dialog)
        app.drag_drop_widget.progressUpdated.connect(app.update_progress)
        
        # Ersetze das alte Widget im Layout
        layout = app.layout()
        for i in range(layout.count()):
            if layout.itemAt(i).widget() == old_widget:
                layout.replaceWidget(old_widget, app.drag_drop_widget)
                old_widget.deleteLater()
                break
        
        # Übertrage die Einstellungen vom alten Widget
        if hasattr(old_widget, 'accepted_extensions'):
            app.drag_drop_widget.set_accepted_extensions(old_widget.accepted_extensions)
        if hasattr(old_widget, 'max_file_size'):
            app.drag_drop_widget.set_max_file_size(old_widget.max_file_size)
        if hasattr(old_widget, 'max_files'):
            app.drag_drop_widget.set_max_files(old_widget.max_files)
    else:
        app.logger.warning("Kein bestehendes drag_drop_widget gefunden.")

def update_app_for_enhanced_drag_drop(app):
    """
    Aktualisiert die App-Klasse mit zusätzlichen Methoden für EnhancedDragDrop.
    
    :param app: Die Instanz der PDFMagicApp
    """
    def show_warning_dialog(app, message):
        QMessageBox.warning(app, "Warnung", message)
    
    def show_error_dialog(app, message):
        QMessageBox.critical(app, "Fehler", message)
    
    def update_progress(app, value):
        if hasattr(app, 'progress_bar'):
            app.progress_bar.setValue(value)
    
    # Füge die neuen Methoden zur App-Klasse hinzu
    app.show_warning_dialog = types.MethodType(show_warning_dialog, app)
    app.show_error_dialog = types.MethodType(show_error_dialog, app)
    app.update_progress = types.MethodType(update_progress, app)

def integrate_enhanced_drag_drop(app):
    """
    Integriert EnhancedDragDrop vollständig in die bestehende App.
    
    :param app: Die Instanz der PDFMagicApp
    """
    update_app_for_enhanced_drag_drop(app)
    apply_enhanced_drag_drop(app)
    
    # Logging
    app.logger.info("EnhancedDragDrop wurde erfolgreich integriert.")