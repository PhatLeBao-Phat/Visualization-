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

import dash as dcc
from dash import html, Dash, ctx
from dash.dependencies import Input, Output, State

class FigureManager:
    clustering_key : str = "neighbourhood group"
    selected_data : dict = {"points": []}
    filtered_data = []

    def __init__(self) -> None:
        self.test = []
        pass

    def data(self, selected) -> None:
        """
        Changes the memory of the selected data for all figures using this class
        """
        for key in selected.keys():
            if key in self.selected_data:
                self.selected_data[key] = selected[key]
        pass

    def figure(self):
        fig = go.Figure()

        return fig



class Map(FigureManager):

    def __init__(self) -> None:
        if "range" not in self.selected_data:
            self.selected_data["range"] = {}
        pass

    def figure(self):
        fig = go.Figure()

        return fig

test1 = Map()
test2 = Map()
test3 = Map()
manager = CustomFigure()

selected = {"points": [1, 2, 3]}
manager.data(selected)

for t in [test1, test2, test3, manager]:
    print(t.selected_data, t.clustering_key)

