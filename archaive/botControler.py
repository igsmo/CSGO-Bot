import numpy as np
import time
import cv2
from PIL import ImageGrab

from tools import models
from tools import parameters
from tools import imageProcessor

class Bot:
    def __init__(self, model) -> None:
        self.model = model()
        self.model.load(parameters.MODEL_NAME)
    
    def predict(self, screen):
        prediction = self.model.predict([screen.reshape(parameters.RESIZED_WIDTH,
                                                        parameters.RESIZED_HEIGHT,
                                                        1)])[0]

        moves = list(np.around(prediction))
        print(moves, prediction)
        

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

        print(f"Loop took {time.time()-last_time} s")
        last_time = time.time()
        bot.predict(imageProcessor.processForPrediction(frame))
        
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

if __name__ == '__main__':
    bot = Bot(model=models.alexnet)
    main_loop()