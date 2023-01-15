import plotly.express as px
from color import color

def figure(self, filtered_data, clustering_key, color_map):
    # fig = px.treemap(filtered_data, path=self.showed, color=clustering_key, custom_data=self.showed)
    # fig = px.treemap(filtered_data, path=self.showed, color=clustering_key, color_discrete_sequence=px.colors.qualitative.G10, custom_data=self.showed)
    # fig = px.treemap(filtered_data, path=self.showed, color=clustering_key, color_discrete_map=color(filtered_data, clustering_key), custom_data=self.showed)
    fig = px.treemap(filtered_data, path=self.showed, color=clustering_key, color_discrete_map=color_map, custom_data=self.showed)
    # fig.update_layout(marker={"color:click": "yellow"})
    # fig.data[0]["sort"] = False
    fig.data[0]["textinfo"] = "percent root+percent parent"
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    # for scatter in fig.data:
    #     scatter.marker = {"color": "yellow"}

    return fig