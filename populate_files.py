# populate_files.py

import os
import re
from typing import Dict, List

def read_source_file(file_path: str) -> str:
    """Liest eine Quelldatei ein"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Fehler beim Lesen von {file_path}: {str(e)}")
        return ""

def extract_class_or_function(content: str, identifier: str) -> str:
    """Extrahiert eine Klasse oder Funktion aus dem Quellcode"""
    # Sucht nach Klassen- oder Funktionsdefinitionen
    pattern = rf"(class|def)\s+{identifier}[\s\S]*?(?=\n\n(?:class|def)|$)"
    match = re.search(pattern, content)
    if match:
        return match.group(0)
    return ""

def populate_converter_py():
    """Befüllt converter.py mit relevanten Code-Segmenten"""
    content = read_source_file('utils.py')
    
    converter_content = """# converter.py
# Erstellt durch populate_files.py

import os
import logging
from datetime import datetime
from typing import List
from PyPDF2 import PdfReader
from docx import Document
from PyQt5.QtCore import QObject, pyqtSignal

"""
    # ConversionWorker Klasse extrahieren
    conversion_worker = extract_class_or_function(content, "ConversionWorker")
    converter_content += conversion_worker

    # convert_pdf_to_docx Funktion extrahieren
    convert_func = extract_class_or_function(content, "convert_pdf_to_docx")
    
    return converter_content

def populate_file_handler_py():
    """Befüllt file_handler.py mit relevanten Code-Segmenten"""
    content = read_source_file('utils.py')
    
    file_handler_content = """# file_handler.py
# Erstellt durch populate_files.py

import os
import shutil
import logging
from datetime import datetime
"""
    
    functions = [
        "create_backup",
        "cleanup_temp_files",
        "get_file_info"
    ]
    
    for func in functions:
        extracted = extract_class_or_function(content, func)
        if extracted:
            file_handler_content += "\n\n" + extracted
            
    return file_handler_content

def populate_validator_py():
    """Befüllt validator.py mit relevanten Code-Segmenten"""
    content = read_source_file('utils.py')
    
    validator_content = """# validator.py
# Erstellt durch populate_files.py

import os
from typing import Optional
from PyPDF2 import PdfReader
"""
    
    functions = [
        "validate_pdf_file",
        "validate_output_directory",
        "check_disk_space"
    ]
    
    for func in functions:
        extracted = extract_class_or_function(content, func)
        if extracted:
            validator_content += "\n\n" + extracted
            
    return validator_content

def populate_main_window_py():
    """Befüllt main_window.py mit relevanten Code-Segmenten"""
    content = read_source_file('interface.py')
    
    main_window_content = """# main_window.py
# Erstellt durch populate_files.py

import os
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QThread
from PyQt5.QtGui import QFont
"""
    
    pdf_magic_app = extract_class_or_function(content, "PDFMagicApp")
    if pdf_magic_app:
        main_window_content += "\n\n" + pdf_magic_app
        
    return main_window_content

def populate_dialogs_py():
    """Befüllt dialogs.py mit relevanten Code-Segmenten"""
    content = read_source_file('utils.py')
    
    dialogs_content = """# dialogs.py
# Erstellt durch populate_files.py

from PyQt5.QtWidgets import QMessageBox
"""
    
    functions = [
        "show_error_message",
        "show_success_dialog"
    ]
    
    for func in functions:
        extracted = extract_class_or_function(content, func)
        if extracted:
            dialogs_content += "\n\n" + extracted
            
    return dialogs_content

def write_file(file_path: str, content: str):
    """Schreibt Inhalt in eine Datei"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Datei erfolgreich erstellt: {file_path}")
    except Exception as e:
        print(f"Fehler beim Schreiben von {file_path}: {str(e)}")

def main():
    """Hauptfunktion zum Befüllen der Dateien"""
    try:
        base_dir = "PDF_Magic/src"
        
        # Converter
        converter_path = os.path.join(base_dir, "core/converter.py")
        write_file(converter_path, populate_converter_py())
        
        # File Handler
        file_handler_path = os.path.join(base_dir, "core/file_handler.py")
        write_file(file_handler_path, populate_file_handler_py())
        
        # Validator
        validator_path = os.path.join(base_dir, "core/validator.py")
        write_file(validator_path, populate_validator_py())
        
        # Main Window
        main_window_path = os.path.join(base_dir, "ui/main_window.py")
        write_file(main_window_path, populate_main_window_py())
        
        # Dialogs
        dialogs_path = os.path.join(base_dir, "ui/dialogs.py")
        write_file(dialogs_path, populate_dialogs_py())
        
        print("Alle Dateien wurden erfolgreich mit Code befüllt!")
        
    except Exception as e:
        print(f"Fehler beim Befüllen der Dateien: {str(e)}")

if __name__ == "__main__":
    main()