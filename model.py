import pandas as pd
import h5py
import os
import numpy as np

def check_path_existence(path: str) -> bool:
        return os.path.exists(path)

def get_file_ext(path: str) -> str:
     _, ext = os.path.splitext(path)
     return ext

def get_line(point1: 'Point', point2: 'Point') -> tuple[float, float]:
    grad = (point2.y - point1.y)/(point2.x - point1.x)
    intercept = point1.y - point1.x * grad
    return (grad, intercept)

class Point():
    """Simple point class"""
    x: float | None
    y: float | None
    def __init__(self, x = None, y = None):
        self.x = x
        self.y = y

class Model():
    df: pd.DataFrame | None = None
    data: h5py.File | None = None
    name_column_index: int | None = None
    def __init__(self):
        self.point1 = Point()
        self.point2 = Point()

    def open_hdf5(self, file_name: str):
        self.data = h5py.File(file_name, 'r')

    def open_df(self, file_name: str):
        self.df = pd.read_pickle(file_name)

    def get_sample_rate(self) -> int:
        return self.data['current_data'].attrs['sample_rate']
    
    def get_event_data(self, name: str) -> np.ndarray:
        return self.data[f'\\current_data\\{name}']
    
    def get_df_cols(self, exclude: int | None = None) -> list[str]:
        if exclude is None:
              return list(self.df.columns)
        else:
            return list(self.df.iloc[:exclude].columns) + list(self.df.iloc[(exclude + 1):].columns)
