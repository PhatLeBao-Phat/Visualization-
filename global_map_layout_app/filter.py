"""
This file contains:
    - Class Filter
"""

class Filter:
    def __init__(self, children, inputs, conditions_func) -> None:
        # The html for the app layout
        self.children = children

        # The inputs used for callback
        self.inputs = inputs

        # Use the values of the input in the conditions_func to generate the conditions to query on
        self.conditions_func = conditions_func
        pass