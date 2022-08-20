import numpy as np
import pandas as pd
from collections import Counter
from sklearn.utils import shuffle
import cv2

from dataReader import DataReader

class ModelTrainer():
    def __init__(self, file_name) -> None:
        self.dataReader = DataReader(file_name=file_name, columns=["W", "A", "S", "D", "EyeAngleX", "EyeAngleY"])
        self.training_data = self.dataReader.getData()

    def unifyData(self):
        # When (A,D) or (W,S) == (1,1) set it (0,0) -> Avoid pressing unneccessarily
        self.training_data.loc[(self.training_data["W"] == 1) & 
                                (self.training_data["S"] == 1), ["W", "S"]] = [0, 0]
        self.training_data.loc[(self.training_data["A"] == 1) & 
                                (self.training_data["D"] == 1), ["A", "D"]] = [0, 0]
    
    def balanceKeyboardData(self, minimum_count=100):
        movement_data = self.dataReader.movementColsToOneCol(self.training_data)
        movement_data["KeyboardDataString"] = movement_data["KeyboardData"].apply(str)

        print("------------ Value count BEFORE balancing ------------")
        print(f'{movement_data["KeyboardDataString"].value_counts()}')
        print("------------------------------------------------------")
        
        # Print unique values
        # print(movement_data["KeyboardDataString"].unique().tolist())

        # Remove rows where count is smaller than minimum_count
        movement_data = movement_data.groupby("KeyboardDataString") \
                                    .filter(lambda x : len(x) > minimum_count) 
        movement_data = shuffle(movement_data).reset_index(drop=True)

        # Balance keyboard data
        balanced_data = pd.DataFrame(columns=movement_data.columns.tolist())
        unique_movement_data = movement_data["KeyboardDataString"].unique().tolist()
        goal_count = min(movement_data["KeyboardDataString"].value_counts().values.tolist())
        for movement in unique_movement_data:
            temp_data = movement_data[movement_data["KeyboardDataString"] == movement][:goal_count]
            balanced_data = pd.concat([balanced_data, temp_data], ignore_index=True)
        balanced_data = shuffle(balanced_data)
        
        print("------------ Value count AFTER balancing ------------")
        print(f'{balanced_data["KeyboardDataString"].value_counts()}')
        print("------------------------------------------------------")

        self.training_data = balanced_data


if __name__ == '__main__':
    modelTrainer = ModelTrainer(file_name="outputs/19_08_2022 20_20_10.csv")
    modelTrainer.unifyData()
    modelTrainer.balanceKeyboardData()
    