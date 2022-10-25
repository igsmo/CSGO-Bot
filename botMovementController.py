from pynput.keyboard import Key, Controller
import keyboard
import win32api, win32con
import math

import time

from tools import gameinfoExtractor
from tools import parameters


class MovementController():
    def __init__(self) -> None:
        self.gameinfoManager = gameinfoExtractor.GameinfoExtractor()

        self.keyboard = Controller()

    """ 
    # Converts to 0-pi*2 scale
    # Returns angle in radians
    def _angleTrunc(self, a) -> float:
        while a < 0.0:
            a += math.pi * 2
        return a

    # Calculate angle between two points 
    # Returns angle between points in radians
    def _getAngleBetweenPoints(self, point_origin, point_end) -> float:
        new_x = point_end[0] - point_origin[0]
        new_y = point_end[1] - point_origin[1]
        return self._angleTrunc(math.atan2(new_y, new_x))
    """

    # Rotates around specified axis by given degrees
    # degress is list [x_deg,y_deg]
    def rotateByDegrees(self, degrees: list, movement_speed=1) -> None:
        # 1 px unit is 0.022 degrees
        print(f"Rotating by {degrees}")
        # Rotate horizontally
    
        if 360-degrees[1] >= degrees[1]:
            dx = round(degrees[1]/0.022 / parameters.SENSITIVITY)
        elif 360+degrees[1] < degrees[1]:
            dy = round((degrees[1]+360)/0.022 / parameters.SENSITIVITY)
        else:
            dx = round((degrees[1]-360)/0.022 / parameters.SENSITIVITY)

        direction = 0
        if dx < 0: direction = 1
        if dx >= 0: direction = -1

        for i in range(abs(dx)):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, direction*movement_speed, 0, 0, 0)

        # Rotate vertically
        print(degrees[0])
        # Check if it is faster to rotate up or down
        if degrees[0] <= 0:
            degrees[0] += 360
        elif degrees[0] >= 360:
            degrees[0] -= 360

        if 360-degrees[0] >= degrees[0]:
            dy = round(degrees[0]/0.022 / parameters.SENSITIVITY)
        elif 360+degrees[0] < degrees[0]:
            dy = round((degrees[0]+360)/0.022 / parameters.SENSITIVITY)
        else:
            dy = round((degrees[0]-360)/0.022 / parameters.SENSITIVITY)

        direction = 0
        if dy < 0: direction = -1
        if dy >= 0: direction = 1

        for i in range(abs(dy)):
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, direction*movement_speed, 0, 0)


    # Moves mouse to given angles       
    # destination -> [EyeAngleX,EyeAngleY]
    # error -> angle in degrees to be of error
    # movement_speed -> how fast to move mouse
    def orientateToAngle(self, destination: list) -> None:
        stats = self.gameinfoManager.getPlayerStats()

        eyes = [stats["EyeAngleX"], stats["EyeAngleY"]]
        rotation_goal = [destination[0] - stats["EyeAngleX"], destination[1] - stats["EyeAngleY"]]

        # print(f"Current eyes {eyes} and wanted rotation {destination} gives {rotation_goal}")

        self.rotateByDegrees(rotation_goal)


    # Moves mouse so it is looking towards given point
    # destination -> [posX,posY]
    # error -> angle in degrees to be of error
    # movement_speed -> how fast to move mouse
    def orientateTowardsPoint(self, point: list) -> None:
        stats = self.gameinfoManager.getPlayerStats()

        # Calculate desitnation EyeAngleX and cast to degrees
        new_x = point[0] - stats["PositionX"]
        new_y = point[1] - stats["PositionY"]
        
        destination_x_ang = math.degrees(math.atan2(new_y, new_x))

        self.orientateToAngle([0, destination_x_ang])


def main():
    movementController = MovementController()
    time.sleep(1)
    movementController.orientateTowardsPoint([960.12030029, 505.92266846, -193.69226074])


if __name__ == "__main__":
    main()