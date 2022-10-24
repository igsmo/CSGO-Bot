from pynput.keyboard import Key, Controller
import win32api, win32con
import math

import time

from tools import gameinfoExtractor
from tools import parameters


class MovementController():
    def __init__(self) -> None:
        self.gameinfoManager = gameinfoExtractor.GameinfoExtractor()

        self.keyboard = Controller()

    # Moves mouse to given angles
    # destination -> [EyeAngleX,EyeAngleY]
    # error -> angle in degrees to be of error
    # movement_speed -> how fast to move mouse
    def orientateToAngle(self, destination: list, error=2, movement_speed=1):
        stats = self.gameinfoManager.getPlayerStats()

        # Convert to 0 - 360 deg
        if destination[0] < 0: destination[0] += 360
        if destination[1] < 0: destination[1] += 360

        # Move horizontally
        while (abs(stats["EyeAngleY"] - destination[0]) > error):
            
            # Move right if destination is on the right
            if stats["EyeAngleY"] - destination[0] < 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, movement_speed, 0, 0, 0)
            # Move left if destination is on the left
            if stats["EyeAngleY"] - destination[0] > 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, -movement_speed, 0, 0, 0)

            stats = self.gameinfoManager.getPlayerStats()

            time.sleep(0.01)


        # Move vertically
        while abs(stats["EyeAngleX"] - destination[1])  > error:
            # Move up if destination is up
            if stats["EyeAngleX"] - destination[1] < 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, -movement_speed, 0, 0)
            # Move down if destination is down
            if stats["EyeAngleX"] - destination[1] > 0:
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, 0, movement_speed, 0, 0)

            stats = self.gameinfoManager.getPlayerStats()

            time.sleep(0.01)
            

    # Moves mouse so it is looking towards given point
    # destination -> [posX,posY]
    # error -> angle in degrees to be of error
    # movement_speed -> how fast to move mouse
    def orientateTowardsPoint(self, point: list, error=2, movement_speed=20):
        stats = self.gameinfoManager.getPlayerStats()

        # Calculate desitnation EyeAngleX and cast to degrees
        destination_x_ang = math.atan((point[1]-stats["PositionY"])/(point[0]-stats["PositionX"]))
        destination_x_ang = math.degrees(destination_x_ang)
        print(destination_x_ang)
        self.orientateToAngle([0, destination_x_ang], error=error, movement_speed=movement_speed)


def main():
    movementController = MovementController()
    time.sleep(1)
    movementController.orientateTowardsPoint([960.12030029, 505.92266846, -193.69226074])


if __name__ == "__main__":
    main()