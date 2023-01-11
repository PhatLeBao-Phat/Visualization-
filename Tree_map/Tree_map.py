import plotly.graph_objects as go 
from plotly.subplots import make_subplots 
import pandas as pd 
import numpy as np 
import plotly.express as px

from data import df_bnb

df = df_bnb.copy()

# Just clean data (SKIP)
df.dropna(subset=['room_type','host_is_superhost', 'neighbourhood_group_cleansed'], inplace=True)
df = df.reset_index()
def dcm(row):
    if row == 't':
        return 'is superhost' 
    else:
        return 'not superhost' 
df['host_is_superhost_cleansed'] = df.host_is_superhost.apply(lambda row: dcm(row))
df['num_count'] = pd.Series(np.repeat(1, len(df))) # Add a attribute for counting

# Make plot 
df["all"] = "all" # Add rote node 
fig = px.treemap(
    df, 
    path=['all', 'neighbourhood_group_cleansed', 'host_is_superhost_cleansed', 'room_type'],
    values='num_count',
    color='price_cleansed',
    color_continuous_scale=px.colors.sequential.RdBu,
    maxdepth=4
)
fig.update_traces(root_color="lightgrey")
fig.update_layout(dict(
    margin=dict(t=50, l=25, r=25, b=25),
    coloraxis_showscale=True,
    coloraxis=dict(
        colorbar=dict(
            title='Price ($)'
        )
    )
))
fig.show()
