from PIL import ImageGrab
import numpy as np
import cv2
import time
from statsExtractor import extract_stats

def process_img(original_img, threshold1, threshold2):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(processed_img, threshold1=threshold1, threshold2=threshold2)
    return processed_img


last_time = time.time()
canny_threshold1 = 200
canny_threshold2 = 50

while(True):
    original_img = np.array(ImageGrab.grab(bbox=(0,40,1280,720)))
    processed_img = process_img(original_img, canny_threshold1, canny_threshold2)
    #cv2.imshow("test", processed_img)

    cv2.imshow("test",)
    print(f"Loop took {time.time()-last_time} s")
    last_time = time.time()

    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break