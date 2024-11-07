# Autor: Leon Gajtner
# Datum: 07.11.2024
# Version: 2.1
# update_version.py

import os
import re
from datetime import datetime

def update_version_in_file(file_path: str, new_version: str = "2.2"):
    """Aktualisiert die Versionsnummer in einer Datei"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Aktualisiere bestehende Versionsangaben
        version_pattern = r'# Version: \d+\.\d+(\.\d+)?'
        if re.search(version_pattern, content):
            content = re.sub(version_pattern, f'# Version: {new_version}', content)
        else:
            # Füge Versionsinfo zum Dateikopf hinzu
            header = f"""# Autor: Leon Gajtner
# Datum: {datetime.now().strftime('%d.%m.%Y')}
# Version: {new_version}
"""
            content = header + content

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"Version aktualisiert in: {file_path}")
        
    except Exception as e:
        print(f"Fehler beim Aktualisieren von {file_path}: {str(e)}")

def find_python_files(directory: str) -> list:
    """Findet alle Python-Dateien in einem Verzeichnis und seinen Unterverzeichnissen"""
    python_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

def main():
    """Hauptfunktion zum Aktualisieren der Versionsnummern"""
    try:
        # Basis-Verzeichnis (PDF_Magic)
        base_dir = "PDF_Magic"
        
        # Finde alle Python-Dateien
        python_files = find_python_files(base_dir)
        
        if not python_files:
            print(f"Keine Python-Dateien in {base_dir} gefunden.")
            return

        # Aktualisiere die Version in jeder Datei
        for file_path in python_files:
            update_version_in_file(file_path)

        print("\nVersionsaktualisierung abgeschlossen!")
        print(f"Insgesamt {len(python_files)} Dateien aktualisiert.")
        
        # Erstelle eine Versions-Log-Datei
        log_content = f"""# PDF Magic Versions-Log
Letzte Aktualisierung: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}
Version: 2.1

Aktualisierte Dateien:
{chr(10).join(['- ' + os.path.relpath(f, base_dir) for f in python_files])}
"""
        
        with open(os.path.join(base_dir, "VERSION.md"), 'w', encoding='utf-8') as f:
            f.write(log_content)
        
        print("\nVersions-Log erstellt: VERSION.md")

    except Exception as e:
        print(f"Fehler bei der Versionsaktualisierung: {str(e)}")

if __name__ == "__main__":
    main()