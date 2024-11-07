# Autor: Leon Gajtner
# Datum: 07.11.2024
# Version: 2.1
# file_handler.py
# Erstellt durch populate_files.py

import os
import shutil
import logging
from datetime import datetime
from typing import Optional

def create_backup(file_path: str) -> Optional[str]:
    """
    Erstellt eine Sicherungskopie einer Datei.
    
    Args:
        file_path: Pfad zur zu sichernden Datei
        
    Returns:
        Optional[str]: Pfad zur Backup-Datei oder None bei Fehler
    """
    try:
        if not os.path.exists(file_path):
            return None
            
        backup_dir = os.path.join(os.path.dirname(file_path), 'backups')
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
            
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        base_name = os.path.basename(file_path)
        backup_path = os.path.join(backup_dir, f"{timestamp}_{base_name}")
        
        shutil.copy2(file_path, backup_path)
        return backup_path
        
    except Exception as e:
        logging.error(f"Fehler beim Erstellen des Backups: {str(e)}")
        return None

def cleanup_temp_files(directory: str, prefix: str = "temp_", older_than: int = 24):
    """
    Bereinigt temporäre Dateien in einem bestimmten Verzeichnis.

    Args:
        directory (str): Das zu bereinigende Verzeichnis
        prefix (str): Präfix der zu löschenden temporären Dateien
        older_than (int): Lösche Dateien, die älter als diese Anzahl von Stunden sind

    Returns:
        int: Anzahl der gelöschten Dateien
    """
    deleted_count = 0
    current_time = datetime.now()
    try:
        for filename in os.listdir(directory):
            if filename.startswith(prefix):
                file_path = os.path.join(directory, filename)
                file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if (current_time - file_modified_time).total_seconds() > older_than * 3600:
                    os.remove(file_path)
                    deleted_count += 1
                    logging.info(f"Gelöschte temporäre Datei: {file_path}")
    except Exception as e:
        logging.error(f"Fehler beim Bereinigen temporärer Dateien: {str(e)}")
    return deleted_count

def get_file_info(file_path: str) -> dict:
    """
    Gibt Informationen über eine Datei zurück.

    Args:
        file_path (str): Pfad zur Datei

    Returns:
        dict: Ein Dictionary mit Dateiinformationen
    """
    try:
        stat_info = os.stat(file_path)
        return {
            "name": os.path.basename(file_path),
            "size": stat_info.st_size,
            "created": datetime.fromtimestamp(stat_info.st_ctime),
            "modified": datetime.fromtimestamp(stat_info.st_mtime),
            "accessed": datetime.fromtimestamp(stat_info.st_atime),
        }
    except Exception as e:
        logging.error(f"Fehler beim Abrufen von Dateiinformationen für {file_path}: {str(e)}")
        return {}