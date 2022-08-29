import os
import numpy as np
import pandas as pd
import sys

class DataLogger():
    def __init__(self, file_name) -> None:
        np.set_printoptions(threshold=sys.maxsize)

        self.file_name = file_name
        self.logged_data = None
        
        self._prepareFile()

    def _prepareFile(self):
        if os.path.isfile(os.path.join("outputs", self.file_name)):
            print("File exists, loading previous data.")
            self.logged_data = pd.read_csv(os.path.join("outputs", self.file_name), sep=";")
        else:
            print("Creating new training file")
            self.logged_data = None
    
    def logData(self, frame, *data_dicts):
        data = {}
        
        for temp_data_dict in data_dicts:
            data = {**data, **temp_data_dict}

        current_row = pd.DataFrame(data, index=[0])
        current_row = pd.concat([current_row, pd.DataFrame([frame])], axis=1)
        print(current_row)
        # Initialize columns if first time
        if self.logged_data is None:
            self.logged_data = pd.DataFrame(current_row, index=[0])
        else:
            self.logged_data = pd.concat([self.logged_data, current_row], ignore_index=True)
        
        if (len(self.logged_data) % 1000 == 0):
            self.logged_data.to_csv(os.path.join("outputs", self.file_name), sep=";")
            
            