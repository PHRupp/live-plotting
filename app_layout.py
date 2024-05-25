import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

def create_app(orig_lat, orig_lon, update_interval_ms=500):

    # Initialize the Dash app
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

    # Define the layout of the app
    load_figure_template(["cyborg", "darkly"])
    app.layout = html.Div([
        html.H2("Live Graph"),
        html.Div([
            html.Plaintext(
                "Center Lat/Lon (deg): ",
                style={'display': 'inline-block'}
            ),
            dcc.Input(
                id='lat-input',
                placeholder='Latitude (deg)',
                type='number',
                value=orig_lat,
                style={'display': 'inline-block'}, #'width': '49%', 
            ),
            dcc.Input(
                id='lon-input',
                placeholder='Longitude (deg)',
                type='number',
                value=orig_lon,
                style={'display': 'inline-block'},
            ),
            html.Hr(),
        ]),
        dcc.Graph(id="live-graph"),
        dcc.Interval(
            id="graph-update",
            interval=update_interval_ms,
            n_intervals=0,
        ),
    ])
    
    return app
