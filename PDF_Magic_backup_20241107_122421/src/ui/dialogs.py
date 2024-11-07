# dialogs.py
# Erstellt durch populate_files.py

from PyQt5.QtWidgets import QMessageBox


def show_error_message(message: str):
    """Zeigt eine Fehlermeldung in einem Dialogfenster an."""
    error_box = QMessageBox()
    error_box.setIcon(QMessageBox.Critical)
    error_box.setText("Ein Fehler ist aufgetreten")
    error_box.setInformativeText(message)
    error_box.setWindowTitle("Fehler")
    error_box.exec_()