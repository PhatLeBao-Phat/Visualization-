import plotly.express as px
import plotly.graph_objects as go 
import dash
from dash import Dash, dcc, html, Input, Output
import pandas as pd 
import dash_bootstrap_components as dbc
import json



def get_data():
    # Read data
    df = px.data.iris()

    # Any further data preprocessing can go her

    return df

df = get_data()
print(df)

fig_scatter = go.Figure()

fig_scatter.add_trace(
    go.Scatter(
        x=df['sepal_length'],
        y=df['sepal_width'],
        mode='markers',
    ),
)

fig_scatter2 = go.Figure()
fig_scatter2.add_trace(
    go.Scatter(
        x=df['petal_width'],
        y=df['petal_length'],
        mode='markers',
    ),
)
print(fig_scatter.data[0])
print(type(fig_scatter.data[0]))
app = Dash(__name__)

app.layout = html.Div(
    children=[
        dcc.Graph(id='fig1', figure=fig_scatter),
        dcc.Graph(id='fig2', figure=fig_scatter2),
    ]
)

@app.callback(
    Output('fig1', 'figure'),
    Input('fig2', 'selectedData')
)
def update(selected_data):
    if selected_data is None:
        selected_index = df.index  # show all
    else:
        selected_index = [  # show only selected indices
            x.get('pointIndex', None) for x in selected_data['points']
        ]
    fig_scatter = go.Figure()

    fig_scatter.add_trace(
        go.Scatter(
            x=df['sepal_length'],
            y=df['sepal_width'],
            mode='markers',
            selectedpoints=selected_index,
            selected=dict(marker=dict(color='orange')),
            unselected=dict(marker=dict(color='rgb(200,200,200)', opacity=0.9))
        ),
    )
    
    return fig_scatter

app.run_server(debug=True, dev_tools_ui=False)