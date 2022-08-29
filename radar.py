import cv2
import time
import matplotlib.pyplot as plt

from tools import imageProcessor

def getPlayerLocation(radar_img):
    radius = 3

    gray_radar_img = imageProcessor.bgrToGray(radar_img)
    gray = cv2.GaussianBlur(gray_radar_img, (radius, radius), 0)
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    image = radar_img.copy()
    cv2.circle(image, maxLoc, radius, (255, 0, 0), 2)

    return maxLoc

radar_img = cv2.imread('radar_sample.png', 1)

while(True):
    cv2.imshow('image', getPlayerLocation(radar_img)[1])
    print(getPlayerLocation(radar_img))
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break