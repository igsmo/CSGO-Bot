from multiprocessing import connection
from pathlib import Path
from queue import Empty
from tracemalloc import start
from turtle import onclick
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg
import pandas as pd
from ast import literal_eval
from pynput import keyboard # , mouse
import heapq

from tools import parameters

class Pathfinder():
    def __init__(self) -> None:
        self.waypoints_df = None

        self.readData()
        self.calculateDistancesBetweenConnections()

    def getArrayFromStringColumn(self, ind, column_name, datatype=float):
        connections = self.waypoints_df.loc[ind, [column_name]].copy()[0][1:-1].split(",")

        # Set to empty array if no elements
        if connections == ['']:
            connections = []
        
        # Convert to int and add
        connections = [datatype(i) for i in connections]

        return connections

    def readData(self):

        def _extractArrayFromString(row):
            arr = " ".join(str(row).split())[1:-1].replace("'", "").replace(",", " ").split(" ")
            arr = [i for i in arr if i]
            return np.asarray(arr).astype(float)

        self.waypoints_df = pd.read_csv(parameters.WAYPOINTS_NAME+"_modified.csv", sep=';')

        self.waypoints_df['WaypointID'] = self.waypoints_df['WaypointID'].astype("int")

        self.waypoints_df['Connections'] = self.waypoints_df['Connections'].astype("string")

        self.waypoints_df['PosXYZ'] = self.waypoints_df['PosXYZ'].apply(_extractArrayFromString)

        self.waypoints_df["x"] = self.waypoints_df['PosXYZ'].apply(lambda x: x[0]).astype(float)
        self.waypoints_df["y"] = self.waypoints_df['PosXYZ'].apply(lambda x: x[1]).astype(float)
        self.waypoints_df["z"] = self.waypoints_df['PosXYZ'].apply(lambda x: x[2]).astype(float)

        print(self.waypoints_df)


    def plotPath(self):
        global ax, fig, plot_points
        if parameters.PLOT_PROJECTION == "3D":  
            ax = plt.axes(projection='3d')
        else: 
            ax = plt.axes()

        fig = ax.get_figure()

        if parameters.PLOT_PROJECTION == "3D":
            scatter = ax.scatter(self.waypoints_df.x, self.waypoints_df.y, self.waypoints_df.z, c=self.waypoints_df.z)
        else:
            scatter = ax.scatter(self.waypoints_df.x, self.waypoints_df.y, c=self.waypoints_df.z, picker=True)

        plot_points = scatter.get_offsets()

        plt.show()


    def calculateDistancesBetweenConnections(self):
        self.waypoints_df["Distances"] = ""

        for i,row in self.waypoints_df.iterrows():
            connections = self.getArrayFromStringColumn(i, "Connections", datatype=int)
            coordinates = np.array([float(i) for i in row["PosXYZ"]]) # Convert string to floats to get x,y,z

            distances = []
            
            for connection in connections:
                connection_coordinates = np.array([float(i) for i in self.waypoints_df.iloc[connection]["PosXYZ"]]) # Get x,y,z of connected point

                distance = np.sqrt(np.sum((connection_coordinates-coordinates)**2, axis=0)) # Calculate distance
                distances.append(distance)

            self.waypoints_df.loc[i, ["Distances"]] = f"{distances}"


    def calculateDistancesToFinish(self, end_point):
        self.waypoints_df["HeuristicDistance"] = 0.0

        end_coordinates = np.array([float(i) for i in self.waypoints_df.iloc[end_point]["PosXYZ"]]) # Get x,y,z of end point

        for i,row in self.waypoints_df.iterrows():
            coordinates = np.array([float(i) for i in row["PosXYZ"]]) # Convert string to floats to get x,y,z

            distance = np.sqrt(np.sum((end_coordinates-coordinates)**2, axis=0)) # Calculate distance

            self.waypoints_df.loc[i, ["HeuristicDistance"]] = distance


    # graph is a dictionary:
    # {id:{id_conn:[distance, heuristic], ...}}
    def astar(self, graph, start_node, end_node):
        # astar: F=G+H, we name F as f_distance, G as g_distance, 
        # H as heuristic
        f_distance={node:float('inf') for node in graph}
        f_distance[start_node]=0
        
        g_distance={node:float('inf') for node in graph}
        g_distance[start_node]=0
        
        came_from={node:None for node in graph}
        came_from[start_node]=start_node
        
        queue=[(0,start_node)]
        while queue:
            current_f_distance,current_node=heapq.heappop(queue)

            if current_node == end_node:
                print('found the end_node')
                return f_distance, came_from
            for next_node,weights in graph[current_node].items():
                temp_g_distance=g_distance[current_node]+weights[0]
                if temp_g_distance<g_distance[next_node]:
                    g_distance[next_node]=temp_g_distance
                    heuristic=weights[1]
                    f_distance[next_node]=temp_g_distance+heuristic
                    came_from[next_node]=current_node
                    
                    heapq.heappush(queue,(f_distance[next_node],next_node))
        return f_distance, came_from


    def getGraphFromWaypointsDf(self):
        graph = {}
        for i,row in self.waypoints_df.iterrows():
            connections = self.getArrayFromStringColumn(i, "Connections", datatype=int)
            distances = self.getArrayFromStringColumn(i, "Distances", datatype=float)

            dict_to_insert = {}
            for j,conn_id in enumerate(connections):
                dict_to_insert[conn_id] = [distances[j], self.waypoints_df.iloc[conn_id]["HeuristicDistance"]]

            graph[int(row["WaypointID"])] = dict_to_insert
        
        return graph


    def getPath(self, start_point, end_point):
        self.calculateDistancesToFinish(end_point)

        came_from = self.astar(self.getGraphFromWaypointsDf(),start_point,end_point)[1]
        current = end_point
        path = []
        while current != start_point:
            path.append(current)
            current = came_from[current]
        path.append(start_point)

        return path[::-1]


def main():
    # TEST VARIABLES 
    end_point = 82
    start_point = 0

    pathfinder = Pathfinder()
    print(pathfinder.getPath(start_point, end_point))


if __name__ == '__main__':
    main()