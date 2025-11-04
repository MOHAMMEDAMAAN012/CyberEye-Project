import sys
import os
import threading
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QFileDialog,
    QProgressBar, QMessageBox
)
from PySide6.QtCore import Qt, Signal, QObject
from core_engine import scan_directory, DEFAULT_SIGNATURES

APP_NAME = "CyberEye"

class ScanSignals(QObject):
    progress = Signal(int, int)
    finished = Signal(list)

class ScannerThread(threading.Thread):
    def __init__(self, directory, signatures, signals):
        super().__init__(daemon=True)
        self.directory = directory
        self.signatures = signatures
        self.signals = signals

    def run(self):
        def update_progress(scanned, total):
            self.signals.progress.emit(scanned, total)
        infected = scan_directory(self.directory, self.signatures, update_progress)
        self.signals.finished.emit(infected)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{APP_NAME} - Modern Antivirus")
        self.resize(750, 480)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title
        title = QLabel(f"<h2 style='color:#00BCD4;'>{APP_NAME}</h2>")
        title.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(title)

        # Directory selection
        h1 = QHBoxLayout()
        self.dir_label = QLabel("No folder selected")
        self.dir_label.setMinimumWidth(400)
        choose_btn = QPushButton("Browse Folder")
        choose_btn.clicked.connect(self.choose_folder)
        h1.addWidget(self.dir_label)
        h1.addWidget(choose_btn)
        self.layout.addLayout(h1)

        # Buttons
        h2 = QHBoxLayout()
        self.scan_btn = QPushButton("Start Scan")
        self.scan_btn.clicked.connect(self.start_scan)
        self.scan_btn.setEnabled(False)
        self.stop_btn = QPushButton("Stop Scan")
        self.stop_btn.setEnabled(False)
        h2.addWidget(self.scan_btn)
        h2.addWidget(self.stop_btn)
        self.layout.addLayout(h2)

        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.layout.addWidget(self.progress_bar)
        self.status_label = QLabel("Idle")
        self.layout.addWidget(self.status_label)

        # Results
        self.results = QListWidget()
        self.layout.addWidget(self.results)

        self.selected_dir = ""
        self.signals = None
        self.thread = None

    def choose_folder(self):
        d = QFileDialog.getExistingDirectory(self, "Select Folder", os.path.expanduser("~"))
        if d:
            self.selected_dir = d
            self.dir_label.setText(d)
            self.scan_btn.setEnabled(True)

    def start_scan(self):
        if not self.selected_dir:
            QMessageBox.warning(self, "No Folder", "Please choose a folder to scan.")
            return

        self.results.clear()
        self.progress_bar.setValue(0)
        self.status_label.setText("Scanning...")
        self.scan_btn.setEnabled(False)
        self.stop_btn.setEnabled(False)  # stop not implemented yet

        self.signals = ScanSignals()
        self.signals.progress.connect(self.update_progress)
        self.signals.finished.connect(self.scan_done)

        self.thread = ScannerThread(self.selected_dir, DEFAULT_SIGNATURES, self.signals)
        self.thread.start()

    def update_progress(self, scanned, total):
        percent = int((scanned / total) * 100) if total else 100
        self.progress_bar.setValue(percent)
        self.status_label.setText(f"Scanned {scanned}/{total}")

    def scan_done(self, infected):
        self.scan_btn.setEnabled(True)
        if infected:
            self.status_label.setText(f"Found {len(infected)} infected files!")
            for f in infected:
                self.results.addItem(f)
        else:
            self.status_label.setText("No infected files found.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec())
