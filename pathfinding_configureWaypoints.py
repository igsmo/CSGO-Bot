from multiprocessing import connection
from turtle import onclick
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import pandas as pd

from tools import parameters

def on_pick(event):
    global latest_selected

    ind = event.ind[0]
    selected_point = waypoints_df.iloc[ind]

    if latest_selected is not None:
        if latest_selected["id"] != selected_point["id"]:
            
            #TODO: Add new waypoint connections

            old_column_value = np.fromstring(selected_point["connections"])
            print("Current row")
            print(old_column_value)

            new_column_value = [
                                    np.array2string(
                                        np.array(np.append(old_column_value,
                                                    latest_selected["id"]))
                                    )
                                ]

            print("To be updated row")
            print(new_column_value)

            waypoints_df.loc[ind, ["connections"]] = new_column_value

    latest_selected = selected_point

    print("Updated DF")
    print(waypoints_df)

waypoints_list = np.load(parameters.WAYPOINTS_NAME+'.npy', allow_pickle=True)

xdata, ydata, zdata, ids, connections = [], [], [], [], []
latest_selected = None

for row in waypoints_list:
    ids.append(row[0])
    xdata.append(row[1][0])
    ydata.append(row[1][1])
    zdata.append(row[1][2])
    connections.append(np.array2string(row[2]))

waypoints_df = pd.DataFrame({
    "id": ids,
    "x": xdata,
    "y": ydata,
    "z": zdata,
    "connections": connections
})

print(waypoints_df)

ax = plt.axes(projection='3d')
fig = ax.get_figure()

ax.scatter(waypoints_df.x, waypoints_df.y, waypoints_df.z, c=waypoints_df.z, picker=True)

cid = fig.canvas.mpl_connect('pick_event', on_pick)

plt.show()