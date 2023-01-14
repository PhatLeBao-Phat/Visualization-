"""
This file contains:
    - Class Filter
"""

class Filter:
    def __init__(self, children, inputs, conditions_func) -> None:
        self.children = children
        self.inputs = inputs
        self.conditions_func = conditions_func
        pass