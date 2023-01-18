from dash import dcc, Input, Output, html
import plotly.express as px
import filter

class RangeSlider(filter.Filter):
    def __init__(self, data, input_name: str, attributes : list[str]) -> None:
        range_sliders = []
        self.histogram_output = []
        self.histogram_lims = {}
        for index, variable in enumerate(attributes):
            marks = {}
            value = []
            min : any = 0
            max : any = 1
            
            dff = data[variable]
            min = dff.min()
            max = dff.max()
            self.histogram_lims[variable] = [min, max]
            #marks = {int(number): str(int(number)) for number in dff.unique()}
            self.histogram_output.append(Output("range-slider-histogram-{}".format(variable), "figure"))
            range_sliders.append(html.Div([
                html.Pre(variable.split("_")[0][0].capitalize() + variable.split("_")[0][1:]),
                dcc.Graph(id="range-slider-histogram-{}".format(variable)),
                dcc.RangeSlider(id="range-slider-{}".format(variable), min=min, max=max, marks=marks, value=[min, max], tooltip={"placement": "bottom", "always_visible": True})
                ]))
            
        inputs = {input_name: [Input("range-slider-{}".format(variable), "value") for variable in attributes]}

        def conditions_func(args : list[list]):
            queries = []

            # The nested list is always length of 2: [min, max]
            for values, key in zip(args, attributes):
                queries.append("(({} >= {}) & ({} <= {}))".format("`{}`".format(key), values[0], "`{}`".format(key), values[1]))

            return queries

        def histogram(df, attribute):
            fig = px.histogram(df, x=attribute)
            
            # legend
            fig.update_layout(showlegend=False)

            # Take up space
            fig.update_layout(margin={"r": 5, "t": 0, "l": 5, "b": 0})

            # x axis
            fig.update_xaxes(visible=False, range=self.histogram_lims[attribute])

            # y axis
            fig.update_yaxes(visible=False)

            # Take up less space
            fig.update_layout(height=50)

            # Make background transparent
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)'     
            )

            return fig

        def histogram_function(df):
            return [histogram(df, attribute) for attribute in attributes]

        self.histogram_figures = histogram_function

        super().__init__(range_sliders, inputs, conditions_func)
        pass
