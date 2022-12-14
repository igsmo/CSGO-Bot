from PIL import ImageGrab
import numpy as np
import cv2
import time
from datetime import datetime
import os

from tools import gameinfoExtractor
from tools import parameters
from tools import imageProcessor
from tools import inputManager
from tools import dataLogger


def current_frame():
    return np.array(ImageGrab.grab
                                    (
                                    bbox=(
                                        0,
                                        parameters.CAPTURE_OFFSET,
                                        parameters.WIDTH,
                                        parameters.HEIGHT+parameters.CAPTURE_OFFSET
                                        )
                                    )
                                )


def main_loop():
    
    last_time = time.time()
    while(True):
        frame = current_frame()
        
        #cv2.imshow("window", frame)
        
        dataLoggingManager.logData(
                imageProcessor.processForLogging(frame),
                captureInputManager.getPressedKeys(), 
                gameinfoManager.getPlayerStats()
            )

        print(f"Loop took {time.time()-last_time} s")
        last_time = time.time()
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    captureInputManager = inputManager.InputManager()
    gameinfoManager = gameinfoExtractor.GameinfoExtractor()
    dataLoggingManager = dataLogger.DataLogger(file_name=f'{datetime.now().strftime("%d_%m_%Y %H_%M_%S")}.csv')
    main_loop()