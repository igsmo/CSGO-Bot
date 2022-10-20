from multiprocessing import connection
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

from tools import parameters

def getArrayFromStringColumn(ind, column_name, datatype=float):
        connections = waypoints_df.loc[ind, [column_name]].copy()[0][1:-1].split(",")

        # Set to empty array if no elements
        if connections == ['']:
            connections = []
        
        # Convert to int and add
        connections = [datatype(i) for i in connections]

        return connections


def readData():
    global waypoints_df, latest_selected

    def _extractArrayFromString(row):
        arr = " ".join(str(row).split())[1:-1].replace("'", "").replace(",", " ").split(" ")
        arr = [i for i in arr if i]
        return arr

    waypoints_df = pd.read_csv(parameters.WAYPOINTS_NAME+"_modified.csv", sep=';')

    waypoints_df['WaypointID'] = waypoints_df['WaypointID'].astype("int")

    waypoints_df['Connections'] = waypoints_df['Connections'].astype("string")

    waypoints_df['PosXYZ'] = waypoints_df['PosXYZ'].apply(_extractArrayFromString)

    waypoints_df["x"] = waypoints_df['PosXYZ'].apply(lambda x: x[0]).astype(float)
    waypoints_df["y"] = waypoints_df['PosXYZ'].apply(lambda x: x[1]).astype(float)
    waypoints_df["z"] = waypoints_df['PosXYZ'].apply(lambda x: x[2]).astype(float)

    print(waypoints_df)


def plotPath():
    global ax, fig, plot_points
    if parameters.PLOT_PROJECTION == "3D":  
        ax = plt.axes(projection='3d')
    else: 
        ax = plt.axes()

    fig = ax.get_figure()

    if parameters.PLOT_PROJECTION == "3D":
        scatter = ax.scatter(waypoints_df.x, waypoints_df.y, waypoints_df.z, c=waypoints_df.z)
    else:
        scatter = ax.scatter(waypoints_df.x, waypoints_df.y, c=waypoints_df.z, picker=True)

    plot_points = scatter.get_offsets()

    plt.show()


def calculateDistancesBetweenConnections():
    waypoints_df["Distances"] = ""

    for i,row in waypoints_df.iterrows():
        connections = getArrayFromStringColumn(i, "Connections", datatype=int)
        coordinates = np.array([float(i) for i in row["PosXYZ"]]) # Convert string to floats to get x,y,z

        distances = []
        
        for connection in connections:
            connection_coordinates = np.array([float(i) for i in waypoints_df.iloc[connection]["PosXYZ"]]) # Get x,y,z of connected point

            distance = np.sqrt(np.sum((connection_coordinates-coordinates)**2, axis=0)) # Calculate distance
            distances.append(distance)

        waypoints_df.loc[i, ["Distances"]] = f"{distances}"


def calculateDistancesToFinish(end_point):
    waypoints_df["HeuristicDistance"] = 0.0

    end_coordinates = np.array([float(i) for i in waypoints_df.iloc[end_point]["PosXYZ"]]) # Get x,y,z of end point

    for i,row in waypoints_df.iterrows():
        coordinates = np.array([float(i) for i in row["PosXYZ"]]) # Convert string to floats to get x,y,z

        distance = np.sqrt(np.sum((end_coordinates-coordinates)**2, axis=0)) # Calculate distance

        waypoints_df.loc[i, ["HeuristicDistance"]] = distance


def getHeuristicDistance(id):
    return waypoints_df.iloc[id]["HeuristicDistance"]


def getDistance(id):
    return waypoints_df.iloc[id]["Distance"]


def getInsertSortedI(arr_in, key):
    n = len(arr_in)
    arr = arr_in.copy() + [0 for i in range(len(arr_in))]

    i = n - 1

    while i >= 0 and arr[i] > key:
        arr[i + 1] = arr[i]
        i -= 1
    
    return i + 1


def performAStar(start_point, end_point):
    visited = [start_point]

    ids_queue = [start_point]
    dist_queue = [0]
    weight_queue = [getHeuristicDistance(start_point)]
    
    while ids_queue is not []:
        
        current_id = ids_queue[0]
        current_connections = getArrayFromStringColumn(current_id, "Connections", datatype=int)
        current_distances = getArrayFromStringColumn(current_id, "Distances", datatype=float)
        current_heuristic = float(waypoints_df.iloc[current_id]["HeuristicDistance"])

        print(current_id, current_connections, visited)
        for i,id in enumerate(current_connections):
            if id in visited: continue
            
            next_heuristic = waypoints_df.iloc[id]["HeuristicDistance"]
            next_distance = current_distances[i] + dist_queue[0]
            weight = next_heuristic + next_distance

            insert_ind = getInsertSortedI(weight_queue, weight)

            if insert_ind > len(ids_queue):
                ids_queue.append(id)
                dist_queue.append(next_distance)
                weight_queue.append(weight)
            else:
                ids_queue.insert(insert_ind, id)
                dist_queue.insert(insert_ind, next_distance)
                weight_queue.insert(insert_ind, weight)

            visited.append(id)
            ids_queue.pop(0)
            dist_queue.pop(0)
            weight_queue.pop(0)



def main():
    # TEST VARIABLES 
    end_point = 12
    start_point = 3
    readData()
    calculateDistancesBetweenConnections()
    calculateDistancesToFinish(end_point)

    print(waypoints_df)

    performAStar(start_point, end_point)


if __name__ == '__main__':
    main()