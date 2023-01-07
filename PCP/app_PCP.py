import plotly.graph_objects as go 
import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd 
import dash_bootstrap_components as dbc
import json

from data import df_plot, df_bnb
from PCP import DIMS, make_PCP
from Dropdown import create_dropdown
from scatterplot import fig_scatter, fig_scatter2

# Plot App 
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dash App Layout 
app.layout = html.Div(
    id='root',
    children=[
        # Left column
        html.Div(
            id='left-column',
            children=[
                html.P(
                    id='title_sidebar',
                    children=['Side Bar'],
                ),
                html.Hr(className='hr', id='dcmwhy'),
                html.P(["Choose the feature for PCP"]),
                create_dropdown(),
                html.Pre(
                    id='structure1',
                    className='print-out',
                ),
                html.Pre(
                    id='structure2',
                    className='print-out',
                ),
            ], 
        ),

        # Right column 
        html.Div(
            id='right-column',
            children=[
                dcc.Graph(id='demo-PCP'),
                dcc.Graph(id='demo-scatter', figure=fig_scatter),
                dcc.Graph(id='demo-scatter2', figure=fig_scatter2)
            ],
        ),
    ],
)


# Callback function 
@app.callback(
    Output('demo-PCP', 'figure'),
    Input('demo-dropdown', 'value'),
    Input('demo-scatter', 'selectedData'),
)
def update_PCP(dropdown_value, selected_data):
    features = [DIMS[feature] for feature in dropdown_value]

    if selected_data is None:
        selected_index = df_plot.index  # show all
    else:
        selected_index = [  # show only selected indices
            x.get('pointIndex', None) for x in selected_data['points']
        ]
    
    # Plot the PCP
    fig = make_PCP(features, df_plot)
    return fig 


# Linking between scatterplot
@app.callback(
    Output('demo-scatter2', 'figure'),
    Input('demo-scatter', 'selectedData)')
)
def update_scatter2(selected_data):
    if selected_data is None:
        selected_index = df_plot.index  # show all
    else:
        selected_index = [  # show only selected indices
            x.get('pointIndex', None) for x in selected_data['points']
        ]
    fig = fig_scatter2
    fig.data[0].update(
            selectedpoints=selected_index,

            # color of selected points
            selected=dict(marker=dict(color='orange')),

            # color of unselected pts
            unselected=dict(marker=dict(color='rgb(200,200,200)', opacity=0.9))
        )

    return fig 


@app.callback(
    Output('structure1', 'children'),
    Output('structure2', 'children'),
    Input('demo-scatter', 'selectedData'),
)
def print_out(selectedData):
    if selectedData is None:
        selected_index = df_plot.index  # show all
    else:
        selected_index = [  # show only selected indices
            x.get('pointIndex', None) for x in selectedData['points']
        ]
    fuc = str(type(selected_index))

    return json.dumps(selectedData, indent=2), fuc

app.run_server(debug=True, dev_tools_ui=False)  # Turn off reloader if inside Jupyter

    