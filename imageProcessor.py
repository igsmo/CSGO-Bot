import cv2
import numpy as np

import captureParameters


def processForEdgeDetection(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(
                                processed_img, 
                                threshold1=captureParameters.CANNY_THRESHOLD1, 
                                threshold2=captureParameters.CANNY_THRESHOLD2
                            )
    return processed_img

def processForLogging(original_img):
    img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    img = cv2.resize(img, 
                                (
                                    captureParameters.RESIZED_WIDTH, 
                                    captureParameters.RESIZED_HEIGHT
                                )
                            )
    img = {"Frame": img.reshape(-1)}
    return img

