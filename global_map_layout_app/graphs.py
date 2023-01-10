"""
This code file contains:
    - Figure class
        > Map
        > Tree
        > Violin
"""

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import json

import dash 
from dash import html, Dash, ctx, dcc
from dash.dependencies import Input, Output, State

from typing import Union
from types import MethodType

class FigureManager:
    data : dict = {"points": [], "filtered_data": [], "clustering_key": "neighbourhood group"}
    app : dict[str: Input] = {"selectedData": [], "children": [], "graph": {}}
    ids : list[str] = []

    def __init__(self, data) -> None:
        self.og_data = data
        self.data["filtered_data"] = data
        pass

    def change_data(self, **args) -> None:
        """
        Changes the memory of the selected data for all figures using this class
        """
        for key in args.keys():
            if key in self.data:
                self.data[key] = args[key]
        pass

    def figure(self) -> None:
        fig = go.Figure()
        return fig

    def need(self, *args : list[str]) -> tuple:
        """
        Returns a tuple from the shared memory dictionary in this manager
        """
        return tuple([self.data[key] for key in args])

    def filter_data(self, conditions) -> None:
        self.data["filtered_data"] = self.og_data.query(conditions)
        pass

class CustomFigure(FigureManager):
    def __init__(self, type : str, unique_name : str):
        # Make standard id format
        id = type + "-" + unique_name

        # Check whether id already exist. If yes, create warning!!!
        if unique_name in self.ids:
            print("NAME ALREADY IN USE!!! REEEEEE")

        # Add id to manager 
        self.ids.append(id)

        # Add inputs, outputs and XXX to the callback needed in app
        self.app["selectedData"].append(Input(id, "selectedData"))
        self.app["children"].append(Output(id, "children"))

        # Add dash graph html element to app
        self.app["graph"][id] = dcc.Loading(
            id="{}-loading".format(id),
            children=[
                dcc.Graph(
                    id=id
                )
            ],
            type="circle"
        )

        pass

    def assign_figure(self, figure : callable) -> None:
        self.figure = MethodType(figure, self)
        pass

def figure(self):
    filtered_data, clustering_key = self.need("filtered_data", "clustering_key")

    # Create map with the data
    fig = px.scatter_mapbox(filtered_data, lat="lat", lon="long", color=filtered_data[clustering_key], custom_data={})

    # Selected points get highlighted yellow and size of marks are 5
    for scatter in fig.data:
        scatter.marker.size = 5
        scatter.selected = {"marker": {"color": "yellow"}}

    # Update layout to have a background. Zoom and center it in New York
    fig.update_layout(mapbox = {"style": "carto-positron", "zoom": 10, "center": {"lon": -73.96276, "lat": 40.68152}})
    fig.update_layout(height=1000)

    return fig

# I need to the os for folder magic
import os
import pandas as pd
import numpy as np

# Creates the data folder
path_to_folder = os.getcwd()
folder_name = "Data"
path_to_new_folder = os.path.join(path_to_folder, folder_name)
if not os.path.exists (path_to_new_folder):
    os.mkdir(path_to_new_folder)
    print("\x1b[36m Created data folder \n")
else:
    print("\x1b[32m Data folder exists\n ")
    
# Checks whether file exists
dataset_name = "airbnb_open_data.csv"
path_to_dataset = os.path.join(path_to_new_folder, dataset_name)

if os.path.exists (path_to_dataset):
    print("\x1b[32m Dataset {} is loaded in succesfully!".format(dataset_name))
    
    # Load in dataset
    data = pd.read_csv(path_to_dataset)
else:
    print(path_to_dataset)
    print("\x1b[31m Dataset still needs to be put in the data folder!\n \n Go to canvas page of visualization and go to the datasets in files.\n Download the airbnb_open_data.csv and put it in the data folder.")

manager = FigureManager(data)
test1 = CustomFigure("map", "1")
test1.assign_figure(figure)


# print(test1.data["filtered_data"])
test1.figure().show()