from dash import Dash, dcc, html, Input, Output

def create_dropdown():
    return dcc.Dropdown(
            options=['accuracy', 'checkin', 'cleanliness', 'communication', 'location'],
            value=['accuracy', 'communication', 'location'],
            multi=True,
            id='demo-dropdown',
            searchable=False,
            )
    