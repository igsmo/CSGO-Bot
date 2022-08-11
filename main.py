from PIL import ImageGrab
import numpy as np
import cv2
import time
from pydirectinput import keyDown, keyUp, press
from threading import Thread

from statsExtractor import extract_stats

# Parameters
CANNY_THRESHOLD1 = 200
CANNY_THRESHOLD2 = 50
WIDTH = 1280
HEIGHT = 720


def process_img(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=CANNY_THRESHOLD1, threshold2=CANNY_THRESHOLD2)
    return processed_img


# for i in list(range(3))[::-1]:
#     print(i+1)
#     time.sleep(1)

def main_loop():
    last_time = time.time()
    while(True):
        offset = 30
        original_img = np.array(ImageGrab.grab(bbox=(0,offset,WIDTH,HEIGHT+offset)))
        processed_img = process_img(original_img)
        cv2.imshow("window", processed_img)

        

        # print(f"Loop took {time.time()-last_time} s")
        last_time = time.time()

        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

main_loop_thread = Thread(target=main_loop)
main_loop_thread.start()
main_loop_thread.join()