

import pathfindingManager as pfm
import botMovementController as bmc



class Controller():
    def __init__(self) -> None:
        self.pathfindingManager = pfm.PathfindingManager()
        self.movementController = bmc.MovementController()

    def moveToWaypoint(self, waypoint_id: int):
        


def main():
    bot = Controller()


if __name__ == "__main__":
    main()