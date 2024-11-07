# Autor: Leon Gajtner
# Datum: 07.11.2024
# PDF Magic Main
# Version: 1.0.0

import sys
import os
import logging
from datetime import datetime
from PyQt5.QtWidgets import QApplication
from interface import PDFMagicApp

def setup_logging():
    """
    Richtet das Logging-System ein.
    Erstellt einen 'Logs' Ordner und eine Logdatei mit Zeitstempel.
    """
    # Logs Verzeichnis erstellen, falls es nicht existiert
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)

    # Logdatei mit Zeitstempel erstellen
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(logs_dir, f'pdf_magic_{timestamp}.log')

    # Logging konfigurieren
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(sys.stdout)
        ]
    )

def main():
    """
    Hauptfunktion zum Starten der Anwendung.
    """
    try:
        # Logging einrichten
        setup_logging()
        
        # Start der Anwendung loggen
        logging.info("PDF Magic wird gestartet...")
        
        # QApplication erstellen
        app = QApplication(sys.argv)
        
        # Hauptfenster erstellen
        window = PDFMagicApp()
        window.show()
        
        logging.info("PDF Magic wurde erfolgreich gestartet")
        
        # Anwendung ausführen
        sys.exit(app.exec_())
        
    except Exception as e:
        logging.error(f"Fehler beim Starten der Anwendung: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()