import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2
import sys

import captureParameters


class DataReader:
    def __init__(self, file_name) -> None:
        np.set_printoptions(threshold=sys.maxsize)
        self.file_name = file_name
        self.data = None

        self._initData()

    def _npArrayFrameFromStr(self, img_string, 
                            height=captureParameters.RESIZED_HEIGHT,
                            width=captureParameters.RESIZED_WIDTH):

        img_string = img_string.replace("\n", "").replace("[", "").replace("]", "")       
        img = np.fromstring(img_string, dtype=int, sep=' '). \
            astype(np.uint8). \
            reshape(
                        (
                        height,
                        width,
                        -1
                        )
                    ) 
        
        return img

    def _initData(self):
        
        self.data = pd.read_csv(f'{self.file_name}', index_col=0)

        frames = []
        for index,row in self.data.iterrows():
            frame = self._npArrayFrameFromStr(row["Frame"])
            frames.append(frame)

        self.data["Frame"] = frames
        print(self.data)
    
    def displayData(self):
        for index,row in self.data.iterrows():
            
            img = cv2.resize(row["Frame"], 
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
        

if __name__ == '__main__':
    dr = DataReader(file_name='outputs/19_08_2022 20_20_10.csv')
    dr.displayData()