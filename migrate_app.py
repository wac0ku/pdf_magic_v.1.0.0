# migrate_app.py

import os
import shutil
import re
from typing import Dict, List
from datetime import datetime

def ensure_directory(path: str):
    """Stellt sicher, dass ein Verzeichnis existiert"""
    if not os.path.exists(path):
        os.makedirs(path)

def update_import_statements(content: str, import_mappings: Dict[str, str]) -> str:
    """Aktualisiert Import-Statements basierend auf der neuen Struktur"""
    for old_import, new_import in import_mappings.items():
        # Ersetze direkte Imports
        content = re.sub(
            f"from {old_import} import",
            f"from {new_import} import",
            content
        )
        # Ersetze einfache Imports
        content = re.sub(
            f"import {old_import}",
            f"import {new_import}",
            content
        )
    return content

def migrate_files():
    """Migriert die bestehenden Dateien in die neue Struktur"""
    # Basis-Verzeichnisse
    src_dir = "PDF_Magic/src"
    core_dir = os.path.join(src_dir, "core")
    ui_dir = os.path.join(src_dir, "ui")
    utils_dir = os.path.join(src_dir, "utils")

    # Stelle sicher, dass die Verzeichnisse existieren
    for directory in [core_dir, ui_dir, utils_dir]:
        ensure_directory(directory)

    # Import-Mappings für die neue Struktur
    import_mappings = {
        'enhanced_drag_drop': 'src.ui.widgets',
        'style': 'src.utils.style',
        'utils': 'src.core.utils',
        'interface': 'src.ui.main_window'
    }

    # Dateizuordnungen für die Migration
    file_mappings = {
        'main.py': 'PDF_Magic/main.py',
        'interface.py': os.path.join(ui_dir, 'main_window.py'),
        'enhanced_drag_drop.py': os.path.join(ui_dir, 'widgets.py'),
        'style.py': os.path.join(utils_dir, 'style.py'),
        'utils.py': os.path.join(core_dir, 'utils.py')
    }

    try:
        # Kopiere und aktualisiere jede Datei
        for source_file, dest_path in file_mappings.items():
            if os.path.exists(source_file):
                print(f"Migriere {source_file} nach {dest_path}")
                
                # Lese den Inhalt der Quelldatei
                with open(source_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Aktualisiere die Imports
                content = update_import_statements(content, import_mappings)

                # Erstelle das Zielverzeichnis, falls es nicht existiert
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Schreibe die aktualisierte Datei
                with open(dest_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                print(f"Erfolgreich migriert: {source_file}")
            else:
                print(f"Warnung: Quelldatei {source_file} nicht gefunden")

        # Erstelle __init__.py Dateien
        init_files = [
            os.path.join(src_dir, "__init__.py"),
            os.path.join(core_dir, "__init__.py"),
            os.path.join(ui_dir, "__init__.py"),
            os.path.join(utils_dir, "__init__.py")
        ]

        for init_file in init_files:
            if not os.path.exists(init_file):
                with open(init_file, 'w', encoding='utf-8') as f:
                    f.write("# Automatisch generierte __init__.py\n")

        print("\nMigration erfolgreich abgeschlossen!")
        print("\nBitte überprüfen Sie die Import-Statements in den migrierten Dateien.")
        print("Möglicherweise müssen einige relative Imports angepasst werden.")

    except Exception as e:
        print(f"Fehler bei der Migration: {str(e)}")

def update_main_imports():
    """Aktualisiert die Imports in der main.py speziell"""
    main_file = "PDF_Magic/main.py"
    if os.path.exists(main_file):
        with open(main_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Aktualisiere die Imports für main.py
        content = content.replace(
            "from interface import PDFMagicApp",
            "from src.ui.main_window import PDFMagicApp"
        )

        with open(main_file, 'w', encoding='utf-8') as f:
            f.write(content)
        print("main.py Imports aktualisiert")

def create_readme():
    """Erstellt eine README.md mit Installationsanweisungen"""
    readme_content = """# PDF Magic
        Eine Python-Anwendung zur Konvertierung von PDF zu DOCX.

        ## Installation

        1. Klonen Sie das Repository: git clone <repository-url>
        
        2. Installieren Sie die Abhängigkeiten:
        
        3. Starten Sie die Anwendung:
        
    ## Projektstruktur
        
## Entwickelt von
Leon Gajtner
"""

    with open("PDF_Magic/README.md", 'w', encoding='utf-8') as f:
        f.write(readme_content)

def main():
    """Hauptfunktion zur Migration der Anwendung"""
    try:
        print("Starte Migration der PDF Magic Anwendung...")
        
        # Erstelle Backup des bestehenden PDF_Magic Verzeichnisses
        if os.path.exists("PDF_Magic"):
            backup_name = f"PDF_Magic_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            shutil.copytree("PDF_Magic", backup_name)
            print(f"Backup erstellt: {backup_name}")

        # Führe die Migration durch
        migrate_files()
        
        # Aktualisiere main.py Imports
        update_main_imports()
        
        # Erstelle README
        create_readme()
        
        print("\nMigration abgeschlossen!")
        print("Bitte testen Sie die Anwendung und überprüfen Sie alle Import-Statements.")
        
    except Exception as e:
        print(f"Fehler bei der Migration: {str(e)}")

if __name__ == "__main__":
    main()
