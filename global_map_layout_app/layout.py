from figure import FigureManager, CustomFigure
from graphs.map import figure as map_figure
from graphs.treemap import figure as treemap_figure
from filters.dropdown import DropDown
from filters.rangeslider import RangeSlider
from color import color

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

from data.data_helpers import df_bnb
from graphs.PCP import DIMS, make_PCP

import time

import plotly.io as io
io.templates.default = "simple_white"

manager = FigureManager()

map = CustomFigure("map", "1")
map.assign_figure(map_figure)

treemap = CustomFigure("treemap", "1")
treemap.assign_figure(treemap_figure)
treemap.showed = ["neighbourhood_group_cleansed", "room_type", "price_cleansed", "bedrooms"]

pcp = CustomFigure("pcp", "1")
pcp.assign_figure(make_PCP)

filter_dropdowns = DropDown(df_bnb, "parameters_filter_dropdown", ["neighbourhood_group_cleansed", "room_type"])
rangesliders_filters = [
    "price_cleansed",
    "review_scores_rating",
    "bedrooms",
]
filter_rangesliders = RangeSlider(df_bnb, "parameters_filter_rangesliders", rangesliders_filters, [100, 1])

app = Dash(__name__)

app.layout = html.Div([
    dcc.Store(id="memory-graphs"),
    dcc.Store(id="memory-treemap"),
    dcc.Store(id="memory-colormap"),
    dcc.Store(id="memory-map"),
    map.html,
    html.Div([
        html.Pre("AirBnb Hosts - JBI100 Dashboard", style={"font-size": 60, "text-align": "center", "padding": "20px"}),
        html.Div([
            html.Div([
                html.Pre("First layer", className="treemap-dropdown-text"),
                dcc.Dropdown(
                    value = "neighbourhood_group_cleansed",
                    id="treemap-layer-1",
                    className="treemap-dropdown"
                ),
                html.Pre("Second layer", className="treemap-dropdown-text"),
                dcc.Dropdown(
                    value = "room_type",
                    id="treemap-layer-2",
                    className="treemap-dropdown"
                ),
                html.Pre("Third layer", className="treemap-dropdown-text"),
                dcc.Dropdown(
                    value = "bedrooms",
                    id="treemap-layer-3",
                    className="treemap-dropdown"
                )
            ], id="treemap-dropdowns-container"),
            treemap.html,
        ]),
        html.Div([
            dcc.Dropdown(
                id='PCP-dropdown',
                options=['accuracy', 'checkin', 'cleanliness', 'communication', 'location', 'response rate', 'acceptance rate'],
                value=['accuracy', 'communication', 'location'],
                multi=True,
                searchable=False,
            ),
            pcp.html
        ]),
        # html.Pre(id="print")
    ], id="visualization-container"),
    html.Div([
        html.Div([
            dcc.Dropdown(
                df_bnb.columns,
                "neighbourhood_group_cleansed",
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
#     Input("treemap-1", "clickData"),
# )
# def to_print(selected):

#     return json.dumps(
#         {
#             # "selected": selected,
#             "data": selected
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

    filtered = df_bnb.query(query)

    return filtered.to_dict('records')

# Keep the treemap clickData the same


# Store the data of clickData of treemap
@app.callback(
    Output("memory-treemap", "data"),
    Input("treemap-1", "clickData"),
    Input("clustering-key", "value"),
    Input("map-1", "selectedData"),
    Input("treemap-layer-1", "value"),
    Input("treemap-layer-2", "value"),
    Input("treemap-layer-3", "value"),
)
def highlight_map(clicked, clustering_key, selected, *args):
    if clicked is None:
        return None

    # # Remove selection when selected
    # if selected is not None:
    #     return None

    # Remove selection when color change
    if ctx.triggered[0]["prop_id"].split(".")[0] == "clustering-key":
        return None

    try:
        derived = clicked["points"][0]["customdata"]
    except:
        return None
    
    print(' & '.join(["({} == {})".format("`{}`".format(key), '"{}"'.format(elem) if type(elem) == str else elem) for key, elem in zip(args, derived) if elem != "(?)"]))

    return ' & '.join(["({} == {})".format("`{}`".format(key), '"{}"'.format(elem) if type(elem) == str else elem) for key, elem in zip(args, derived) if elem != "(?)"])

# Store the colormap
@app.callback(
    Output("memory-colormap", "data"),
    Input("memory-graphs", "data"),
    Input("clustering-key", "value")
)
def update_colormap(filtered_dict, clustering_key):
    filtered = pd.DataFrame.from_records(filtered_dict)
    return color(filtered, clustering_key)

# Store the selection on the map
@app.callback(
    Output("memory-map", "data"),
    Input("memory-map", "data"),
    Input("map-1", "selectedData"),
    Input("clustering-key", "value")
)
def highlight_map(prev_selected, selected, clustering_key):
    if selected is None:
        return prev_selected

    # # Remove selection when color change
    # if ctx.triggered[0]["prop_id"].split(".")[0] == "clustering-key":
    #     return None

    right_bottom_y = selected["range"]["mapbox"][0][0]
    right_bottom_x = selected["range"]["mapbox"][0][1]
    left_top_y = selected["range"]["mapbox"][1][0]
    left_top_x = selected["range"]["mapbox"][1][1]
    # data_bool = (data["long"] > right_bottom[0]) & (data["lat"] < right_bottom[1]) & (data["long"] < left_top[0]) & (data["lat"] > left_top[1])

    return "((longitude > {}) & (latitude < {}) & (longitude < {}) & (latitude > {}))".format(right_bottom_y, right_bottom_x, left_top_y, left_top_x)


@app.callback(
    map.output,
    Input("memory-graphs", "data"),
    Input("memory-treemap", "data"),
    Input("memory-colormap", "data"),
    Input("memory-map", "data"),
    Input("clustering-key", "value"),
)
def update_map(filtered_dict, treemap_highlight, color_map, selected, clustering_key = "neighbourhood group"):
    filtered = pd.DataFrame.from_records(filtered_dict)

    if selected is not None:
        filtered = filtered.query(selected)
        # filtered.loc[filtered.query(selected).index, clustering_key] = "selected"

    if treemap_highlight is not None:
        # filtered.loc[filtered.query(treemap_highlight).index, clustering_key] = "highlighted"
        filtered = filtered.query(treemap_highlight)

    time.sleep(1)
    return (
        map.figure(filtered, clustering_key, color_map)
    )

@app.callback(
    treemap.output,
    Input("memory-graphs", "data"),
    Input("memory-colormap", "data"),
    Input("memory-map", "data"),
    Input("treemap-layer-1", "value"),
    Input("treemap-layer-2", "value"),
    Input("treemap-layer-3", "value"),
    Input("clustering-key", "value")
)
def update_map(filtered_dict, color_map, selected, v1, v2, v3, clustering_key = "neighbourhood group"):
    filtered = pd.DataFrame.from_records(filtered_dict)

    if selected is not None:
        filtered = filtered.query(selected)

    time.sleep(1)
    return (
        treemap.figure(filtered, clustering_key, color_map, path = [v1, v2, v3])
    )

@app.callback(
    Output("treemap-layer-1", "options"),
    Output("treemap-layer-2", "options"),
    Output("treemap-layer-3", "options"),
    Input("treemap-layer-1", "value"),
    Input("treemap-layer-2", "value"),
    Input("treemap-layer-3", "value"),
)
def update_treemap_options(v1, v2, v3):
    options = treemap.showed.copy()
    return (
        [option for option in options if v2 != option if v3 != option],
        [option for option in options if v1 != option if v3 != option],
        [option for option in options if v1 != option if v2 != option],
)

@app.callback(
    pcp.output,
    Input("memory-graphs", "data"),
    Input("memory-treemap", "data"),
    Input("memory-map", "data"),
    Input('PCP-dropdown', 'value'),
    Input("clustering-key", "value")
)
def update_map(filtered_dict, treemap_highlight, selected, dropdown_value, clustering_key = "neighbourhood group"):
    filtered = pd.DataFrame.from_records(filtered_dict)
    features = [DIMS[feature] for feature in dropdown_value]

    if selected is not None:
        filtered = filtered.query(selected)

    if treemap_highlight is not None:
        filtered = filtered.query(treemap_highlight)

    time.sleep(1)
    return (
        pcp.figure(features, filtered)#, clustering_key)
        # make_PCP(features, filtered)#, clustering_key)
    )

@app.callback(
    filter_rangesliders.histogram_output,
    Input("memory-graphs", "data"),
    Input("memory-treemap", "data"),
    Input("memory-map", "data"),
)
def update_map(filtered_dict, treemap_highlight, selected):
    filtered = pd.DataFrame.from_records(filtered_dict)

    if selected is not None:
        filtered = filtered.query(selected)

    if treemap_highlight is not None:
        filtered = filtered.query(treemap_highlight)

    return filter_rangesliders.histogram_figures(filtered)

app.run_server(debug=True)

value = "Brooklyn"
df_bnb.loc[df_bnb.query('`neighbourhood group` == @value').index, "neighbourhood group"] = "highlighted"
print(df_bnb["neighbourhood group"].unique())
print(df_bnb)





