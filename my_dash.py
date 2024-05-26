
import argparse
import random

import dash
from dash import callback, dcc, html
from dash.dependencies import Output, Input, State

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template

import plotly.express as px
import plotly.graph_objs as go

import app_layout
from my_plots import get_alt_plot, get_geo_plot
from data_store import MyConfig, MyData

orig_lat, orig_lon, orig_alt = (45.0, -117.0, 1E5)
MAX_SIZE = 10
STEP = 0.02
ZOOM_FACTOR= 10

# TODO: Config data and real-time data should be different dcc.Store


def run_arg_parse():
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help',
    )
    parser.add_argument(
        '-lat', '--latitude', default=orig_lat, type=float,
        help='latitude (deg) for center of map',
    )
    parser.add_argument(
        '-lon', '--longitude', default=orig_lon, type=float,
        help='longitude (deg) for center of map',
    )
    parser.add_argument(
        '-ui', '--update_interval', default=1000, type=int,
        help='interval (milliseconds) for data/plot updates',
    )
    parser.add_argument(
        '-p', '--port', default=51000, type=int,
        help='port to send data to',
    )
    parser.add_argument(
        '-n', '--num_points', default=MAX_SIZE, type=int,
        help='Number of data points to keep',
    )
    return parser.parse_args()


args = run_arg_parse()
lat, lon, alt, time = ([args.latitude], [args.longitude], [1E5], [0])
orig_lat, orig_lon = (args.latitude, args.longitude)
MAX_SIZE = args.num_points

# Initialize the Dash app
app = app_layout.create_app(
    orig_lat,
    orig_lon,
    update_interval_ms=args.update_interval,
)


# Callback function to data at a cadence
@callback(
    Output("state-data", "data"),
    Input("graph-update", "n_intervals"),
    State("state-data", "data"),
)
def update_state_data(n, data_dict):

    data = MyData()
    data.from_dict(data_dict)
    
    if not data.has_data():
    
        data.update(
            new_lat_deg=orig_lat,
            new_lon_deg=orig_lon,
            new_alt_m=0.0,
            new_time_s=0.0,
        )
    
    else:

        # Get the new positions
        new_lat = data._lat_deg[-1] + STEP * (random.random() - 0.0*1/2)
        new_lon = data._lon_deg[-1] + STEP * (random.random() - 0.0*1/2)
        new_alt = data._alt_m[-1] + 1E2 * (random.random() - 1/2)
        new_time = data._time_s[-1] + args.update_interval / 1E3 # convert to sec

        data.update(
            new_lat_deg=new_lat,
            new_lon_deg=new_lon,
            new_alt_m=new_alt,
            new_time_s=new_time,
        )
    
    print('------------ STATE -------------')
    print(data.to_json_str(indent=4))

    return data.to_dict()


# Callback function to data input from user
@callback(
    Output("config-data", "data"),
    Input("zoom-input", "value"),
    Input("lat-input", "value"),
    Input("lon-input", "value"),
    State("config-data", "data"),
)
def update_config_data(
    new_zoom,
    new_orig_lat_deg,
    new_orig_lon_deg,
    config_dict,
):
    config = MyConfig().from_dict(config_dict)
    config._zoom_factor = new_zoom
    config._orig_lat_deg = new_orig_lat_deg
    config._orig_lon_deg = new_orig_lon_deg
    
    print('------------ CONFIG -------------')
    print(config.to_json_str(indent=4))

    return config.to_dict()


# Callback function to update the graph
@callback(
    Output("live-geo-plot", "figure"),
    Input("state-data", "data"),
    Input("config-data", "data"),
)
def update_geo_plot(data_dict, config_dict):

    data = MyData().from_dict(data_dict)
    config = MyConfig().from_dict(config_dict)

    fig_geo = get_geo_plot(
        data._lat_deg,
        data._lon_deg,
        config._orig_lat_deg,
        config._orig_lon_deg,
        config._zoom_factor,
    )

    # Return the graph figure
    return fig_geo


# Callback function to update the graph
@callback(
    Output("live-alt-plot", "figure"),
    Input("state-data", "data"),
)
def update_alt_plot(data_dict):

    data = MyData().from_dict(data_dict)

    fig_alt = get_alt_plot(
        data._time_s,
        data._alt_m,
    )

    # Return the graph figure
    return fig_alt


if __name__ == "__main__":
    app.run_server(debug=True, port=args.port)
