import plotly.express as px

def color(data, clustering_key):
    return {key: color for key, color in zip(list(data[clustering_key].unique()), px.colors.qualitative.G10)}