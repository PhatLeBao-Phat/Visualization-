import plotly.graph_objects as go 
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd 
import os

# Read dataset 
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..\jupyter_notebook\listings.csv")

df_bnb = pd.read_csv(path)
df_plot = df_bnb.copy()[[
    'host_total_listings_count',
    'host_response_rate',
    'accommodates',
    'bedrooms',
    'review_scores_rating',
    'review_scores_accuracy',
    'review_scores_cleanliness',
    'review_scores_checkin',
    'review_scores_communication',
    'review_scores_location',
    'review_scores_value',
    'reviews_per_month',
]]
df_plot.dropna(inplace=True)
df_plot = df_plot.iloc[1:1000, :]

# Plot the PCP 
fig = go.Figure(data=
    go.Parcoords(
        line = dict(color = df_plot['review_scores_rating'],
                   colorscale = 'Electric',
                   showscale = True,
                #    cmin = -4000,
                #    cmax = -100
            ),
        dimensions = list([
            go.parcoords.Dimension(
                label = 'accuracy',
                values = df_plot['review_scores_accuracy']
                ),
            go.parcoords.Dimension(
                label = 'cleanliness',
                 values = df_plot['review_scores_cleanliness']
                 ),
            go.parcoords.Dimension(
                label = 'checkin',
                values = df_plot['review_scores_checkin']
                ),
            go.parcoords.Dimension(
                label = 'communication',
                values = df_plot['review_scores_communication']
                ),
            go.parcoords.Dimension(
                label = 'location',
                values = df_plot['review_scores_location']
                ),
        ]),
        unselected = dict(line = dict(color = 'gray', opacity = 0.5))
    )
)

fig.update_layout(
    plot_bgcolor = 'white',
    paper_bgcolor = 'white'
)

fig.show()

# Plot App 
app = dash.Dash()
app.layout = html.Div([
    dcc.Graph(figure=fig)
])

app.run_server(debug=True, use_reloader=True)  # Turn off reloader if inside Jupyter
