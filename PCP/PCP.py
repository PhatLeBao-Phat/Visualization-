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

