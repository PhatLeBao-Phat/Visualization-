from layout import filter_dropdowns, filter_rangesliders, df_bnb, treemap
from color import color
from dash import Output, Input, ctx
import pandas as pd

def initialize_data_callbacks(app):

    # Menu
    @app.callback(
        Output("menu-container", "data-menu-toggle"),
        Input("menu-button", "n_clicks"),
        Input("menu-container", "data-menu-toggle"),
        prevent_initial_call=True
    )
    def filter_dropdown(n_clicks, boolean):
        return "appear" if boolean == "collapsed" else "collapsed"

    # All the inputs arrive here, data gets filtered and stored in a dict
    @app.callback(
        Output("memory-graphs", "data"),
        filter_dropdowns.inputs,
        filter_rangesliders.inputs,
    )
    def filter_data(parameters_filter_dropdown, parameters_filter_rangeslider):
        query1 = ' & '.join(filter_dropdowns.conditions_func(list(parameters_filter_dropdown.values())[0]))
        query2 = " & ".join(filter_rangesliders.conditions_func(list(parameters_filter_rangeslider.values())[0]))
        query = " & ".join(["{}".format(query1), "{}".format(query2)])

        filtered = df_bnb.query(query)

        return filtered.to_dict('records')

    # Store the data of clickData of treemap
    @app.callback(
        Output("memory-treemap", "data"),
        Input("treemap-1", "clickData"),
        Input("clustering-key", "value"),
        Input("map-1", "selectedData")
    )
    def highlight_map(clicked, clustering_key, selected):
        if clicked is None:
            return None

        # # Remove selection when selected
        # if selected is not None:
        #     return None

        # Remove selection when color change
        if ctx.triggered[0]["prop_id"].split(".")[0] == "clustering-key":
            return None

        try:
            derived = clicked["points"][0]["customdata"]
        except:
            return None
        
        return ' & '.join(["({} == {})".format("`{}`".format(key), '"{}"'.format(elem)) for key, elem in zip(treemap.showed, derived) if elem != "(?)"])

    # Store the colormap
    @app.callback(
        Output("memory-colormap", "data"),
        Input("memory-graphs", "data"),
        Input("clustering-key", "value")
    )
    def update_colormap(filtered_dict, clustering_key):
        filtered = pd.DataFrame.from_records(filtered_dict)
        return color(filtered, clustering_key)

    # Store the selection on the map
    @app.callback(
        Output("memory-map", "data"),
        Input("memory-map", "data"),
        Input("map-1", "selectedData"),
        Input("clustering-key", "value")
    )
    def highlight_map(prev_selected, selected, clustering_key):
        if selected is None:
            return prev_selected

        # # Remove selection when color change
        # if ctx.triggered[0]["prop_id"].split(".")[0] == "clustering-key":
        #     return None

        right_bottom_y = selected["range"]["mapbox"][0][0]
        right_bottom_x = selected["range"]["mapbox"][0][1]
        left_top_y = selected["range"]["mapbox"][1][0]
        left_top_x = selected["range"]["mapbox"][1][1]
        # data_bool = (data["long"] > right_bottom[0]) & (data["lat"] < right_bottom[1]) & (data["long"] < left_top[0]) & (data["lat"] > left_top[1])

        return "((longitude > {}) & (latitude < {}) & (longitude < {}) & (latitude > {}))".format(right_bottom_y, right_bottom_x, left_top_y, left_top_x)