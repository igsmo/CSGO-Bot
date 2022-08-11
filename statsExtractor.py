from PIL import ImageGrab
import numpy as np
import cv2
import time
import easyocr

# NOTE!!!!
# HARDCODED FOR WIDTH=1280 AND HEIGHT=720

def extract_stats(img):
    
    health_roi = img[680:720, 35:80]
    armor_roi = img[680:720, 172:216]
    ammo_roi = img[670:720, 1130:1217]
    position_roi = img[0:50, 0:150]
    radar_roi = img[50:230, 0:210]
    money_roi = img[230:280, 0:150]
    time_roi = img[0:20, 610:672]
    bomb_roi = img[284:328, 0:58]
    ct_roi = img[0:40, 340:610]
    t_roi = img[0:40, 672:970]

    reader = easyocr.Reader(['en'])
    txt = reader.readtext(health_roi)
    print(txt)
    return health_roi