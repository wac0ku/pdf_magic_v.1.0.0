# validator.py
# Erstellt durch populate_files.py

import os
import shutil
from typing import Optional
from PyPDF2 import PdfReader


def validate_pdf_file(file_path: str) -> Optional[str]:
    """
    Überprüft, ob die angegebene Datei eine gültige PDF-Datei ist.
    
    Args:
        file_path: Pfad zur zu überprüfenden Datei
        
    Returns:
        Optional[str]: Fehlermeldung wenn die Datei ungültig ist, sonst None
    """
    try:
        if not os.path.exists(file_path):
            return f"Die Datei {file_path} existiert nicht."
        
        if not os.access(file_path, os.R_OK):
            return f"Keine Leserechte für {file_path}."
        
        if not file_path.lower().endswith('.pdf'):
            return f"Die Datei {file_path} ist keine PDF-Datei."
        
        # Überprüfe die Dateigröße (max. 100MB)
        file_size = os.path.getsize(file_path)
        if file_size > 100 * 1024 * 1024:  # 100MB in Bytes
            return f"Die Datei {file_path} ist zu groß (max. 100MB erlaubt)."
        
        # Versuche die PDF-Datei zu öffnen um ihre Gültigkeit zu prüfen
        with open(file_path, 'rb') as file:
            try:
                PdfReader(file)
            except Exception:
                return f"Die Datei {file_path} ist keine gültige PDF-Datei."
        
        return None
        
    except Exception as e:
        return f"Fehler bei der Überprüfung von {file_path}: {str(e)}"

def validate_output_directory(directory: str) -> Optional[str]:
    """
    Überprüft, ob das Ausgabeverzeichnis gültig und beschreibbar ist.
    
    Args:
        directory: Pfad zum zu überprüfenden Verzeichnis
        
    Returns:
        Optional[str]: Fehlermeldung wenn das Verzeichnis ungültig ist, sonst None
    """
    try:
        if not directory:
            return "Kein Ausgabeverzeichnis angegeben."
        
        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except Exception as e:
                return f"Konnte Ausgabeverzeichnis nicht erstellen: {str(e)}"
        
        if not os.access(directory, os.W_OK):
            return f"Keine Schreibrechte im Verzeichnis {directory}."
        
        return None
        
    except Exception as e:
        return f"Fehler bei der Überprüfung des Verzeichnisses: {str(e)}"

def check_disk_space(directory: str, required_space: int) -> Optional[str]:
    """
    Überprüft, ob genügend Speicherplatz verfügbar ist.
    
    Args:
        directory: Zu überprüfendes Verzeichnis
        required_space: Benötigter Speicherplatz in Bytes
        
    Returns:
        Optional[str]: Fehlermeldung wenn nicht genug Speicherplatz vorhanden ist, sonst None
    """
    try:
        total, used, free = shutil.disk_usage(directory)
        if free < required_space:
            free_mb = free / (1024 * 1024)
            required_mb = required_space / (1024 * 1024)
            return (f"Nicht genügend Speicherplatz verfügbar. "
                   f"Verfügbar: {free_mb:.1f}MB, Benötigt: {required_mb:.1f}MB")
        return None
    except Exception as e:
        return f"Fehler bei der Überprüfung des Speicherplatzes: {str(e)}"