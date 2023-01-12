from dash import dcc, Input
import filter

class RangeSlider(filter.Filter):
    def __init__(self, data, input_name: str, attributes : list[str], step: list[int, int]) -> None:
        range_sliders = []
        for index, variable in enumerate(attributes):
            marks = {}
            value = []
            min : any = 0
            max : any = 1
            
            dff = data[variable]
            min = dff.min()
            max = dff.max()
            #marks = {int(number): str(int(number)) for number in dff.unique()}
            range_sliders.append(dcc.RangeSlider(id="range-slider-{}".format(variable), min=min, max=max, marks=marks, value=[min, max], tooltip={"placement": "bottom", "always_visible": True}))
            
        inputs = {input_name: [Input("range-slider-{}".format(variable), "value") for variable in attributes]}

        def conditions_func(args : list[list]):
            queries = []

            # The nested list is always length of 2: [min, max]
            for values, key in zip(args, attributes):
                queries.append("(({} >= {}) & ({} <= {}))".format("`{}`".format(key), values[0], "`{}`".format(key), values[1]))

            return queries

        super().__init__(range_sliders, inputs, conditions_func)
        pass

