from controller import Controller
import sys
from PyQt6.QtWidgets import QApplication

if __name__ == '__main__':
    version = 'pre-alpha'
    app = QApplication(sys.argv)
    ctrlr = Controller(version)
    app.exec()