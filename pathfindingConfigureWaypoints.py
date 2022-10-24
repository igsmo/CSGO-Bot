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

csgo_radar = mpimg.imread('mirage_0pos.png')

def extractConnectionsArr(ind):
        connections = waypoints_df.loc[ind, ["Connections"]].copy()[0][1:-1].split(",")

        # Set to empty array if no elements
        if connections == ['']:
            connections = []
        
        # Convert to int and add
        connections = [int(i) for i in connections]

        return connections

def updateWaypointConnections():
    global scatter
    ax.clear()
    
    if parameters.PLOT_PROJECTION == "3D":
        scatter = ax.scatter(waypoints_df.x, waypoints_df.y, waypoints_df.z, c=waypoints_df.z, picker=True)
    else:
        scatter = ax.scatter(waypoints_df.x, waypoints_df.y, c=waypoints_df.z, picker=True)
    
    for i,row in waypoints_df.iterrows():
        x_start = row.x
        y_start = row.y
        z_start = row.z
        # print(f"Start connect: {row.WaypointID}")

        connections = extractConnectionsArr(row.WaypointID)

        for conn_to_plot in connections:
            # print(f"To connect: {waypoints_df.iloc[conn_to_plot].WaypointID}")
            x_end = waypoints_df.iloc[conn_to_plot].x
            y_end = waypoints_df.iloc[conn_to_plot].y
            z_end = waypoints_df.iloc[conn_to_plot].z
            ax.plot([x_start, x_end], [y_start, y_end], [z_start, z_end])

    pid = waypoints_df["WaypointID"].tolist()
    for xi, yi, pidi in zip(waypoints_df.x,waypoints_df.y,pid):
        ax.annotate(str(pidi), xy=(xi,yi))
        
    plt.draw()

def onPick(event):
    global latest_selected

    if parameters.PLOT_PROJECTION == "3D":
        artist = event.artist
        xData, yData, zData = [o.data for o in artist._offsets3d]
        
        point = [list(xData), list(yData), list(zData)]
        ind = event.ind[0]
        # print(point)
        selected_point = waypoints_df[(waypoints_df["x"] == point[0][ind]) & (waypoints_df["y"] == point[1][ind])].iloc[0]

    
    else:
        ind = event.ind[0]
        point = list(plot_points[ind])
        selected_point = waypoints_df[(waypoints_df["x"] == point[0]) & (waypoints_df["y"] == point[1])].iloc[0]
    
    # print(selected_point)
    # print(latest_selected)

    if latest_selected is not None:
        if latest_selected["WaypointID"] != selected_point["WaypointID"]:
            
            selected_connections = extractConnectionsArr(ind)
            latest_connections = extractConnectionsArr(latest_selected.WaypointID)

            if int(latest_selected["WaypointID"]) in selected_connections:
                updateWaypointConnections()
                return

            selected_connections.append(latest_selected["WaypointID"])
            latest_connections.append(selected_point["WaypointID"])

            # Replace column value
            waypoints_df.loc[selected_point["WaypointID"], "Connections"] = str(selected_connections)
            waypoints_df.loc[latest_selected["WaypointID"], "Connections"] = str(latest_connections)

            # Update graph
            updateWaypointConnections()

    if latest_selected is None:
        latest_selected = selected_point
    else:
        latest_selected = None

    print("Updated DF")
    print(waypoints_df)

def addKeyListener():
    global waypoints_df

    def _keyListener(key):
        if str(key) == "'.'": # Finish and save waypoints
            # waypoints_df = waypoints_df.drop(columns=['x', 'y', 'z'])
            waypoints_df.to_csv(parameters.WAYPOINTS_NAME+"_modified.csv", sep=';', index=False)
            print(f"Saved '{parameters.WAYPOINTS_NAME}_modified.csv'")

    keyboardCaptureProcess = keyboard.Listener(on_press=_keyListener)
    keyboardCaptureProcess.start()

def readData():
    global waypoints_df, latest_selected

    waypoints_df = pd.read_csv(parameters.WAYPOINTS_NAME+"_modified.csv", sep=';')
    # waypoints_df = pd.read_csv(parameters.WAYPOINTS_NAME+".csv", sep=';')

    waypoints_df['WaypointID'] = waypoints_df['WaypointID'].astype("int")

    waypoints_df['Connections'] = waypoints_df['Connections'].astype("string")
    
    def extract_array_from_string(row):
        arr = " ".join(str(row).split())[1:-1].replace("'", "").replace(",", " ").split(" ")
        arr = [i for i in arr if i]
        return arr

    waypoints_df['PosXYZ'] = waypoints_df['PosXYZ'].apply(extract_array_from_string)

    waypoints_df["x"] = waypoints_df['PosXYZ'].apply(lambda x: x[0]).astype(float)
    waypoints_df["y"] = waypoints_df['PosXYZ'].apply(lambda x: x[1]).astype(float)
    waypoints_df["z"] = waypoints_df['PosXYZ'].apply(lambda x: x[2]).astype(float)

    print(waypoints_df)

    latest_selected = None

def startPlot():
    global ax, fig, plot_points
    if parameters.PLOT_PROJECTION == "3D":  
        ax = plt.axes(projection='3d')
    else: 
        ax = plt.axes()

    fig = ax.get_figure()

    if parameters.PLOT_PROJECTION == "3D":
        scatter = ax.scatter(waypoints_df.x, waypoints_df.y, waypoints_df.z, c=waypoints_df.z, picker=True)
    else:
        scatter = ax.scatter(waypoints_df.x, waypoints_df.y, c=waypoints_df.z, picker=True)

    plot_points = scatter.get_offsets()

    pid = waypoints_df["WaypointID"].tolist()
    for xi, yi, pidi in zip(waypoints_df.x,waypoints_df.y,pid):
        ax.annotate(str(pidi), xy=(xi,yi))

    cid = fig.canvas.mpl_connect('pick_event', onPick)

    plt.show()

    updateWaypointConnections()

def main():
    addKeyListener()
    readData()
    startPlot()

if __name__ == '__main__':
    main()