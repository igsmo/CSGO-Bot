import numpy as np
import pandas as pd
from collections import Counter
from random import shuffle
import cv2
import sys

import parameters

data = pd.read_csv('outputs/19_08_2022 20_20_10.csv', index_col=0)

np.set_printoptions(threshold=sys.maxsize)

def balanceData(data):
    print(data)
    for index,row in data.iterrows():
        img = row["Frame"].replace("\n", "").replace("[", "").replace("]", "")
        # img = img.split()
        # img = np.array([int(i) for i in img])
        img = np.fromstring(img, dtype=int, sep=' '). \
            astype(np.uint8). \
            reshape(
                        (
                        parameters.RESIZED_HEIGHT,
                        parameters.RESIZED_WIDTH,
                        -1
                        )
                    ) 
        
        img = cv2.resize(img, 
                            (
                                parameters.WIDTH, 
                                parameters.HEIGHT
                            )
                        )
        
        cv2.imshow('test', img)
        row.drop("Frame", inplace=True)
        print(row.values.tolist())
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

balanceData(data)