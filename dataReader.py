import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2
import sys

import parameters


class DataReader:
    def __init__(self, file_name: str, columns=None) -> None:
        np.set_printoptions(threshold=sys.maxsize)
        self.file_name = file_name
        self.data = None

        self._initData(columns=columns)

        print(self.getData().head())

    def _npArrayFrameFromStr(self, img_string):

        img_string = img_string.replace("\n", "").replace("[", "").replace("]", "")       
        img = np.fromstring(img_string, dtype=int, sep=' '). \
            astype(np.uint8)
        
        return img

    def _initData(self, columns: list):
        
        self.data = pd.read_csv(f'{self.file_name}', index_col=0)

        if columns != None:
            self.data = self.data[columns+["Frame"]]

        # Convert str to np.array for frames
        frames = []
        for index,row in self.data.iterrows():
            frame = self._npArrayFrameFromStr(row["Frame"])
            frames.append(frame)
        self.data["Frame"] = frames

    def movementColsToOneCol(self, data) -> pd.DataFrame:
        res = data.copy()
        print(res.columns.tolist())
        # Get parameters only present in data
        keys_to_log = [i for i, j in zip(parameters.KEYS_TO_LOG, res.columns.tolist()) if i == j]
        keyboard_data = res[keys_to_log].values.tolist()
        res["KeyboardData"] = keyboard_data
        # res = res.drop(columns=keys_to_log)

        # eye_data = res[["EyeAngleX", "EyeAngleY"]].values.tolist()
        # res["EyeData"] = eye_data
        # res = res.drop(columns=["EyeAngleX", "EyeAngleY"])

        return res
    
    def displayData(self,
                    height=parameters.RESIZED_HEIGHT,
                    width=parameters.RESIZED_WIDTH) -> None:
        for index,row in self.data.iterrows():
            frame_rows = row["Frame"].reshape((height, width, -1 )) 
            img = cv2.resize(frame_rows, 
                                (
                                    parameters.WIDTH, 
                                    parameters.HEIGHT
                                )
                            ) 
            
            cv2.imshow('test', img)

            row = row.iloc[0:len(row.tolist())-1]
            print(row.values.tolist())

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def getDataExcept(self, columns: list) -> pd.DataFrame:
        return self.data[self.data != columns]
    
    def getData(self) -> pd.DataFrame:
        return self.data
        

if __name__ == '__main__':
    dr = DataReader(file_name='outputs/19_08_2022 20_20_10.csv')
    dr.displayData()