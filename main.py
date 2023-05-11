from controller import Controller
import sys
from PyQt6.QtWidgets import QApplication
import logging

if __name__ == '__main__':
    version = 'pre-alpha'
    logging.basicConfig(level = logging.INFO)
    app = QApplication(sys.argv)
    ctrlr = Controller(version)
    app.exec()