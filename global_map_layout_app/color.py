import plotly.express as px

def color(data, clustering_key):
    # Get type
    type_column = data[clustering_key].dtype

    # Sequential clustering_key coloring
    if  type_column == "int64" or type_column == "float64":
        # Color map with increasing luminance
        return px.colors.sequential.Inferno

    # Discrete clustering_key coloring
    # Color map with the same luminance
    return {key: color for key, color in zip(list(data[clustering_key].unique()), px.colors.qualitative.G10)}