import plotly.graph_objects as go 
import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd 
import json

from data.data_helpers import df_bnb
from PCP import DIMS, make_PCP
from Tree_map import create_treemap, tree

# Plot App
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Dash App Layout 
app.layout = html.Div(
    id='root',
    children=[

        # Left column
        html.Div(
            id='left-column', 
            children=[
                dcc.Dropdown(
                    id='PCP-dropdown',
                    options=['accuracy', 'checkin', 'cleanliness', 'communication', 'location', 'response rate', 'acceptance rate'],
                    value=['accuracy', 'communication', 'location'],
                    multi=True,
                    searchable=False,
                ),
                dcc.Slider(1, 4, 1,
                    value=3,
                    id='tree-map-slider'
                ),
            ],
        ),

        # Right column 
        html.Div(
            id='right-column', 
            children=[
                dcc.Graph(id='PCP'),
                html.P(id='Tree-map-title', children='Tree Map'),
                dcc.Graph(id='tree-map', figure=create_treemap(df_bnb.copy(), 4))
            ],
        ) 
    ]

)

# Callback function 
@app.callback(
    Output('PCP', 'figure'),
    Input('PCP-dropdown', 'value'),
)
def update_PCP(dropdown_value):
    features = [DIMS[feature] for feature in dropdown_value]
    
    # Plot the PCP
    fig = make_PCP(features, df_bnb)
    return fig 


@app.callback(
    Output('tree-map', 'figure'),
    Input('tree-map-slider', 'value')
)
def update_tree(value):
    tree.update_traces(maxdepth=value)
    return tree

app.run_server(debug=True, dev_tools_ui=False)
