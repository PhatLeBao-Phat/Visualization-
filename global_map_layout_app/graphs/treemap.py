import plotly.express as px

def figure(self, filtered_data, clustering_key, color_map, path):
    fig = px.treemap(filtered_data, path=path, color=clustering_key, color_discrete_map=color_map, custom_data=path)

    fig.data[0].texttemplate = "<br>".join([
        "%{value} or %{percentParent} of the listings is %{label}",
    ])
    fig.data[0].hovertemplate = "<br>".join([
        "%{customdata[0]}",
        "%{customdata[1]}",
        "%{customdata[2]}",
        "%{value} or %{percentParent:.1%}",
    ])
    fig.update_layout(margin = dict(t=50, l=25, r=25, b=25))

    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )
    return fig