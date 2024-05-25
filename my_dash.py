
import argparse

import dash
from dash import dcc, html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.express as px
import plotly.graph_objs as go
import random

import app_layout

orig_lat, orig_lon = (45.0, -117.0)
MAX_SIZE = 10
STEP = 0.02

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
    return parser.parse_args()

args = run_arg_parse()
lat, lon = ([args.latitude], [args.longitude])
orig_lat, orig_lon = (args.latitude, args.longitude)

# Initialize the Dash app
app = app_layout.create_app(orig_lat, orig_lon)


# Callback function to update the graph
@app.callback(
    [
        Input("lat-input", "value"),
        Input("lon-input", "value"),
    ]
)
def update_lat_lon(new_lat, new_lon):
    global orig_lat, orig_lon
    orig_lat = new_lat
    orig_lon = new_lon


# Callback function to update the graph
@app.callback(
    Output("live-graph", "figure"),
    [
        Input("graph-update", "n_intervals"),
    ]
)
def update_graph(n):

    global lat, lon

    # Get the new positions
    new_lat = lat[-1] + (STEP*random.random() - 0.0*STEP/2)
    new_lon = lon[-1] + (STEP*random.random() - 0.0*STEP/2)

    # Update position history
    lat.append(new_lat)
    lon.append(new_lon)

    # Remove oldest position
    while len(lat) > MAX_SIZE:
        del lat[0]
        del lon[0]

    num_points = len(lat)

    trace = px.scatter_geo(
        lat=lat,
        lon=lon,
        color_discrete_sequence=["#1F1EFF"] * num_points,
        opacity=[(i+1) / num_points for i in range(num_points)],
        width=1600,
        height=1000,
    )

    fig = go.Figure(data=trace, layout=go.Layout())
    fig.update_geos(
        resolution=50,
        showland=True, landcolor="#85A16D",
        showocean=True, oceancolor="#000435",
        showlakes=True, lakecolor="RebeccaPurple",
        showrivers=True, rivercolor="RebeccaPurple",
        showsubunits=True, subunitcolor="Red",
        showcountries=True, countrywidth=2, countrycolor="Black",
        showcoastlines=True, coastlinecolor="Black",
        lataxis=dict(showgrid=True),
        lonaxis=dict(showgrid=True),
        projection_rotation=dict(lat=orig_lat, lon=orig_lon),
        center=dict(lat=orig_lat, lon=orig_lon), # this will center on the point
        projection_scale=10, #this is kind of like zoom
        projection_type='orthographic',
    )

    # Return the graph figure
    return fig


if __name__ == "__main__":
    app.run_server(debug=True, port=8051)
