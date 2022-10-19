from multiprocessing import connection
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

def extractArrayFromString(ind, column_name, datatype=float):
        connections = waypoints_df.loc[ind, [column_name]].copy()[0][1:-1].split(",")

        # Set to empty array if no elements
        if connections == ['']:
            connections = []
        
        # Convert to int and add
        connections = [datatype(i) for i in connections]

        return connections


def extract_array_from_string(row):
    arr = " ".join(str(row).split())[1:-1].replace("'", "").replace(",", " ").split(" ")
    arr = [i for i in arr if i]
    return arr


def readData():
    global waypoints_df, latest_selected

    waypoints_df = pd.read_csv(parameters.WAYPOINTS_NAME+"_modified.csv", sep=';')

    waypoints_df['WaypointID'] = waypoints_df['WaypointID'].astype("int")

    waypoints_df['Connections'] = waypoints_df['Connections'].astype("string")

    waypoints_df['PosXYZ'] = waypoints_df['PosXYZ'].apply(extract_array_from_string)

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


def calculateDistances():
    waypoints_df["Distances"] = ""

    for i,row in waypoints_df.iterrows():
        connections = extractArrayFromString(i, "Connections", datatype=int)
        coordinates = np.array([float(i) for i in row["PosXYZ"]]) # Convert string to floats to get x,y,z

        distances = []
        
        for connection in connections:
            connection_coordinates = np.array([float(i) for i in waypoints_df.iloc[connection]["PosXYZ"]]) # Get x,y,z of connected point

            distance = np.sqrt(np.sum((connection_coordinates-coordinates)**2, axis=0)) # Calculate distance
            distances.append(distance)

        waypoints_df.loc[i, ["Distances"]] = f"{distances}"


def main():
    START_POINT = 12
    DESTINATION_POINT = 3
    readData()
    calculateDistances()


if __name__ == '__main__':
    main()