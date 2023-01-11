import plotly.express as px

def figure(self, filtered_data, clustering_key):
    fig = px.treemap(filtered_data, path=[px.Constant("all"), "neighbourhood group", "review rate number"], color=clustering_key)
    fig.data[0]["sort"] = False
    fig.data[0]["textinfo"] = "percent root+percent parent"
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    return fig