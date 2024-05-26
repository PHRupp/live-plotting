
import argparse
import random

import dash
from dash import dcc, html
from dash.dependencies import Output, Input

import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash_bootstrap_templates import load_figure_template

import plotly.express as px
import plotly.graph_objs as go

import app_layout
from my_plots import get_alt_plot, get_geo_plot

orig_lat, orig_lon, orig_alt = (45.0, -117.0, 1E5)
MAX_SIZE = 10
STEP = 0.02
ZOOM_FACTOR= 10


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
        help='longitude (deg) for center of map',
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


# Callback function to update the graph
@app.callback(
    [
        Input("lat-input", "value"),
        Input("lon-input", "value"),
        Input("zoom-input", "value"),
    ]
)
def update_lat_lon(new_lat, new_lon, new_zoom):
    global orig_lat, orig_lon, ZOOM_FACTOR
    orig_lat = new_lat
    orig_lon = new_lon
    ZOOM_FACTOR = new_zoom


# Callback function to update the graph
@app.callback(
    Output("live-geo-plot", "figure"),
    [
        Input("graph-update", "n_intervals"),
    ]
)
def update_geo_plot(n):

    global lat, lon, alt

    # Get the new positions
    new_lat = lat[-1] + STEP * (random.random() - 0.0*1/2)
    new_lon = lon[-1] + STEP * (random.random() - 0.0*1/2)
    new_alt = alt[-1] + 1E2 * (random.random() - 1/2)
    new_time = time[-1] + args.update_interval / 1E3 # convert to sec

    # Update position history
    lat.append(new_lat)
    lon.append(new_lon)
    alt.append(new_alt)
    time.append(new_time)

    # Remove oldest position
    while len(lat) > MAX_SIZE:
        del lat[0]
        del lon[0]
        del alt[0]
        del time[0]

    fig_geo = get_geo_plot(
        lat,
        lon,
        orig_lat,
        orig_lon,
        ZOOM_FACTOR,
    )
    
    # Return the graph figure
    return fig_geo


# Callback function to update the graph
@app.callback(
    Output("live-alt-plot", "figure"),
    [
        Input("graph-update", "n_intervals"),
    ]
)
def update_alt_plot(n):

    global lat, lon, alt

    fig_alt = get_alt_plot(
        time,
        alt,
    )

    # Return the graph figure
    return fig_alt


if __name__ == "__main__":
    app.run_server(debug=True, port=args.port)
