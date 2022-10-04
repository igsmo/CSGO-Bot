import cv2
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pynput import keyboard # , mouse

from tools import imageProcessor
from tools import gameinfoExtractor
from tools import parameters

waypoint_data = None

def addWaypoint(key):
    global waypoint_data

    if str(key) == "'.'":
        # np.save(parameters.WAYPOINTS_NAME, waypoint_data.to_numpy())\
        
        waypoint_data.to_csv(parameters.WAYPOINTS_NAME+".csv", sep=';', index=False)
        print(f"Saved '{parameters.WAYPOINTS_NAME}.csv'")

    if str(key) == "'/'":
        stats = gameinfoManager.getPlayerStats()
        positions = np.array([stats["PositionX"], stats["PositionY"], stats["PositionZ"]])
        # waypoint_id = waypoint_data[-1][0] + 1
        if waypoint_data is None:
            waypoint_data = pd.DataFrame({"WaypointID": [0],
                                        "PosXYZ": [positions],
                                        "Connections": "[]"})
        else:
            waypoint_id = int(waypoint_data.iloc[-1:]["WaypointID"]) + 1
            print(waypoint_id)
            row = pd.DataFrame({"WaypointID": [waypoint_id],
                                        "PosXYZ": [positions],
                                        "Connections": "[]"})
            waypoint_data = pd.concat([waypoint_data, row])

        print(waypoint_data)

gameinfoManager = gameinfoExtractor.GameinfoExtractor()

keyboardCaptureProcess = keyboard.Listener(on_press=addWaypoint)
keyboardCaptureProcess.start()

while(True): 
    pass

# WAYPOINT_ID, POS_XYZ, CONNECTIONS