import os

# Verzeichnisstruktur
directories = [
    "PDF_Magic"
]

# Dateien, die erstellt werden sollen (ohne Inhalt)
files = [
    "PDF_Magic/main.py",
    "PDF_Magic/interface.py",
    "PDF_Magic/utils.py",
    "PDF_Magic/style.py",
    "PDF_Magic/requirements.txt"
]

# Verzeichnis erstellen
for directory in directories:
    os.makedirs(directory, exist_ok=True)

# Leere Dateien erstellen
for file_path in files:
    with open(file_path, 'w') as file:
        pass  # Leere Datei erstellen

print("Verzeichnis und leere Dateien wurden erstellt!")