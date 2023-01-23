import pandas as pd 
import numpy as np 
import plotly.graph_objects as go 
import plotly.express as px

from data.data_helpers import PATH, FEATURES, df_bnb

DIMS = {
    'accuracy' : go.parcoords.Dimension(
        label = 'accuracy',
        values = df_bnb['review_scores_accuracy'],
        range=[0, 5],
        constraintrange=[0, 5],
    ),
    'cleanliness' : go.parcoords.Dimension(
        label = 'cleanliness',
        values = df_bnb['review_scores_cleanliness'],
        range=[0, 5],
        constraintrange=[0, 5],
    ),
    'checkin' : go.parcoords.Dimension(
        label = 'checkin',
        values = df_bnb['review_scores_checkin'],
        range=[0, 5],
        constraintrange=[0, 5],
    ),
    'communication' : go.parcoords.Dimension(
        label = 'communication',
        values = df_bnb['review_scores_communication'],
        range=[0, 5],
        constraintrange=[0, 5],
    ),
    'location' : go.parcoords.Dimension(
        label = 'location',
        values = df_bnb['review_scores_location'],
        range=[0, 5],
        constraintrange=[0, 5],
    ),
    'response rate' : go.parcoords.Dimension(
        label = 'response rate (%)',
        values = df_bnb['host_response_rate_cleansed'],
        range=[0, 100],
        constraintrange=[0, 100],
    ),
    'acceptance rate' : go.parcoords.Dimension(
        label = 'acceptance rate (%)',
        values = df_bnb['host_acceptance_rate_cleansed'],
        range=[0, 100],
        constraintrange=[0, 100],
    ),
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

# def make_PCP(self, features, filtered, color_map, color):
#     # Make dummies
#     dummify = color
#     dfg = pd.DataFrame({dummify:df_bnb[dummify].unique()})
#     dfg['dummy'] = dfg.index
#     filtered = pd.merge(filtered, dfg, on = dummify, how='left')

#     # Color map into list
#     color_list = []
#     for key, value in color_map.items():
#         if key in list(filtered[color].unique()):
#             color_list.append(value)

#     # Makes sure when only one category it does not give an error
#     if len(color_list) == 1:
#         color_list.append(color_list[0])

#     PCP_figure = dict(
#         type='parcoords',
#         line=dict(
#             # Put in dummy for categorical data 
#             color=filtered["dummy"],

#             # Only put in the color for each attributes present
#             colorscale=color_list
#         ),
#         # Set the parallel coords featured
#         dimensions=features,

#         # When selection, not selected
#         unselected=dict(line = dict(color = 'gray', opacity = 0.3))
#     )

#     layout = dict(
#         PCP=dict(

#         ),
#         # Less white space
#         margin={"r": 5, "t": 40, "l": 30, "b": 10},

#         # Make background white
#         plot_bgcolor= 'white',
#         paper_bgcolor= 'white',

#         # The rest
#         shapes=[
#             {   "type": "rect",
#                 "xref": "paper",
#                 "yref": "paper",
#                 "x0": 0,
#                 "y0": 0,
#                 "x1": 1,
#                 "y1": 1,
#                 "line": {"width": 1, "color": "#B0BEC5"},
#                 "visible": True
#             }
#         ],
#         showlegend=True,
#         hovermode="x",
#     )

#     # Put into a figure
#     figure = dict(
#         data=[PCP_figure], 
#         layout=layout,
#     )

#     return figure 

def make_PCP(self, features, filtered, color_map, color):
    features = [reverse_DIMS[feature] for feature in features]

    # Make dummies
    dummify = color

    if color == 'k-means':
        dfg = pd.DataFrame({dummify:filtered[dummify].unique()})
        dfg['dummy'] = dfg.index
        filtered = pd.merge(filtered, dfg, on = dummify, how='left')
    else:
        dfg = pd.DataFrame({dummify:df_bnb[dummify].unique()})
        dfg['dummy'] = dfg.index
        filtered = pd.merge(filtered, dfg, on = dummify, how='left')


    # If it is a sequential color_map then skip the code underneath
    if type(color_map) != list:
        # Color map into list
        color_list = []
        for key, value in color_map.items():
            if key in list(filtered[color].unique()):
                color_list.append(value)

        # Makes sure when only one category it does not give an error
        if len(color_list) == 1:
            color_list.append(color_list[0])
    else:
        color_list = color_map

    fig = px.parallel_coordinates(
        # Set the data
        filtered,

        # Set the parallel coords featured
        dimensions=features,

        # Put in dummy for categorical data
        color=filtered["dummy"],

        # Only put in the color for each attributes present
        color_continuous_scale=color_list
    )

    # Remove color scale
    fig.update_coloraxes(showscale=False)

    fig.update_layout(
        # Less white space
        margin={"r": 5, "t": 40, "l": 30, "b": 10},

        # Make background white
        plot_bgcolor= 'white',
        paper_bgcolor= 'white',

        # The rest
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
        showlegend=True,
        hovermode="x",
    )
    return fig