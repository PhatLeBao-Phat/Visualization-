# I need os for folder magic
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

# Fast clean
data = data.replace("NaN", np.nan)
data = data.replace("nan", np.nan)

data = data.dropna(subset=["price", "review rate number", "room type", "neighbourhood group"])

def cleaning_price(price : str) -> int:
    return int(str(price).translate({ord('$'): None, ord(","): None}))

data["price"] = data["price"].apply(lambda x: cleaning_price(x))

from figure import FigureManager, CustomFigure
from graphs.map import figure as map_figure
from graphs.treemap import figure as treemap_figure
from filters.dropdown import DropDown
from filters.rangeslider import RangeSlider

import plotly.express as px
import plotly.graph_objects as go

import pandas as pd
import numpy as np
import json
 
from dash import html, Dash, ctx, dcc
from dash.dependencies import Input, Output, State

from typing import Union
from types import MethodType

import time

manager = FigureManager()
map = CustomFigure("map", "1")
map.assign_figure(map_figure)

treemap = CustomFigure("treemap", "1")
treemap.assign_figure(treemap_figure)
treemap.showed = ["neighbourhood group", "room type"]

filter_dropdowns = DropDown(data, "parameters_filter_dropdown", ["neighbourhood group", "room type", "Construction year"])
filter_rangesliders = RangeSlider(data, "parameters_filter_rangesliders", ["price", "review rate number"], [100, 1])

app = Dash(__name__)

app.layout = html.Div([
    dcc.Store(id="memory-graphs"),
    dcc.Store(id="memory-treemap"),
    map.html,
    html.Div([
        treemap.html,
        html.Pre(id="print")
    ], id="visualization-container"),
    html.Div([
        html.Div([
            dcc.Dropdown(
                data.columns,
                "neighbourhood group",
                id="clustering-key"
            ),
            html.Div(filter_dropdowns.children),
            html.Div(filter_rangesliders.children),
        ], id="menu-filter-container"),
        html.Div([
            html.Button(
                [html.I(className="open fa-solid fa-bars-staggered fa-2xl"), html.I(className="close fa-solid fa-xmark fa-2xl")],
                id="menu-button",
                n_clicks=0
                ),   
        ], id="menu-button-container")
    ], id="menu-container", **{"data-menu-toggle": "collapsed"})
])

# @app.callback(
#     Output("print", "children"),
#     Input("clustering-key", "value"),
#     Input("treemap-1", "clickData"),
#     Input("treemap-1", "selectedData"),
#     Input("memory-treemap", "data")
# )
# def to_print(blab, parameters_filter_dropdown, lolo, bla):
#     if parameters_filter_dropdown is None:
#         return None

#     return json.dumps(
#         {"lol": lol,
#         "selectedData": lol,
#         "derived": "nee",
#         "shit": bla
#         }
#         , indent=2)

# Menu
@app.callback(
    Output("menu-container", "data-menu-toggle"),
    Input("menu-button", "n_clicks"),
    Input("menu-container", "data-menu-toggle"),
    prevent_initial_call=True
)
def filter_dropdown(n_clicks, boolean):
    return "appear" if boolean == "collapsed" else "collapsed"

# All the inputs arrive here, data gets filtered and stored in a dict
@app.callback(
    Output("memory-graphs", "data"),
    filter_dropdowns.inputs,
    filter_rangesliders.inputs,
)
def filter_data(parameters_filter_dropdown, parameters_filter_rangeslider):
    query1 = ' & '.join(filter_dropdowns.conditions_func(list(parameters_filter_dropdown.values())[0]))
    query2 = " & ".join(filter_rangesliders.conditions_func(list(parameters_filter_rangeslider.values())[0]))
    query = " & ".join(["{}".format(query1), "{}".format(query2)])

    filtered = data.query(query)

    return filtered.to_dict('records')

# Store the data of clickData of treemap
@app.callback(
    Output("memory-treemap", "data"),
    Input("treemap-1", "clickData")
)
def highlight_map(clicked):
    if clicked is None:
        return None

    derived = clicked["points"][0]["customdata"]
    
    return ' & '.join(["({} == {})".format("`{}`".format(key), '"{}"'.format(elem)) for key, elem in zip(treemap.showed, derived) if elem != "(?)"])

@app.callback(
    map.output,
    Input("memory-graphs", "data"),
    Input("memory-treemap", "data"),
    Input("clustering-key", "value")
)
def update_map(filtered_dict, treemap_highlight, clustering_key = "neighbourhood group"):
    filtered = pd.DataFrame.from_records(filtered_dict)

    if treemap_highlight is not None:
        filtered.loc[filtered.query(treemap_highlight).index, clustering_key] = "highlighted"

    time.sleep(1)
    return (
        map.figure(filtered, clustering_key)
    )

@app.callback(
    treemap.output,
    Input("memory-graphs", "data"),
    Input("clustering-key", "value")
)
def update_map(filtered_dict, clustering_key = "neighbourhood group"):
    filtered = pd.DataFrame.from_records(filtered_dict)

    time.sleep(1)
    return (
        treemap.figure(filtered, clustering_key)
    )

app.run_server(debug=True)

value = "Brooklyn"
data.loc[data.query('`neighbourhood group` == @value').index, "neighbourhood group"] = "highlighted"
print(data["neighbourhood group"].unique())
print(data)



