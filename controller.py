from PyQt6.QtWidgets import QFileDialog
from model import Model, check_path_existence, get_file_ext, Point, get_line
from view import MainWindow, ErrorDialog
import numpy as np
import logging
import matplotlib as mpl

def open_file_dialog(filt: str):
    qfd = QFileDialog()
    path = None
    f = qfd.getOpenFileName(qfd, "Select File", path, filt)
    return f[0]

class Controller():
    free_select: bool = False
    event_point = None
    split_point1: Point | None = None
    split_point1_artist = None
    split_point2: Point | None = None
    split_point2_artist = None
    split_line_artist = None
    def __init__(self, version = "Default"):
        self.version = version
        self.model = Model()
        self.view = MainWindow(self.version)

        self.reset_view_state()
        self._initialise_buttons()

    #Initialisation

    def reset_model(self):
        self.model = Model()

    def reset_view_state(self):
        #Buttons that begin enabled
        self.view.chooseDataButton.setEnabled(True)
        self.view.chooseDfButton.setEnabled(True)
        self.view.startButton.setEnabled(True)
        self.view.dataLocation.setText("")
        self.view.dataLocation.setReadOnly(False)
        self.view.dataframeLocation.setText("")
        self.view.dataframeLocation.setReadOnly(False)
        self.view.saveSelectionButton.setEnabled(False)
        #Buttons that begin disabled
        self.view.chooseFirstButton.setEnabled(False)
        self.view.chooseSecButton.setEnabled(False)
        self.view.chooseRegionButton.setEnabled(False)
        self.view.resetAllButton.setEnabled(False)
        self.view.saveSelectionButton.setEnabled(False)
        self.view.lockNameButton.setEnabled(False)
        self.view.updatePlotButton.setEnabled(False)
        #Comboboxes that begin disabled
        self.view.xBox.setEnabled(False)
        self.view.xBox.clear()
        self.view.yBox.setEnabled(False)
        self.view.yBox.clear()
        self.view.nameBox.setEnabled(False)
        self.view.nameBox.clear()
        #Plots
        self.view.scatterPlot.clear_axes()
        self.view.eventPlot.clear_axes()
        #Reset variables
        self.event_point = None
        self.free_select = False
        self.split_point1 = None
        self.split_point2 = None
        self.split_point1_artist = None
        self.split_point2_artist = None
        self.split_line_artist = None
        

    def _initialise_buttons(self):
        self.view.startButton.clicked.connect(self.start)
        self.view.chooseDataButton.clicked.connect(self.select_data)
        self.view.chooseDfButton.clicked.connect(self.select_dataframe)
        self.view.newButton.clicked.connect(self.new)
        self.view.lockNameButton.clicked.connect(self.lock_names)
        self.view.updatePlotButton.clicked.connect(self.update_scatter_plot)
        self.scatter_cid = self.view.scatterPlot.canvas.mpl_connect('button_press_event', self.select_event)
        self.view.chooseFirstButton.clicked.connect(self.choose_first)
        self.view.chooseSecButton.clicked.connect(self.choose_second)
        self.view.resetAllButton.clicked.connect(self.reset_all_choices)
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
        self.view.nameBox.setEnabled(True)
        self.view.nameBox.addItems(cols)
        self.view.lockNameButton.setEnabled(True)

    def new(self):
        self.reset_model()
        self.reset_view_state()

    def select_data(self):
        path = open_file_dialog('HDF5 (*.hdf5)')
        logging.info(f"{path} selected as data source.")
        self.view.dataLocation.setText(path)

    def select_dataframe(self):
        path = open_file_dialog('PKL File (*.pkl)')
        logging.info(f"{path} selected as dataframe.")
        self.view.dataframeLocation.setText(path)
        
    def lock_names(self):
        index = self.view.nameBox.currentIndex()
        self.view.lockNameButton.setEnabled(False)
        self.view.nameBox.setEnabled(False)
        self.view.chooseFirstButton.setEnabled(True)
        self.view.chooseSecButton.setEnabled(True)

        #Populate Control Comboboxes
        other_cols = self.model.get_df_cols(exclude = index)
        self.view.xBox.addItems(other_cols)
        self.view.xBox.setEnabled(True)
        self.view.yBox.addItems(other_cols)
        self.view.yBox.setEnabled(True)
        self.view.updatePlotButton.setEnabled(True)

    def update_scatter_plot(self):
        #Check selected parameters
        x_parameter = self.view.xBox.currentText()
        y_parameter = self.view.yBox.currentText()

        #Fetch data
        try:
            x_data = np.array(self.model.df[x_parameter])
            y_data = np.array(self.model.df[y_parameter])
        except KeyError:
            logging.info(f"Failed to fetch data for parameters {x_parameter}, {y_parameter}...")
            return None

        #Reset plots
        self.view.scatterPlot.clear_axes()
        self.view.eventPlot.clear_axes()

        #Reset Variables
        self.event_point = None
        self.free_select = False
        self.split_point1 = None
        self.split_point2 = None
        self.split_point1_artist = None
        self.split_point2_artist = None
        self.split_line_artist = None

        #Plot new scatter plot
        logging.info(f"Plotting {len(x_data)} points...")
        self.view.scatterPlot.scatter(x_data, y_data, alpha = 0.1)
        logging.info("Done plotting.")

        #Update toolbar
        self.view.scatterPlot.update_toolbar()
        self.view.eventPlot.update_toolbar()

        #Enable free select
        self.free_select = True

    def plot_event(self, name):
        event_data = self.model.get_event_data(name)
        t_data = np.arange(len(event_data))/self.model.get_sample_rate()

        self.view.eventPlot.clear_axes()
        self.view.eventPlot.label_x("Time /s")
        self.view.eventPlot.label_y("Current /nA")

        self.view.eventPlot.plot(t_data, event_data)
        self.view.eventPlot.update_toolbar()

    def select_event(self, event):
        #Miss all of this if app is not in free select mode
        if not self.free_select:
            return None
        

        logging.info(f"Click detected at {event.xdata}, {event.ydata} with free select on.")
        click = Point(event.xdata, event.ydata)

        #Picking nearest event (if there is one)
        x_parameter = self.view.xBox.currentText()
        y_parameter = self.view.yBox.currentText()
        picked = self.model.choose_event(click, (x_parameter, y_parameter))

        #Check whether any event was found
        if picked is None:
            logging.info("No valid events in vicinity of click.")
            return None
        else:
            logging.info(f"Event named '{picked[self.view.nameBox.currentText()]}' selected, fetching data...")

        #Plot event
        event_name = picked[self.view.nameBox.currentText()]
        self.plot_event(event_name)

        #Remove any old points
        if self.event_point is not None:
            point = self.event_point.pop(0)
            point.remove()

        #Plot marker for selected event
        event_point = Point(picked[x_parameter], picked[y_parameter])
        self.event_point = self.view.scatterPlot.plot_point(event_point, c='r', marker = 'o')

    def choose_first(self):
        #TODO this spaghetti could be later replaced with a context manager
        #Disable everything and disconnect free_select
        self.view.scatterPlot.canvas.mpl_disconnect(self.scatter_cid)
        self.view.updatePlotButton.setEnabled(False)
        self.view.chooseFirstButton.setEnabled(False)
        self.view.chooseSecButton.setEnabled(False)
        self.view.chooseRegionButton.setEnabled(False)
        self.view.resetAllButton.setEnabled(False)
        self.view.saveSelectionButton.setEnabled(False)
        self.view.xBox.setEnabled(False)
        self.view.yBox.setEnabled(False)

        self.scatter_cid = self.view.scatterPlot.canvas.mpl_connect('button_press_event',self._click_first)

    def _click_first(self,event):
        self.split_point1 = Point(event.xdata, event.ydata)

        if self.split_point1_artist is not None:
            point = self.split_point1_artist.pop(0)
            point.remove()
        self.split_point1_artist = self.view.scatterPlot.plot_point(self.split_point1, c='g', marker = 'o')

        self.view.chooseFirstButton.setEnabled(True)
        self.view.chooseSecButton.setEnabled(True)
        self.view.chooseRegionButton.setEnabled(True)
        self.view.resetAllButton.setEnabled(True)
        self.view.saveSelectionButton.setEnabled(True)
        self.view.xBox.setEnabled(True)
        self.view.yBox.setEnabled(True)

        self.scatter_cid = self.view.scatterPlot.canvas.mpl_connect('button_press_event', self.select_event)

    def choose_second(self):
        #TODO this spaghetti could be later replaced with a context manager
        #Disable everything and disconnect free_select
        self.view.scatterPlot.canvas.mpl_disconnect(self.scatter_cid)
        self.view.updatePlotButton.setEnabled(False)
        self.view.chooseFirstButton.setEnabled(False)
        self.view.chooseSecButton.setEnabled(False)
        self.view.chooseRegionButton.setEnabled(False)
        self.view.resetAllButton.setEnabled(False)
        self.view.saveSelectionButton.setEnabled(False)
        self.view.xBox.setEnabled(False)
        self.view.yBox.setEnabled(False)

        self.scatter_cid = self.view.scatterPlot.canvas.mpl_connect('button_press_event', self._click_second)

    def _click_second(self,event):
        self.split_point2 = Point(event.xdata, event.ydata)

        if self.split_point2_artist is not None:
            point = self.split_point2_artist.pop(0)
            point.remove()
        self.split_point2_artist = self.view.scatterPlot.plot_point(self.split_point2, c='g', marker = 'o')

        self.view.updatePlotButton.setEnabled(True)
        self.view.chooseFirstButton.setEnabled(True)
        self.view.chooseSecButton.setEnabled(True)
        self.view.chooseRegionButton.setEnabled(True)
        self.view.resetAllButton.setEnabled(True)
        self.view.saveSelectionButton.setEnabled(True)
        self.view.xBox.setEnabled(True)
        self.view.yBox.setEnabled(True)

        self.scatter_cid = self.view.scatterPlot.canvas.mpl_connect('button_press_event', self.select_event)


    def check_line(self):
        if self.split_point1 is not None and self.split_point2 is not None:
            line = get_line(self.split_point1, self.split_point2)
            self.split_line_artist = self.view.scatterPlot.plot()

    def reset_all_choices(self):
        if self.split_point1_artist is not None:
            point1 = self.split_point1_artist.pop(0)
            point1.remove()
        if self.split_point2_artist is not None:
            point2 = self.split_point2_artist.pop(0)
            point2.remove()
        if self.split_line_artist is not None:
            line = self.split_line_artist.pop(0)
            line.remove()
        self.split_point1 = None
        self.split_point2 = None
        self.split_point1_artist = None
        self.split_point2_artist = None
        self.split_line_artist = None

            


