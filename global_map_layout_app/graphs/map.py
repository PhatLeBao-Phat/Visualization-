# from color import color
import plotly.graph_objects as go


def figure(self, filtered_data, clustering_key, color_map):
    # Create map with the data
    # fig = px.scatter_mapbox(filtered_data, lat="lat", lon="long", color=filtered_data[clustering_key], custom_data={})
    # fig = px.scatter_mapbox(filtered_data, lat="lat", lon="long", color=clustering_key, color_discrete_sequence=px.colors.qualitative.G10, custom_data={})
    # fig = px.scatter_mapbox(filtered_data, lat="lat", lon="long", color=clustering_key, color_discrete_map=color(filtered_data, clustering_key), custom_data={})
    fig = px.scatter_mapbox(filtered_data, lat="latitude", lon="longitude", color=clustering_key, color_discrete_map=color_map, custom_data={})

    # Selected points get highlighted yellow and size of marks are 5
    for scatter in fig.data:
        scatter.marker.size = 5
        scatter.selected = {"marker": {"color": "yellow"}}

    fig.add_trace(go.Scattermapbox(
        lat = [40.8296, 40.7826, 40.6892, 40.704, 40.7580, 40.8506, 40.7126, 40.7484, 40.7593, 40.8972, 40.7400, 40.695],
        lon = [-73.9262, -73.9656, -74.0445, -73.9942, -73.9855, -73.8770, -74.0099, -73.9857, -73.9794, -73.8861, -73.8407, -73.866],
        mode = "markers",
        marker=go.scattermapbox.Marker(
            size=25,
            color='rgb(255, 0, 0)',
            opacity=0.3,
        ),
        text=["Yankee Stadium", "Central Park", "Statue of Liberty", "Brooklyn Bridge", "Times Squares", "Bronx Zoo", "World trade center", "Empire state building", "Top of the Rock", "Van Cortlandt Park", "Flushing Meadows Corona Park", "Forest Park"],
        name = "Tourist attractions"
    ))


    # Update layout to have a background. Zoom and center it in New York
    fig.update_layout(mapbox = {"style": "carto-positron", "zoom": 10, "center": {"lon": -73.96276, "lat": 40.68152}})
    fig.update_layout(margin={"r": 5, "t": 0, "l": 5, "b": 0})
    fig.update_layout(legend=dict(
        yanchor="top",
        y=1,
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
