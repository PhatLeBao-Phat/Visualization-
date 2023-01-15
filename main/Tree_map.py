import plotly.graph_objects as go 
from plotly.subplots import make_subplots 
import pandas as pd 
import numpy as np 
import plotly.express as px

from data.data_helpers import df_bnb

df = df_bnb.copy()

def create_treemap(df, max_depth):
    fig = px.treemap(
        data_frame = df, 
        path=['all', 'neighbourhood_group_cleansed', 'host_is_superhost_cleansed', 'room_type'],
        values='num_count',
        color='price_cleansed',
        color_continuous_scale=px.colors.sequential.RdBu,
        maxdepth=max_depth,
    )
    fig.update_traces(root_color="lightgrey")
    fig.update_layout(dict(
        # paper_bgcolor='black',
        title=dict(
            xanchor='center',
            xref='container'
        ),
        # shapes=[
        #     {   "type": "rect",
        #         "xref": "paper",
        #         "yref": "paper",
        #         "x0": 0,
        #         "y0": 0,
        #         "x1": 1,
        #         "y1": 1,
        #     }
        # ],
        margin=dict(t=10, l=25, r=25, b=25),
        coloraxis_showscale=True,
        coloraxis=dict(
            colorbar=dict(
                title='Price ($)'
            )
        )
    ))

    return fig 

tree = create_treemap(df_bnb, 4)