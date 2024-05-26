import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_bootstrap_templates import load_figure_template

def create_app(orig_lat, orig_lon, zoom_factor = 10, update_interval_ms=5000):

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
            html.Plaintext(
                "     Zoom Factor: ",
                style={'display': 'inline-block'}
            ),
            dcc.Input(
                id='zoom-input',
                placeholder='Zoom (factor)',
                type='number',
                value=zoom_factor,
                style={'display': 'inline-block'},
            ),
        ]),
        html.Hr(),
        html.Div([
            dcc.Graph(
                id="live-geo-plot",
                style={
                    'display': 'inline-block',
                    'width': '50%',
                    'height': '100vf',
                }
            ),
            dcc.Graph(
                id="live-alt-plot",
                animate=True,
                style={
                    'display': 'inline-block',
                    'width': '50%',
                    'height': '100vf',
                }
            ),
        ]),
        dcc.Interval(
            id="graph-update",
            interval=update_interval_ms,
            n_intervals=0,
        ),
        dcc.Store(id="state-data"),
        dcc.Store(id="config-data"),
    ])
    
    return app
