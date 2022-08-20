import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2

from dataReader import DataReader

class ModelTrainer():
    def __init__(self, file_name) -> None:
        self.dataReader = DataReader(file_name=file_name, columns=["W", "A", "S", "D"])
        self.training_data = self.dataReader.getData()

        self._balanceData()
    
    def _balanceData(self):
        # When (A,D) or (W,S) == (1,1) set it (0,0) -> Avoid pressing unneccessarily
        self.training_data.loc[(self.training_data["W"] == 1) & 
                                (self.training_data["S"] == 1), ["W", "S"]] = [0, 0]
        self.training_data.loc[(self.training_data["A"] == 1) & 
                                (self.training_data["D"] == 1), ["W", "S"]] = [0, 0]


        print(self.dataReader.movementColsToOneCol(self.training_data))


if __name__ == '__main__':
    modelTrainer = ModelTrainer(file_name="outputs/19_08_2022 20_20_10.csv")