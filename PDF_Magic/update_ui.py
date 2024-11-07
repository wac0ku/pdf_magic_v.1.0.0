# Autor: Leon Gajtner
# Datum: 07.11.2024
# Version: 2.1
# update_ui.py

import os
import re

def update_main_window(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Füge die Import-Anweisung hinzu, falls noch nicht vorhanden
    if 'QFileDialog' not in content:
        import_pattern = r'from PyQt5\.QtWidgets import (.*?)\)'
        import_replacement = r'from PyQt5.QtWidgets import \1, QFileDialog)'
        content = re.sub(import_pattern, import_replacement, content, flags=re.DOTALL)

    # Füge die Initialisierung des output_dir in __init__ hinzu
    init_pattern = r'(def __init__\(self\):.*?super\(\).__init__\(\))'
    init_replacement = r'\1\n        self.output_dir = None'
    content = re.sub(init_pattern, init_replacement, content, flags=re.DOTALL)

    # Füge den neuen Button hinzu
    button_layout_pattern = r'(button_layout = QHBoxLayout\(\).*?button_layout\.addWidget\(self\.convert_button\))'
    button_layout_replacement = r'\1\n\n        self.save_location_button = QPushButton("Speichern unter")\n        self.save_location_button.setToolTip("Speicherort für konvertierte Dateien auswählen")\n        self.save_location_button.clicked.connect(self.select_save_location)\n        button_layout.addWidget(self.save_location_button)'
    content = re.sub(button_layout_pattern, button_layout_replacement, content, flags=re.DOTALL)

    # Füge die select_save_location Methode hinzu
    if 'def select_save_location' not in content:
        # Finde das Ende der Klasse
        class_content = content.split('class PDFMagicApp(QMainWindow):')[1]
        last_method = class_content.rstrip()
        
        # Füge die neue Methode hinzu
        new_method = '''
    def select_save_location(self):
        """Öffnet einen Dialog zur Auswahl des Speicherorts"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Speicherort auswählen",
            self.output_dir or os.path.expanduser("~/Documents")
        )
        if directory:
            self.output_dir = directory
            self.statusBar.showMessage(f"Speicherort: {self.output_dir}")
            # Aktiviere den Konvertieren-Button nur wenn auch Dateien ausgewählt sind
            self.convert_button.setEnabled(bool(self.pdf_files))
        else:
            self.statusBar.showMessage("Kein Speicherort ausgewählt")
            self.convert_button.setEnabled(False)
'''
        content = content.rstrip() + new_method + '\n'

    # Aktualisiere die convert_pdfs Methode
    convert_pattern = r'def convert_pdfs\(self\):.*?if not self\.pdf_files:'
    convert_replacement = '''def convert_pdfs(self):
        """Startet den Konvertierungsprozess für die ausgewählten PDF-Dateien"""
        if not self.pdf_files:'''
    
    content = re.sub(convert_pattern, convert_replacement, content, flags=re.DOTALL)

    # Entferne den alten Dialog zur Speicherortauswahl aus convert_pdfs
    old_dialog_pattern = r'output_dir = QFileDialog\.getExistingDirectory\(.*?\n.*?return\n'
    new_check = '''        if not hasattr(self, "output_dir") or not self.output_dir:
            self.statusBar.showMessage("Bitte wählen Sie zuerst einen Speicherort aus.")
            return

        output_dir = self.output_dir\n'''
    content = re.sub(old_dialog_pattern, new_check, content, flags=re.DOTALL)

    # Schreibe die Änderungen zurück in die Datei
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

    print(f"Die Datei {file_path} wurde erfolgreich aktualisiert.")

if __name__ == "__main__":
    # Finde den korrekten Pfad zur main_window.py
    current_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(current_dir, "src", "ui", "main_window.py"),
        os.path.join(current_dir, "PDF_Magic", "src", "ui", "main_window.py"),
        "src/ui/main_window.py",
    ]

    file_path = None
    for path in possible_paths:
        if os.path.exists(path):
            file_path = path
            break

    if file_path:
        update_main_window(file_path)
        print(f"Update erfolgreich durchgeführt für: {file_path}")
    else:
        print("Fehler: main_window.py konnte nicht gefunden werden.")