# from color import color
import plotly.graph_objects as go


def figure(self, filtered_data, clustering_key, color_map, tourist_bool = True):
    # Create map
    if type(color_map) != list:
        # Coloured on a discrete clustering_key
        fig = px.scatter_mapbox(filtered_data, lat="latitude", lon="longitude", color=clustering_key, color_discrete_map=color_map, custom_data={})
    else:
        # Coloured on a sequential clustering_key
        fig = px.scatter_mapbox(filtered_data, lat="latitude", lon="longitude", color=clustering_key, color_continuous_scale=color_map, custom_data={})

    # Selected points get highlighted yellow and size of marks are 5
    for scatter in fig.data:
        scatter.marker.size = 5
        scatter.selected = {"marker": {"color": "yellow"}}

    # Tourist attractions mapped on the map
    if tourist_bool == True or tourist_bool == "True":
        fig.add_trace(go.Scattermapbox(
            lat = [40.8296, 40.7826, 40.6892, 40.704, 40.7580, 40.8506, 40.7126, 40.7484, 40.7593, 40.8972, 40.7400, 40.695],
            lon = [-73.9262, -73.9656, -74.0445, -73.9942, -73.9855, -73.8770, -74.0099, -73.9857, -73.9794, -73.8861, -73.8407, -73.866],
            mode = "markers",
            marker=go.scattermapbox.Marker(
                size=25,
                color='rgb(0, 0, 0)',
                opacity=0.6,
            ),
            text=["Yankee Stadium", "Central Park", "Statue of Liberty", "Brooklyn Bridge", "Times Squares", "Bronx Zoo", "World trade center", "Empire state building", "Top of the Rock", "Van Cortlandt Park", "Flushing Meadows Corona Park", "Forest Park"],
            name = "Tourist attractions"
        ))

    # Changes style, zooms in on center of New York
    fig.update_layout(mapbox = {"style": "carto-positron", "zoom": 10, "center": {"lon": -73.96276, "lat": 40.68152}})

    # Less white space
    fig.update_layout(margin={"r": 5, "t": 0, "l": 5, "b": 0})

    # Anchors the legend in the left corner (to not get in the way of the filter menu)
    fig.update_layout(legend=dict(
        yanchor="bottom",
        y=0,
        xanchor="left",
        x=0,
    ))

    return fig


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
