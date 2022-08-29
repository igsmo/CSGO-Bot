import numpy as np
import pandas as pd
from collections import Counter
from sklearn.utils import shuffle
import cv2

from tools.dataReader import DataReader
from tools import parameters
from tools import models

class ModelTrainer():
    def __init__(self, file_name, model) -> None:
        self.dataReader = DataReader(file_name=file_name, columns=["W", "A", "S", "D", "EyeAngleX", "EyeAngleY"])
        self.training_data = self.dataReader.getData()

        self.model = model()

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

    def getPreparedX(self):
        x = np.array(self.training_data["Frame"].values.tolist()). \
            reshape(-1, parameters.RESIZED_WIDTH, parameters.RESIZED_HEIGHT, 1)

        return x

    def getPreparedY(self):
        columns_no_frame = self.dataReader.getData(). \
            loc[:, self.dataReader.getData().columns != "Frame"]
            
        # TODO: Change 3 output to as many as output columns!
        #mouse_key_data = self.training_data[columns_no_frame.columns.tolist()].values.tolist()
        mouse_key_data = self.training_data[["W", "S", "D"]].values.tolist()
        return np.array(mouse_key_data)

    def fitModel(self, x=None, y=None, test_split=0.1):
        if x is None or y is None: 
            x = self.getPreparedX()
            y = self.getPreparedY()
        print(y.shape)

        self.model.fit({'input': x}, {'targets': y}, n_epoch=parameters.EPOCH,
                        validation_set=test_split,
                        snapshot_step=500, show_metric=True, run_id=parameters.MODEL_NAME)        
        
        self.model.save(parameters.MODEL_NAME)


if __name__ == '__main__':
    modelTrainer = ModelTrainer(file_name="outputs/29_08_2022 19_36_21.csv", model=models.alexnet)
    modelTrainer.unifyData()
    modelTrainer.balanceKeyboardData()
    modelTrainer.fitModel()
