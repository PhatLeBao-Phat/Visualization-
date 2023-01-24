import filter
from dash import dcc, Input, html

class DropDown(filter.Filter):
    def __init__(self, data, input_name: str, attributes: list) -> None:
        dropdowns = []
        attributes.sort()
        for attribute in attributes:
            unique = data[attribute].dropna().unique()
            unique.sort()
            if len(list(unique)) < 30:
                dropdowns.append(html.Div([
                    html.Pre(attribute.split("_")[0][0].capitalize() + attribute.split("_")[0][1:]),
                    dcc.Dropdown(unique, unique, id="dropdown-{}".format(attribute), multi=True)
                    ]))

        inputs = {input_name: [Input("dropdown-{}".format(variable), "value") for variable in attributes]}

        def conditions_func(args: list[list]):
            queries = []
            for values, key in zip(args, attributes):
                if len(values) == 0:
                    continue

                if type(values[0]) == str:
                    queries.append(' | '.join(['{} == {}'.format('`{}`'.format(key), '"{}"'.format(v)) for v in values]))
                else:
                    queries.append(' | '.join(['{} == {}'.format("`{}`".format(key), v) for v in values]))

            for index, _ in enumerate(queries):
                queries[index] = "({})".format(_)

            return queries

        super().__init__(dropdowns, inputs, conditions_func)
        pass