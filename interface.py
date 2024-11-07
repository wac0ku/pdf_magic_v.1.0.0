# Autor: Leon Gajtner
# Datum: 07.11.2024
# PDF Magic Interface
# Version: 1.0.0

import os
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QPushButton, 
                           QTextEdit, QProgressBar, QFileDialog,
                           QListWidget, QHBoxLayout, QMessageBox,
                           QLabel, QMainWindow, QStatusBar, QMenu,
                           QMenuBar, QAction, QSystemTrayIcon)
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont

from enhanced_drag_drop import EnhancedDragDrop
from style import apply_styles
from utils import ConversionWorker, update_log, update_progress_bar, show_error_message

class PDFMagicApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.pdf_files = []
        self.last_directory = None
        self.init_ui()
        self.setup_system_tray()

    def init_ui(self):
        """Initialisiert die Benutzeroberfläche mit einem modernen und intuitiven Design"""
        self.setWindowTitle("PDF Magic - PDF zu DOCX Konverter")
        self.setGeometry(100, 100, 1000, 700)
        apply_styles(self)

        # Hauptwidget und Layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Menüleiste erstellen
        self.create_menu_bar()

        # Willkommensbereich
        welcome_layout = QVBoxLayout()
        welcome_layout.setAlignment(Qt.AlignCenter)

        # Willkommens-Label
        welcome_label = QLabel("Willkommen bei PDF Magic!")
        welcome_label.setObjectName("welcome_label")
        welcome_label.setFont(QFont('Segoe UI', 24))
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(welcome_label)
        
        # Untertext
        instructions = QLabel("Konvertieren Sie Ihre PDF-Dateien einfach in DOCX-Format.")
        instructions.setObjectName("instructions_label")
        instructions.setFont(QFont('Segoe UI', 14))
        instructions.setAlignment(Qt.AlignCenter)
        welcome_layout.addWidget(instructions)
        
        # Abstand nach unten
        spacer = QWidget()
        spacer.setFixedHeight(20)
        welcome_layout.addWidget(spacer)
        
        main_layout.addLayout(welcome_layout)
    
        # Drag & Drop Bereich
        self.drag_drop_widget = EnhancedDragDrop(self)
        main_layout.addWidget(self.drag_drop_widget)
    
        # Horizontales Layout für Liste und Log
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # Dateiliste mit Beschriftung
        list_container = QVBoxLayout()
        list_label = QLabel("PDF-Dateien:")
        list_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        list_container.addWidget(list_label)

        self.file_list = QListWidget()
        self.file_list.setMinimumWidth(300)
        self.file_list.setAlternatingRowColors(True)
        list_container.addWidget(self.file_list)
        content_layout.addLayout(list_container)

        # Log-Fenster mit Beschriftung
        log_container = QVBoxLayout()
        log_label = QLabel("Protokoll:")
        log_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        log_container.addWidget(log_label)

        self.log_window = QTextEdit()
        self.log_window.setReadOnly(True)
        log_container.addWidget(self.log_window)
        content_layout.addLayout(log_container)

        main_layout.addLayout(content_layout)

        # Fortschrittsanzeige
        progress_container = QVBoxLayout()
        progress_label = QLabel("Fortschritt:")
        progress_label.setFont(QFont('Segoe UI', 12, QFont.Bold))
        progress_container.addWidget(progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setFormat("%p% - %v von %m Dateien")
        progress_container.addWidget(self.progress_bar)
        main_layout.addLayout(progress_container)

        # Button-Layout
        button_layout = QHBoxLayout()
        button_layout.setAlignment(Qt.AlignCenter)

        # Buttons
        self.open_button = QPushButton("Dateien öffnen")
        self.open_button.setToolTip("PDF-Dateien zum Konvertieren auswählen")
        self.open_button.clicked.connect(self.open_file_dialog)
        button_layout.addWidget(self.open_button)

        self.convert_button = QPushButton("Konvertieren")
        self.convert_button.setToolTip("Ausgewählte PDF-Dateien in DOCX konvertieren")
        self.convert_button.clicked.connect(self.convert_pdfs)
        button_layout.addWidget(self.convert_button)

        main_layout.addLayout(button_layout)

        # Statusleiste
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        self.statusBar.showMessage("Bereit")

    def create_menu_bar(self):
        """Erstellt eine benutzerfreundliche Menüleiste"""

        menubar = self.menuBar()

        # Datei-Menü
        file_menu = menubar.addMenu('&Datei')
        open_action = QAction('&Öffnen', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('PDF-Dateien öffnen')
        open_action.triggered.connect(self.open_file_dialog)
        file_menu.addAction(open_action)
        exit_action = QAction('&Beenden', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Anwendung beenden')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Hilfe-Menü
        help_menu = menubar.addMenu('&Hilfe')
        about_action = QAction('&Über', self)
        about_action.setStatusTip('Über PDF Magic')
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def setup_system_tray(self):
        """Richtet ein System Tray Icon für schnellen Zugriff ein"""
        self.tray_icon = QSystemTrayIcon(self)
        tray_menu = QMenu()

        # Aktion zum Öffnen des Hauptfensters
        show_action = QAction("PDF Magic öffnen", self)
        show_action.triggered.connect(self.show)
        tray_menu.addAction(show_action)

        # Aktion zum schnellen Öffnen von Dateien
        quick_open_action = QAction("Schnell PDF öffnen", self)
        quick_open_action.triggered.connect(self.quick_open_pdf)
        tray_menu.addAction(quick_open_action)

        # Trennlinie
        tray_menu.addSeparator()

        # Beenden-Aktion
        quit_action = QAction("Beenden", self)
        quit_action.triggered.connect(self.close)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

        # Verbinde Doppelklick auf das Tray-Icon mit dem Öffnen des Hauptfensters
        self.tray_icon.activated.connect(self.tray_icon_activated)

    def tray_icon_activated(self, reason):
        """Behandelt Aktivierungen des Tray-Icons"""
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()

    def quick_open_pdf(self):
        """Öffnet schnell eine PDF-Datei über das Tray-Menü"""
        file_path, _ = QFileDialog.getOpenFileName(self, "PDF schnell öffnen", "", "PDF Dateien (*.pdf)")
        if file_path:
            self.add_pdf_file(file_path)
            self.show()  # Zeigt das Hauptfenster an

    def add_pdf_file(self, file_path):
        """Fügt eine PDF-Datei zur Liste hinzu"""
        if file_path not in self.pdf_files:
            self.pdf_files.append(file_path)
            self.file_list.addItem(os.path.basename(file_path))
            self.update_status()

    def update_status(self):
        """Aktualisiert die Statusleiste mit der aktuellen Anzahl der PDF-Dateien"""
        file_count = len(self.pdf_files)
        self.statusBar.showMessage(f"{file_count} PDF-Datei{'en' if file_count != 1 else ''} bereit zur Konvertierung")

    def open_file_dialog(self):
        """Öffnet einen Datei-Dialog zum Auswählen von PDF-Dateien"""
        files, _ = QFileDialog.getOpenFileNames(self, "PDF-Dateien auswählen", self.last_directory, "PDF Dateien (*.pdf)")
        if files:
            self.last_directory = os.path.dirname(files[0])
            for file in files:
                self.add_pdf_file(file)

    def convert_pdfs(self):
        """Startet den Konvertierungsprozess für die ausgewählten PDF-Dateien"""
        if not self.pdf_files:
            show_error_message("Bitte wählen Sie zuerst PDF-Dateien aus.")
            return

        output_dir = QFileDialog.getExistingDirectory(self, "Ausgabeordner wählen", "")
        if not output_dir:
            return

        self.progress_bar.setMaximum(len(self.pdf_files))
        self.progress_bar.setValue(0)

        self.worker = ConversionWorker(self.pdf_files, output_dir)
        self.worker_thread = QThread()
        self.worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.worker_thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker.progress.connect(lambda value: update_progress_bar(self.progress_bar, value))
        self.worker.log.connect(lambda message: update_log(self.log_window, message))
        self.worker.error.connect(show_error_message)

        self.worker_thread.start()

        self.convert_button.setEnabled(False)
        self.worker_thread.finished.connect(
            lambda: self.convert_button.setEnabled(True)
        )
        self.worker_thread.finished.connect(self.conversion_finished)

    def conversion_finished(self):
        """Wird aufgerufen, wenn die Konvertierung abgeschlossen ist"""
        QMessageBox.information(self, "Konvertierung abgeschlossen", 
                                "Alle PDF-Dateien wurden erfolgreich konvertiert!")
        self.pdf_files.clear()
        self.file_list.clear()
        self.update_status()

    def show_about(self):
        """Zeigt Informationen über die Anwendung"""
        QMessageBox.about(self, "Über PDF Magic",
            "PDF Magic v2.1\n\n"
            "Ein benutzerfreundlicher PDF zu DOCX Konverter\n"
            "Entwickelt von Leon Gajtner\n\n"
            "© 2024 Alle Rechte vorbehalten")

    def closeEvent(self, event):
        """Behandelt das Schließen-Event des Hauptfensters"""
        reply = QMessageBox.question(self, 'Bestätigung',
            "Möchten Sie PDF Magic wirklich beenden?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()
            self.tray_icon.hide()  # Entfernt das Tray-Icon beim Beenden
        else:
            event.ignore()
            self.hide()  # Versteckt das Hauptfenster statt es zu schließen

    def handle_dropped_files(self, files):
        """Verarbeitet die per Drag & Drop hinzugefügten Dateien"""
        for file_path in files:
            if file_path.lower().endswith('.pdf'):
                self.add_pdf_file(file_path)
            else:      
                show_error_message(f"Die Datei {os.path.basename(file_path)} ist keine PDF-Datei.")

    def dragEnterEvent(self, event):
        """Behandelt das Drag-Enter Event für das Hauptfenster"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Behandelt das Drop Event für das Hauptfenster"""
        file_paths = [url.toLocalFile() for url in event.mimeData().urls()]
        self.handle_dropped_files(file_paths)

    def check_conversion_status(self):
        """Überprüft den Status der Konvertierung und aktualisiert die UI entsprechend"""
        if hasattr(self, 'worker_thread') and self.worker_thread.isRunning():
            return True
        return False

    def clear_files(self):
        """Löscht alle ausgewählten Dateien aus der Liste"""
        self.pdf_files.clear()
        self.file_list.clear()
        self.update_status()
        self.log_window.clear()
        self.progress_bar.setValue(0)

    def remove_selected_file(self):
        """Entfernt die ausgewählte Datei aus der Liste"""
        current_row = self.file_list.currentRow()
        if current_row >= 0:
            removed_file = self.pdf_files.pop(current_row)
            self.file_list.takeItem(current_row)
            self.update_status()
            self.log_window.append(f"Datei entfernt: {removed_file}")

    def keyPressEvent(self, event):
        """Behandelt Tastatureingaben"""
        if event.key() == Qt.Key_Delete:
            self.remove_selected_file()
        elif event.key() == Qt.Key_Escape:
            if not self.check_conversion_status():
                self.hide()
        super().keyPressEvent(event)

    def showEvent(self, event):
        """Wird aufgerufen, wenn das Fenster angezeigt wird"""
        super().showEvent(event)
        self.update_status()
        self.statusBar.showMessage("Bereit für neue Konvertierungen")

    def hideEvent(self, event):
        """Wird aufgerufen, wenn das Fenster versteckt wird"""
        super().hideEvent(event)
        if self.tray_icon.isVisible():
            self.tray_icon.showMessage(
                "PDF Magic",
                "Die Anwendung läuft im Hintergrund weiter.",
                QSystemTrayIcon.Information,
                2000
            )

    def contextMenuEvent(self, event):
        """Erstellt ein Kontextmenü für die Dateiliste"""
        if self.file_list.underMouse():
            context_menu = QMenu(self)
            
            remove_action = QAction("Entfernen", self)
            remove_action.triggered.connect(self.remove_selected_file)
            context_menu.addAction(remove_action)
            
            clear_action = QAction("Alle löschen", self)
            clear_action.triggered.connect(self.clear_files)
            context_menu.addAction(clear_action)
            
            context_menu.exec_(event.globalPos())

    def update_ui_state(self, is_converting=False):
        """Aktualisiert den Zustand der UI-Elemente basierend auf dem Konvertierungsstatus"""
        self.open_button.setEnabled(not is_converting)
        self.convert_button.setEnabled(not is_converting and len(self.pdf_files) > 0)
        self.file_list.setEnabled(not is_converting)
        self.drag_drop_widget.setEnabled(not is_converting)

    def show_error_dialog(self, message):
        """Zeigt einen Fehlerdialog an"""
        QMessageBox.critical(self, "Fehler", message)

    def show_success_dialog(self, message):
        """Zeigt einen Erfolgsdialog an"""
        QMessageBox.information(self, "Erfolg", message)

    def show_warning_dialog(self, message):
        """Zeigt einen Warnungsdialog an"""
        QMessageBox.warning(self, "Warnung", message)

    def log_message(self, message):
        """Fügt eine Nachricht zum Log-Fenster hinzu"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_window.append(f"[{timestamp}] {message}")

    def clear_log(self):
        """Löscht den Inhalt des Log-Fensters"""
        self.log_window.clear()

    def save_log(self):
        """Speichert den Log-Inhalt in eine Datei"""
        file_name, _ = QFileDialog.getSaveFileName(self, "Log speichern", "", "Text Dateien (*.txt)")
        if file_name:
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(self.log_window.toPlainText())
            self.show_success_dialog("Log wurde erfolgreich gespeichert.")