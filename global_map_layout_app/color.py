import plotly.express as px
import colorsys

def color(data, clustering_key, color_blind = False):
    # Get type
    type_column = data[clustering_key].dtype

    # Sequential clustering_key coloring
    if  type_column == "int64" or type_column == "float64":
        # Color map with increasing luminance
        return px.colors.sequential.Inferno

    # Discrete clustering_key coloring
    # Color map with the same luminance

    color_list = ['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33']
    if color_blind == "No Red":
        color_list = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c']
    if color_blind == "No Green":
        color_list = ['#a6cee3','#1f78b4','#b2df8a','#33a02c','#fb9a99','#e31a1c']
    if color_blind == "No Blue":
        color_list = ['#7fc97f','#beaed4','#fdc086','#ffff99','#386cb0','#f0027f']
    # return {key: color for key, color in zip(list(data[clustering_key].unique()), px.colors.qualitative.G10)}
    return {key: color for key, color in zip(list(data[clustering_key].unique()), color_list)}