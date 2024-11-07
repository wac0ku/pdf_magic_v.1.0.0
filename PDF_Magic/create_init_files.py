# Autor: Leon Gajtner
# Datum: 07.11.2024
# Version: 2.1
# create_init_files.py

import os
from datetime import datetime

def create_init_files(root_dir):
    """
    Erstellt oder aktualisiert __init__.py Dateien in allen Unterverzeichnissen des angegebenen Verzeichnisses.
    """
    for dirpath, dirnames, filenames in os.walk(root_dir):
        init_path = os.path.join(dirpath, '__init__.py')
        python_files = [file for file in filenames if file.endswith('.py') and file != '__init__.py']
        
        with open(init_path, 'w', encoding='utf-8') as f:
            f.write(f"# Autor: Leon Gajtner\n")
            f.write(f"# Datum: {datetime.now().strftime('%d.%m.%Y')}\n")
            f.write(f"# Version: 2.1\n")
            f.write(f"# Automatisch generierte __init__.py für {os.path.basename(dirpath)}\n\n")

            # Importiere alle Python-Module im aktuellen Verzeichnis
            if python_files:
                f.write("# Importiere Module\n")
                for py_file in python_files:
                    module_name = os.path.splitext(py_file)[0]
                    f.write(f"from .{module_name} import *\n")
                f.write("\n")

            # Füge spezifische Importe basierend auf dem Verzeichnisnamen hinzu
            if 'core' in dirpath.lower():
                f.write("# Core-spezifische Importe\n")
                f.write("from PyPDF2 import PdfReader, PdfWriter\n")
                f.write("from docx import Document\n\n")
            elif 'ui' in dirpath.lower():
                f.write("# UI-spezifische Importe\n")
                f.write("from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit, QProgressBar\n")
                f.write("from PyQt5.QtCore import Qt, QThread, pyqtSignal\n")
                f.write("from PyQt5.QtGui import QFont\n\n")
            elif 'utils' in dirpath.lower():
                f.write("# Utility-spezifische Importe\n")
                f.write("import logging\n")
                f.write("import json\n")
                f.write("import os\n\n")

            # Füge eine __all__ Liste hinzu
            if python_files:
                f.write("__all__ = [\n")
                for py_file in python_files:
                    module_name = os.path.splitext(py_file)[0]
                    f.write(f"    '{module_name}',\n")
                f.write("]\n")

        print(f"Erstellt/Aktualisiert: {init_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_directory = script_dir  # Verwende das aktuelle Verzeichnis als Wurzelverzeichnis
    
    if not os.path.exists(root_directory):
        print(f"Fehler: Das Verzeichnis {root_directory} existiert nicht.")
    else:
        create_init_files(root_directory)
        print("Erstellung/Aktualisierung der __init__.py Dateien abgeschlossen.")