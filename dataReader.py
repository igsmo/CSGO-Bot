import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2
import sys

import captureParameters


class DataReader:
    def __init__(self, file_name: str, columns=None) -> None:
        np.set_printoptions(threshold=sys.maxsize)
        self.file_name = file_name
        self.data = None

        self._initData(columns=columns)

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

    def movementColsToOneCol(self, data):
        res = data.copy()
        keys_to_log = list(set(captureParameters.KEYS_TO_LOG).intersection(res.columns.tolist()))
        movement_data = res[keys_to_log].values.tolist()
        res["KeyboardData"] = movement_data
        print(res.columns.tolist())
        res = res.drop(columns=keys_to_log)

        return res
    
    def displayData(self,
                    height=captureParameters.RESIZED_HEIGHT,
                    width=captureParameters.RESIZED_WIDTH):
        for index,row in self.data.iterrows():
            frame_rows = row["Frame"].reshape((height, width, -1 )) 
            img = cv2.resize(frame_rows, 
                                (
                                    captureParameters.WIDTH, 
                                    captureParameters.HEIGHT
                                )
                            )
            
            cv2.imshow('test', img)

            row = row.iloc[0:len(row.tolist())-1]
            print(row.values.tolist())

            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break

    def getDataExcept(self, columns: list):
        return self.data[self.data != columns]
    
    def getData(self):
        return self.data
        

if __name__ == '__main__':
    dr = DataReader(file_name='outputs/19_08_2022 20_20_10.csv')
    dr.displayData()