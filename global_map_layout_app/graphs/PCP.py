import pandas as pd 
import numpy as np 
import plotly.graph_objects as go 

from data.data_helpers import PATH, FEATURES, df_bnb

DIMS = {
    'accuracy' : go.parcoords.Dimension(
        label = 'accuracy',
        values = df_bnb['review_scores_accuracy'],
        range=[0, 5],
    ),
    'cleanliness' : go.parcoords.Dimension(
        label = 'cleanliness',
        values = df_bnb['review_scores_cleanliness'],
        range=[0, 5],
    ),
    'checkin' : go.parcoords.Dimension(
        label = 'checkin',
        values = df_bnb['review_scores_checkin'],
        range=[0, 5],
    ),
    'communication' : go.parcoords.Dimension(
        label = 'communication',
        values = df_bnb['review_scores_communication'],
        range=[0, 5],
    ),
    'location' : go.parcoords.Dimension(
        label = 'location',
        values = df_bnb['review_scores_location'],
        range=[0, 5],
    ),
    'response rate' : go.parcoords.Dimension(
        label = 'response rate (%)',
        values = df_bnb['host_response_rate_cleansed'],
        range=[0, 100],
    ),
    'acceptance rate' : go.parcoords.Dimension(
        label = 'acceptance rate (%)',
        values = df_bnb['host_acceptance_rate_cleansed'],
        range=[0, 100],
    )
}

reverse_DIMS = {
    'accuracy':'review_scores_accuracy', 
    'checkin':'review_scores_cleanliness', 
    'cleanliness':'review_scores_checkin', 
    'communication':'review_scores_communication', 
    'location':'review_scores_location', 
    'response rate':'host_response_rate_cleansed', 
    'acceptance rate':'host_acceptance_rate_cleansed'
}

def make_PCP(features, df, color='review_scores_rating'):
    df_bnb = df.copy()
    customdata = list(
        zip(
            df_bnb['host_response_rate'],
            df_bnb['accommodates'],
            df_bnb['bedrooms'],
        )
    )

    PCP_figure = dict(
        type='parcoords',
        line=dict(
            color=df_bnb[color],
            colorscale='Electric',
            showscale=True,

        ),
        dimensions=features,
        unselected=dict(line = dict(color = 'gray', opacity = 0.3)),
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

