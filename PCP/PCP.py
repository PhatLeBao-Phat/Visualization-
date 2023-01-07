import pandas as pd 
import numpy as np 
import plotly.graph_objects as go 

from data import PATH, FEATURES, df_plot, df_bnb

DIMS = {
        'accuracy' : go.parcoords.Dimension(
            label = 'accuracy',
            values = df_plot['review_scores_accuracy']
            ),
        'cleanliness' : go.parcoords.Dimension(
            label = 'cleanliness',
                values = df_plot['review_scores_cleanliness']
                ),
        'checkin' : go.parcoords.Dimension(
            label = 'checkin',
            values = df_plot['review_scores_checkin']
            ),
        'communication' : go.parcoords.Dimension(
            label = 'communication',
            values = df_plot['review_scores_communication']
            ),
        'location' : go.parcoords.Dimension(
            label = 'location',
            values = df_plot['review_scores_location']
            ),
    }

def make_PCP(features, df):
    df_plot = df.copy()
    customdata = list(
        zip(
            df_plot['host_response_rate'],
            df_plot['accommodates'],
            df_plot['bedrooms'],
        )
    )

    PCP_figure = dict(
        type='parcoords',
        line=dict(
            color=df_plot['review_scores_rating'],
            colorscale='Electric',
            showscale=True,

        ),
        dimensions=features,
        unselected=dict(line = dict(color = 'gray', opacity = 0.5)),
        customdata=customdata,
    )

    layout = dict(
        PCP=dict(

        ),
        plot_bgcolor= 'white',
        paper_bgcolor= 'white',
        title=dict(
            color='black',
            text='Principle Components Plot',
            xanchor='center',
            xref='contrainer'
        ),
        shapes=[
            {   "type": "rect",
                "xref": "paper",
                "yref": "paper",
                "x0": 0,
                "y0": 0,
                "x1": 1,
                "y1": 1,
                "line": {"width": 1, "color": "#B0BEC5"},
                "visible": True
            }
        ],
        # margin=dict(l=5, t=30, b=20, r=5),
        # height=300,
        showlegend=True,
        hovermode="x",
    )
    
    figure = dict(
        data=[PCP_figure], 
        layout=layout,
    )
    return figure 

