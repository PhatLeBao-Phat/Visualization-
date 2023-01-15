"""
This code file contains:
    - FigureManager
    - CustomFigure
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
    # data : dict = {"points": [], "filtered_data": [], "clustering_key": "neighbourhood group"}
    app = {"selectedData": [], "figure": [], "graph": {}}
    ids = []

    def __init__(self) -> None:
        pass

    def figure(self) -> None:
        fig = go.Figure()
        return fig

class CustomFigure(FigureManager):
    def __init__(self, type : str, unique_name : str):
        self.id = type + "-" + unique_name
        self.input = Input(self.id, "selectedData")
        self.output = Output(self.id, "figure")
        self.html = dcc.Loading(
            id="{}-loading".format(self.id),
            children=[
                dcc.Graph(
                    id=self.id
                )
            ],
            type="circle"
        )

        # Check whether id already exist. If yes, create warning!!!
        if self.id in self.ids:
            print("NAME ALREADY IN USE!!! REEEEEE")

        # Add id to manager 
        self.ids.append(self.input)

        # Add inputs and outputs to the callback needed in app
        self.app["selectedData"].append(self.input)
        self.app["figure"].append(self.output)

        # Add dash graph html element to app
        self.app["graph"][id] = self.html

        pass

    def assign_figure(self, figure : callable) -> None:
        self.figure = MethodType(figure, self)
        pass
