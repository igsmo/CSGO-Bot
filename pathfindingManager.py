import numpy as np
import time
from scipy.spatial import KDTree

import pathfindingFindPathAStar
from tools import gameinfoExtractor
from tools import parameters

class PathfindingManager():
    def __init__(self) -> None:
        self.pathfinder = pathfindingFindPathAStar.Pathfinder()
        self.gameinfoManager = gameinfoExtractor.GameinfoExtractor()
        
        self.waypoints_df = self.pathfinder.waypoints_df
        self.kdtree = KDTree(self.waypoints_df["PosXYZ"].tolist())

    def getNearestPoint(self):
        stats = self.gameinfoManager.getPlayerStats()
        current_position = [stats["PositionX"], stats["PositionY"], stats["PositionZ"]]
        dist, id = self.kdtree.query(current_position, 1)
        return self.waypoints_df.iloc[id]

    def findPathFromCurrentPosition(self, destination):
        return self.pathfinder.getPath(self.getNearestPoint(), destination)

    

def main():
    movementManager = PathfindingManager()
    while True:
        movementManager.findPathFromCurrentPosition(30)
        time.sleep(0.1)

if __name__ == '__main__':
    main()