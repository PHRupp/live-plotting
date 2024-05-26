
import plotly.express as px
import plotly.graph_objs as go


def get_geo_plot(lat, lon, orig_lat, orig_lon, zoom):

    num_points = len(lat)

    trace = px.scatter_geo(
        lat=lat,
        lon=lon,
        color_discrete_sequence=["#1F1EFF"] * num_points,
        opacity=[(i+1) / num_points for i in range(num_points)],
    )

    fig = go.Figure(
        data=trace, 
        layout=go.Layout(
            title='Geolocation',
        )
    )
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
        projection_scale=zoom,
        projection_type='orthographic',
    )
    
    # Return the graph figure
    return fig

def get_alt_plot(time, alt):
    trace = go.Scatter(
        x=time,
        y=alt,
        mode= 'lines+markers',
        #width=800,
        #height=600,
    )
    layout = go.Layout(
        title="Altitude",
        xaxis=dict(range=[min(time), max(time)]),
        yaxis=dict(range=[min(alt), max(alt)]),
    )
    return {"data": [trace], "layout": layout}
