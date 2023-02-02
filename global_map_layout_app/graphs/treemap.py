import plotly.express as px

def figure(self, filtered_data, clustering_key, color_map, path):
    # Create treemap
    if type(color_map) != list:
        # Coloured on a discrete clustering_key
        fig = px.treemap(filtered_data, path=path, color=clustering_key, color_discrete_map=color_map, custom_data=path)
    else:
        # Coloured on a sequential clustering_key
        fig = px.treemap(filtered_data, path=path, color=clustering_key, color_continuous_scale=color_map, custom_data=path)

    # Remove color scale
    fig.update_coloraxes(showscale=False)

    """
    Texttemplate displays text on default when loaded in on last layer
        - value: Gives the number of listings in this layer
        - percentParent: Gives the percentage of listings of based previous later
        - label: A unique observation of that layer
    """
    fig.data[0].texttemplate = "<br>".join([
        "%{value} or %{percentParent} of the listings of 2nd layer is %{label}",
    ])

    """
    Hovertemplate displays text when hovered hover any layer
        - customdata[0]: Shows value of first attribute
        - customdata[1]: Shows value of second attribute
        - customdata[2]: Shows value of third attribute
        - value: Gives the number of listings in this layer
        - percentParent: Gives the percentage of listings of based previous later
    """
    fig.data[0].hovertemplate = "<br>".join([
        "1st layer: %{customdata[0]}",
        "2nd layer: %{customdata[1]}",
        "3rd layer: %{customdata[2]}",
        "%{value} or %{percentRoot:.1%} of all listings",
    ])

    # Less white space
    fig.update_layout(margin={"r": 5, "t": 30, "l": 5, "b": 0})

    # Background color adjusted and font on the hovering
    fig.update_layout(
        hoverlabel=dict(
            bgcolor="white",
            font_size=16,
            font_family="Rockwell"
        )
    )
    
    return fig