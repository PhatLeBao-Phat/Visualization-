import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import html, Dash, ctx, dcc
from dash.dependencies import Input, Output, State
from typing import Union
from types import MethodType
from data.data_helpers import df_bnb
from graphs.PCP import DIMS, make_PCP
import time
import sklearn.cluster as sk_cluster

from color import color
from figure import FigureManager, CustomFigure
from graphs.map import figure as map_figure
from graphs.treemap import figure as treemap_figure
from filters.dropdown import DropDown
from filters.rangeslider import RangeSlider


# Add k-means to df_bnb columns
unique_k_means = list(df_bnb.copy().select_dtypes(include="number").drop(["latitude", "longitude"], axis=1).columns)
unique_k_means.sort()
df_bnb["k-means"] = 0

# Unique columns
columns = list(df_bnb.columns)
columns.sort()

# Create manager for the figures. Keeps track of the all the ids, inputs and outputs added
manager = FigureManager()

# Adds figure map
map = CustomFigure("map", "1")
# Assign the figure that generates map
map.assign_figure(map_figure)
# Assign information
map_information = html.Div([
    html.Pre("Controls of map include:"),
    html.Li("Selection with 'Box Select'. Top right corner"),
    html.Li("Hover over any point on map. Shows price, bedrooms and review rate + lat and long"),
    html.Li("When the cluster key is not numerical. The value of cluster is shown right of the hover label"),
    html.Li("Clicking traces in legend to hide or show traces. Bottom left corner"), 
    html.Li("Clicking the reset button. Resets selection on map"), 
])
map.assign_information(map_information)


# Adds figure treemap
treemap = CustomFigure("treemap", "1")
# Assign the figure that generates treemap
treemap.assign_figure(treemap_figure)
# Assign what can be selected as options
treemap.showed = ["neighbourhood_group_cleansed", "room_type", "price_cleansed", "bedrooms", "k-means"]
# Generates dropdown (dropdowns are currently hardcoded)

# Assign information
treemap_information = html.Div([
    html.Pre("Controls of treemap include:"),
    html.Li("Change any layer of the treemap via dropdowns"),
    html.Li("Clicking on any box in any layer"),
    html.Li("When clicked in, go to the left of the box and just above the box you can select 'All' which is hidden"),
])
treemap.assign_information(treemap_information)

# Adds figure PCP
pcp = CustomFigure("pcp", "1")
# Assign the figure that generates PCP
pcp.assign_figure(make_PCP)
# Assign information
pcp_information = html.Div([
    html.Pre("Controls of pcp include:"),
    html.Li("Add or remove 'parallel coordinates' via multi dropdown"),
    html.Li("Change the order of the 'parallel coordinate' by dragging the column names"),
    html.Li("On the parallel coordinates, click and drag down or up to highligh lines"),
    html.Li("When lines cross, it means negative correlation"),
    html.Li("When lines are parallel to each other, it means positive correlation"),
    html.Li("Correlation: mutual connection or linearly related"),
    html.Li("PCP is effective with less data")
])
pcp.assign_information(pcp_information)


# The general clustering_key for all visualizations (figures)
initial_clustering_key = "neighbourhood_group_cleansed"

# Generate a dropdown for each attribute mentioned
dropdown_filters = [
    "neighbourhood_group_cleansed",
    "room_type"
]
# Generates multi-choice dropdown menus
filter_dropdowns = DropDown(df_bnb, "parameters_filter_dropdown", dropdown_filters)

# Generate a rangeslider for each attribute mentioned
rangesliders_filters = [
    "price_cleansed",
    "review_scores_rating",
    "bedrooms",
]
# Generates rangesliders
filter_rangesliders = RangeSlider(df_bnb, "parameters_filter_rangesliders", rangesliders_filters)

# The app from Dash
app = Dash(__name__)

# The layout that will be generated in html
app.layout = html.Div([
    # Stores data filtered by all the filters
    dcc.Store(id="memory-graphs"),
    # Stores condition which to filter on based on what is clicked in treemap
    dcc.Store(id="memory-treemap"),
    # Stores the colormap from module color based on clustering_key
    dcc.Store(id="memory-colormap"), 
    # Stores condition which to filter on based on what is selected in map
    dcc.Store(id="memory-map"),
    
    # The html of map [Contains: Loading and graph]
    map.html,

    # The container for the treemap, PCP and title
    html.Div([
        # The title of our project
        html.Pre("AirBnb Hosts - JBI100 Dashboard", style={"font-size": 60, "text-align": "center", "padding": "20px"}),
        
        # Treemap container
        html.Div([
            # Container for all the dropdowns for each layer
            html.Div([
                # First layer
                html.Pre("First layer", className="treemap-dropdown-text"),
                dcc.Dropdown(
                    value = "neighbourhood_group_cleansed",
                    id="treemap-layer-1",
                    className="treemap-dropdown"
                ),

                # Second layer
                html.Pre("Second layer", className="treemap-dropdown-text"),
                dcc.Dropdown(
                    value = "room_type",
                    id="treemap-layer-2",
                    className="treemap-dropdown"
                ),

                # Third layer
                html.Pre("Third layer", className="treemap-dropdown-text"),
                dcc.Dropdown(
                    value = "bedrooms",
                    id="treemap-layer-3",
                    className="treemap-dropdown"
                )
            ], id="treemap-dropdowns-container"),

            # The html of treemap [Contains: Loading and graph]
            treemap.html,
        ]),

        # PCP container
        html.Div([
            # Multi variable dropdown which attribute to display in PCP
            dcc.Dropdown(
                id='PCP-dropdown',
                options=['accuracy', 'checkin', 'cleanliness', 'communication', 'location', 'response rate', 'acceptance rate'],
                value=['accuracy', 'communication', 'location'],
                multi=True,
                searchable=False,
            ),

            # The html of pcp [Contains: Loading and graph]
            pcp.html
        ]),
    ], id="visualization-container"),

    # Filter menu container
    html.Div([

        # Filters container
        html.Div([
            # The name
            html.Pre("Filter Menu", style={"font-size": 30, "text-align": "center"}),

            html.Pre("Clustering key selector. Decides coloring"),
            # Clustering_key dropdown
            dcc.Dropdown(
                columns,
                "neighbourhood_group_cleansed",
                id="clustering-key"
            ),

            # All the other before mentioned multi dropdowns
            html.Div(filter_dropdowns.children),

            # All the other before mentioned rangesliders
            html.Div(filter_rangesliders.children),

            # Button to turn off tourist attractions
            html.Pre("Show tourist attractions:"),
            html.Button(id="menu-filter-tourist-attractions", n_clicks=0, **{"data-menu-tourist-attractions": "False"}),

            html.Pre("K-means. Select k-means to activate"),
            # K-means slider. Range is 12 long as humans can max. see 12 colors differently at the same time
            html.Pre("Number of clusters"),
            dcc.Slider(1, 6, 1, value = 2, id="slider-k-means"),

            # K-means multi dropdown
            html.Pre("Attributes to compute k-means"),
            dcc.Dropdown(unique_k_means, unique_k_means, id="dropdown-k-means", multi=True),
        ], id="menu-filter-container"),

        # Menu Button container
        html.Div([
            # The Button to toggle the information on or off
            html.Button(
                # Contains the informatio icon
                [html.I(className="open fa-solid fa-info fa-2xl"), html.I(className="close fa-solid fa-circle-info fa-2xl")],
                id="information-button",
                className="menu-button",
                n_clicks=0
            ),

            # The Button to toggle the filter menu on or off
            html.Button(
                # Contains icons for open and closed. Open gives the three bars and closed gives a cross
                [html.I(className="open fa-solid fa-bars-staggered fa-2xl"), html.I(className="close fa-solid fa-xmark fa-2xl")],
                id="menu-button",
                className="menu-button",
                n_clicks=0
            ),   

            # The Button to reset all parameters and data
            html.Button(
                # Contains the reset icon
                html.I(className="reset fa-solid fa-arrow-rotate-right fa-2xl"),
                id="menu-reset-button",
                className="menu-button",
                n_clicks=0
            ),

            html.Div([
                html.Button([
                    html.I(className="fa-solid fa-arrows-to-eye fa-2xl"),
                ], id="menu-blindness-button", className="menu-button", n_clicks=0),

                html.Div([
                    # No Green
                    html.Button(
                        # Contains icons for open and closed. Open gives the three bars and closed gives a cross
                        [html.I(className="open fa-solid fa-eye fa-2xl"), html.I(className="close fa-solid fa-eye-dropper fa-2xl")],
                        id="menu-blindness-button-green",
                        className="menu-button coloring",
                        n_clicks=0,
                    ),

                    # No Red
                    html.Button(
                        # Contains icons for open and closed. Open gives the three bars and closed gives a cross
                        [html.I(className="open fa-solid fa-eye fa-2xl"), html.I(className="close fa-solid fa-eye-dropper fa-2xl")],
                        id="menu-blindness-button-red",
                        className="menu-button coloring",
                        n_clicks=0,
                    ),

                    # No Blue
                    html.Button(
                        # Contains icons for open and closed. Open gives the three bars and closed gives a cross
                        [html.I(className="open fa-solid fa-eye fa-2xl"), html.I(className="close fa-solid fa-eye-dropper fa-2xl")],
                        id="menu-blindness-button-blue",
                        className="menu-button coloring",
                        n_clicks=0,
                    ),

                    # Normal
                    html.Button(
                        # Contains icons for open and closed. Open gives the three bars and closed gives a cross
                        [html.I(className="open fa-solid fa-eye fa-2xl"), html.I(className="close fa-solid fa-eye-dropper fa-2xl")],
                        id="menu-blindness-button-normal",
                        className="menu-button coloring",
                        n_clicks=0,
                    ),

                    html.Pre("Deuteranopia"),
                    html.Pre("Protanopia"),
                    html.Pre("Tritanopia"),
                    html.Pre("Normal"),
                ]),
            ], id="menu-blindness-button-container", **{"data-show-coloring": "hide"}),
        ], id="menu-button-container")
    ], id="menu-container", **{"data-menu-toggle": "collapsed"})
], id="layout", **{"data-information": "hide", "data-color": "Normal"})

# Toggle for information overlay
@app.callback(
    Output("layout", "data-information"),
    Input("information-button", "n_clicks"),
    Input("layout", "data-information"),
    prevent_initial_call=True
)
def update_info(n_clicks, data):
    return "show" if data == "hide" else "hide"

# Hide or Show coloring blindness menu
@app.callback(
    Output("menu-blindness-button-container", "data-show-coloring"),
    Input("menu-blindness-button", "n_clicks"),
    Input("menu-blindness-button-container", "data-show-coloring"),
    prevent_initial_call=True
)
def update_coloring(n_clicks, data):
    return "show" if data == "hide" else "hide"

# Color blindness buttons
@app.callback(
    Output("layout", "data-color"),
    Input("menu-blindness-button-green", "n_clicks"),
    Input("menu-blindness-button-red", "n_clicks"),
    Input("menu-blindness-button-blue", "n_clicks"),
    Input("menu-blindness-button-normal", "n_clicks"),
    prevent_initial_call=True
)
def update_blindness(*args):
    if ctx.triggered[0]["prop_id"].split(".")[0] == "menu-blindness-button-green":
        return "No Green"
    if ctx.triggered[0]["prop_id"].split(".")[0] == "menu-blindness-button-red":
        return "No Red"
    if ctx.triggered[0]["prop_id"].split(".")[0] == "menu-blindness-button-blue":
        return "No Blue"
    if ctx.triggered[0]["prop_id"].split(".")[0] == "menu-blindness-button-normal":
        return "Normal"

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
    Input("slider-k-means", "value"),
    Input("dropdown-k-means", "value")
)
def filter_data(parameters_filter_dropdown, parameters_filter_rangeslider, k_clusters = 3, k_dropdowns = ["bedrooms"]):
    query1 = ' & '.join(filter_dropdowns.conditions_func(list(parameters_filter_dropdown.values())[0]))
    query2 = " & ".join(filter_rangesliders.conditions_func(list(parameters_filter_rangeslider.values())[0]))
    query = " & ".join(["{}".format(query1), "{}".format(query2)])
    filtered = df_bnb.query(query)

    # K-means
    k_means = sk_cluster.KMeans(n_clusters = k_clusters)

    # altered = filtered.copy().select_dtypes(include="number").drop(["latitude", "longitude"], axis=1)
    altered = filtered[k_dropdowns]
    altered = altered.fillna(0)

    predicted = k_means.fit_predict(altered)
    filtered["k-means"] = predicted.astype(str)

    return filtered.to_dict('records')

# Store the data of clickData of treemap
@app.callback(
    Output("memory-treemap", "data"),
    Input("treemap-1", "clickData"),
    Input("clustering-key", "value"),
    Input("menu-reset-button", "n_clicks"),
    Input("treemap-layer-1", "value"),
    Input("treemap-layer-2", "value"),
    Input("treemap-layer-3", "value"),
)
def highlight_map(clicked, clustering_key, reset, *args):
    if clicked is None:
        return None

    if ctx.triggered[0]["prop_id"].split(".")[0] == "menu-reset-button":
        return None

    # Remove selection when color change
    if ctx.triggered[0]["prop_id"].split(".")[0] in ["clustering-key", "treemap-layer-1", "treemap-layer-2", "treemap-layer-3"]:
        return None

    try:
        derived = clicked["points"][0]["customdata"]
    except:
        return None

    return ' & '.join(["({} == {})".format("`{}`".format(key), '"{}"'.format(elem) if type(elem) == str else elem) for key, elem in zip(args, derived) if elem != "(?)"])

# Store the colormap
@app.callback(
    Output("memory-colormap", "data"),
    Input("memory-graphs", "data"),
    Input("clustering-key", "value"),
    Input("layout", "data-color")
)
def update_colormap(filtered_dict, clustering_key, coloring):
    filtered = pd.DataFrame.from_records(filtered_dict)
    print(coloring)
    return color(filtered, clustering_key, coloring)

# Store the selection on the map
@app.callback(
    Output("memory-map", "data"),
    Input("memory-map", "data"),
    Input("map-1", "selectedData"),
    Input("menu-reset-button", "n_clicks")
)
def highlight_map(prev_selected, selected, reset):
    if ctx.triggered[0]["prop_id"].split(".")[0] == "menu-reset-button":
        return None

    if selected is None:
        return prev_selected

    right_bottom_y = selected["range"]["mapbox"][0][0]
    right_bottom_x = selected["range"]["mapbox"][0][1]
    left_top_y = selected["range"]["mapbox"][1][0]
    left_top_x = selected["range"]["mapbox"][1][1]

    return "((longitude > {}) & (latitude < {}) & (longitude < {}) & (latitude > {}))".format(right_bottom_y, right_bottom_x, left_top_y, left_top_x)

# Menu button to show tourist attraction
@app.callback(
    Output("menu-filter-tourist-attractions", "data-menu-tourist-attractions"),
    Input("menu-filter-tourist-attractions", "n_clicks"),
    Input("menu-filter-tourist-attractions", "data-menu-tourist-attractions"),
    prevent_initial_call=True
)
def update_tourist_attractions(n_clicks, boolean):
    return "False" if boolean == "True" else "True"

@app.callback(
    map.output,
    Input("memory-graphs", "data"),
    Input("memory-treemap", "data"),
    Input("memory-colormap", "data"),
    Input("memory-map", "data"),
    Input("menu-filter-tourist-attractions", "data-menu-tourist-attractions"), 
    Input("clustering-key", "value"),
)
def update_map(filtered_dict, treemap_highlight, color_map, selected, tourist_boolean, clustering_key = initial_clustering_key):
    filtered = pd.DataFrame.from_records(filtered_dict)

    if selected is not None:
        filtered = filtered.query(selected)

    if treemap_highlight is not None:
        filtered = filtered.query(treemap_highlight)

    time.sleep(1)
    return (
        map.figure(filtered, clustering_key, color_map, tourist_boolean)
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
def update_map(filtered_dict, color_map, selected, v1, v2, v3, clustering_key = initial_clustering_key):
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
    Input("memory-colormap", "data"),
    Input("memory-treemap", "data"),
    Input("memory-map", "data"),
    Input('PCP-dropdown', 'value'),
    Input("clustering-key", "value")
)
def update_map(filtered_dict, color_map, treemap_highlight, selected, features, clustering_key = initial_clustering_key):
    filtered = pd.DataFrame.from_records(filtered_dict)
    # features = [DIMS[feature] for feature in features]

    if selected is not None:
        filtered = filtered.query(selected)

    if treemap_highlight is not None:
        filtered = filtered.query(treemap_highlight)

    time.sleep(1)
    return (
        pcp.figure(features, filtered, color_map, clustering_key)
    )

@app.callback(
    filter_rangesliders.histogram_output,
    Input("memory-graphs", "data"),
    Input("memory-colormap", "data"),
    Input("memory-treemap", "data"),
    Input("memory-map", "data"),
    Input("clustering-key", "value")
)
def update_map(filtered_dict, color_map, treemap_highlight, selected, clustering = initial_clustering_key):
    filtered = pd.DataFrame.from_records(filtered_dict)

    if selected is not None:
        filtered = filtered.query(selected)

    if treemap_highlight is not None:
        filtered = filtered.query(treemap_highlight)

    return filter_rangesliders.histogram_figures(filtered, clustering, color_map)

app.run_server(debug=True, dev_tools_ui=False)





