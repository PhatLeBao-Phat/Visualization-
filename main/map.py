import plotly.express as px

def figure(filtered_data, clustering_key, color_map):
    """
    Assuming this function is used to make the map 
    -------------------------------------
    Input: 
    - filtered_data:
    - clustering_key:
    - color_map:
    
    Ouput:
    - fig 
    --------------------------------------
    """
    # Create map with the data
    # fig = px.scatter_mapbox(filtered_data, lat="lat", lon="long", color=filtered_data[clustering_key], custom_data={})
    # fig = px.scatter_mapbox(filtered_data, lat="lat", lon="long", color=clustering_key, color_discrete_sequence=px.colors.qualitative.G10, custom_data={})
    # fig = px.scatter_mapbox(filtered_data, lat="lat", lon="long", color=clustering_key, color_discrete_map=color(filtered_data, clustering_key), custom_data={})
    fig = px.scatter_mapbox(filtered_data, lat="lat", lon="long", color=clustering_key, color_discrete_map=color_map, custom_data={})


    # Selected points get highlighted yellow and size of marks are 5
    for scatter in fig.data:
        scatter.marker.size = 5
        scatter.selected = {"marker": {"color": "yellow"}}
        # scatter.unselected = {"marker": {"opacity": 0.4}}

    # Update layout to have a background. Zoom and center it in New York
    fig.update_layout(mapbox = {"style": "carto-positron", "zoom": 10, "center": {"lon": -73.96276, "lat": 40.68152}})
    fig.update_layout(margin={"r": 5, "t": 0, "l": 5, "b": 0})
    fig.update_layout(legend=dict(
        yanchor="top",
        y=1,
        xanchor="left",
        x=0,
    ))

    return fig

