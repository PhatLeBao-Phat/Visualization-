import plotly.graph_objects as go 
import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd 

from data import df_plot, df_bnb
from PCP import DIMS


# Plot App 
app = Dash(__name__)


# Dash App Layout 
app.layout = html.Div(
    children=[
    # Left column
    html.Div([
        dcc.Dropdown(
        options=['accuracy', 'checkin', 'cleanliness', 'communication', 'location'],
        value=['accuracy', 'communication', 'location'],
        multi=True,
        id='demo-dropdown',
        searchable=False,
        style={'font-size': 13}
        ),
        html.Hr(),
    ], 
    style={'padding': 20, 'flex': 1}
    ),

    # Right column 
    html.Div([
        dcc.Graph(id='demo-graph'),
        ])
    ],
    style={'display': 'flex', 'flex-direction': 'row'},
    )


# Callback function 
@app.callback(
    Output('demo-graph', 'figure'),
    Input('demo-dropdown', 'value')
)
def update_graph(dropdown_value):
    features = [DIMS[feature] for feature in dropdown_value]
    
    # Plot the fig 
    fig = go.Figure(
        data=go.Parcoords(
            line = dict(color = df_plot['review_scores_rating'],
                    colorscale = 'Electric',
                    showscale = True,
                    #    cmin = -4000,
                    #    cmax = -100
                ),
            dimensions = features,
            unselected = dict(line = dict(color = 'gray', opacity = 0.5)),
        )
    )
    
    fig.update_layout(
        plot_bgcolor = 'white',
        paper_bgcolor = 'white',
        title=dict(
            text='Principle Components Plot',
            xanchor='left'
        )

    )
    return fig 


app.run_server(debug=True, dev_tools_ui=False)  # Turn off reloader if inside Jupyter
