import plotly.express as px
from color import color
from graphs.PCP import reverse_DIMS

def figure(self, filtered_data, clustering_key, color_map, path):
    fig = px.treemap(filtered_data, path=self.showed, color=clustering_key, color_discrete_map=color_map, custom_data=self.showed)
    # fig = px.treemap(filtered_data, path=[reverse_DIMS[key] for key in path], color=clustering_key, color_discrete_map=color_map, custom_data=[reverse_DIMS[key] for key in path])
    fig.data[0]["textinfo"] = "percent root+percent parent"
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))
    return fig