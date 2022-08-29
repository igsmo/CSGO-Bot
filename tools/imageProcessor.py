import cv2
import numpy as np

from tools import parameters


def processForEdgeDetection(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    processed_img = cv2.Canny(
                                processed_img, 
                                threshold1=parameters.CANNY_THRESHOLD1, 
                                threshold2=parameters.CANNY_THRESHOLD2
                            )
    return processed_img

def processForLogging(original_img):
    img = processForEdgeDetection(original_img)
    img = cv2.resize(img, 
                                (
                                    parameters.RESIZED_WIDTH, 
                                    parameters.RESIZED_HEIGHT
                                )
                            )
    img = {"Frame": img.reshape(-1)}
    return img

def processForPrediction(original_img):
    img = processForEdgeDetection(original_img)
    img = cv2.resize(img, 
                                (
                                    parameters.RESIZED_WIDTH, 
                                    parameters.RESIZED_HEIGHT
                                )
                            )
    return img

def bgrToGray(original_img):
    processed_img = cv2.cvtColor(original_img, cv2.COLOR_BGR2GRAY)
    return processed_img

def binaryThreshold(original_img, threshold):
    ret,processed_img = cv2.threshold(original_img,threshold,255,cv2.THRESH_BINARY)
    return processed_img