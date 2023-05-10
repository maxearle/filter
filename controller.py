from PyQt6.QtWidgets import QFileDialog

def open_file_dialog(filt: str):
    qfd = QFileDialog()
    path = None
    f = qfd.getOpenFileName(qfd, "Select File", path, filt)
    return f