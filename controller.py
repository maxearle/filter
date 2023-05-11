from PyQt6.QtWidgets import QFileDialog
from model import Model, check_path_existence, get_file_ext
from view import MainWindow, ErrorDialog

def open_file_dialog(filt: str):
    qfd = QFileDialog()
    path = None
    f = qfd.getOpenFileName(qfd, "Select File", path, filt)
    return f

class Controller():
    name_col: str
    def __init__(self, version = "Default"):
        self.model = Model()
        self.view = MainWindow(version = version)

        self._initialise_buttons()

    #Initialisation

    def _initialise_buttons(self):
        self.view.startButton.clicked.connect(self.start)
        ...

    def start(self):
        #Checking path/file validity
        data_location = self.view.dataLocation.text()
        dataframe_location = self.view.dataframeLocation.text()
        if not check_path_existence(data_location):
            ErrorDialog("Selected data path does not exist!")
            return None
        if not get_file_ext(data_location) == '.hdf5':
            ErrorDialog("Selected file does not have extension '.hdf5'.")
            return None
        if not check_path_existence(dataframe_location):
            ErrorDialog("Selected dataframe path does not exist!")
            return None
        if not get_file_ext(data_location) == '.hdf5':
            ErrorDialog("Selected file does not have extension '.pkl'.")
            return None
        
        #Opening files and adding to model
        self.model.open_hdf5(data_location)
        self.model.open_df(dataframe_location)

        #Locking all fields and other buttons except 'New Dataset'
        self.view.startButton.setEnabled(False)
        self.view.chooseDfButton.setEnabled(False)
        self.view.dataframeLocation.setReadOnly(True)
        self.view.chooseDataButton.setEnabled(False)
        self.view.dataLocation.setReadOnly(True)

        #Populating Name Column Selection Box
        cols = self.model.get_df_cols()
        self.view.nameBox.addItems(cols)
