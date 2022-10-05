from multiprocessing import connection
from turtle import onclick
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd
from ast import literal_eval

from tools import parameters

def extract_connections_arr(ind):
        connections = waypoints_df.loc[ind, ["Connections"]].copy()[0][1:-1].split(",")

        # Set to empty array if no elements
        if connections == ['']:
            connections = []
        
        # Convert to int and add
        connections = [int(i) for i in connections]

        return connections

def update_waypoint_connections():
    ax.clear()
    
    scatter = ax.scatter(waypoints_df.x, waypoints_df.y, c=waypoints_df.z, picker=True)
    
    for i,row in waypoints_df.iterrows():
        x_start = row.x
        y_start = row.y
        print(f"Start connect: {row.WaypointID}")

        connections = extract_connections_arr(row.WaypointID)

        for conn_to_plot in connections:
            print(f"To connect: {waypoints_df.iloc[conn_to_plot].WaypointID}")
            x_end = waypoints_df.iloc[conn_to_plot].x
            y_end = waypoints_df.iloc[conn_to_plot].y
            print([x_start, x_end], [y_start, y_end])
            ax.plot([x_start, x_end], [y_start, y_end])
    
    plt.draw()

def on_pick(event):
    global latest_selected
    
    ind = event.ind[0]

    selected_point = waypoints_df.iloc[ind]
    print(selected_point)

    if latest_selected is not None:
        if latest_selected["WaypointID"] != selected_point["WaypointID"]:
            
            selected_connections = extract_connections_arr(ind)
            latest_connections = extract_connections_arr(latest_selected.WaypointID)

            if int(latest_selected["WaypointID"]) in selected_connections:
                return

            selected_connections.append(latest_selected["WaypointID"])
            latest_connections.append(selected_point["WaypointID"])

            # Replace column value
            waypoints_df.loc[selected_point["WaypointID"], "Connections"] = str(selected_connections)
            waypoints_df.loc[latest_selected["WaypointID"], "Connections"] = str(latest_connections)

            # Update graph
            update_waypoint_connections()

    if latest_selected is None:
        latest_selected = selected_point
    else:
        latest_selected = None

    print("Updated DF")
    print(waypoints_df)

waypoints_df = pd.read_csv(parameters.WAYPOINTS_NAME+".csv", sep=';')

waypoints_df['WaypointID'] = waypoints_df['WaypointID'].astype("int")

waypoints_df['Connections'] = waypoints_df['Connections'].astype("string")
waypoints_df['PosXYZ'] = waypoints_df['PosXYZ'].apply(lambda x: " ".join(str(x).split())[2:-2].split(" "))

waypoints_df["x"] = waypoints_df['PosXYZ'].apply(lambda x: x[0]).astype(float)
waypoints_df["y"] = waypoints_df['PosXYZ'].apply(lambda x: x[1]).astype(float)
waypoints_df["z"] = waypoints_df['PosXYZ'].apply(lambda x: x[2]).astype(float)

print(waypoints_df)

latest_selected = None

ax = plt.axes()
fig = ax.get_figure()

scatter = ax.scatter(waypoints_df.x, waypoints_df.y, c=waypoints_df.z, picker=True)

cid = fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()

update_waypoint_connections()
