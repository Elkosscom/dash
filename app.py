import datetime as dt

import numpy as np
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

#########################
# Loading Data
#########################


df = pd.read_csv("novel-coronavirus - data_adm1.csv")
data_columns = [col for col in df.columns if col.startswith(("death", "confirmed"))]
cols_deaths = [col for col in data_columns if col.startswith("death")]
cols_confirmed = [col for col in data_columns if col.startswith("confirmed")]
cols_dates = [col.split("_")[1] for col in cols_confirmed]


#########################
# Lists and declarations
#########################
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets,
    suppress_callback_exceptions=True,
)
server = app.server
colours = {
    'bg0':"rgb(18,18,18)",
    'bg1':"rgb(29,29,29)",
    'bg2':"rgb(33,33,33)",
    'bg3':"rgb(36,36,36)",
    'bg4':"rgb(38,38,38)",
    'bg5':"rgb(44,44,44)",
    'bg6':"rgb(45,45,45)",
    'bg7':"rgb(49,49,49)",
    'bg8':"rgb(52,52,52)",
    'bg9':"rgb(54,54,54)",
}

#########################
# Dashboard Sections
#########################

main_view = html.Div(
    [
        dcc.Graph(id="map"),
        dcc.Slider(
            id="date_slider",
            min=0,
            max=len(cols_dates) - 1,
            value=0,
            step=1,
            marks={i: cols_dates[i] for i in range(0, len(cols_dates), 2)},
            updatemode='mouseup'
        ),
        html.Br(style={''})
    ],
    style={'backgroundColor':colours['bg0'],'height':'200%'}
)



#########################
# Dashboard Layout / View
#########################

app.layout = html.Div(main_view,style={'backgroundColor':colours['bg0']})

############################################
# Interaction Between Components / Controller
############################################
@app.callback(
    Output("map", "figure"), [Input("date_slider", "value")]
)
def update_map(day: int):
    fig = go.Figure()
    confirmed = df[f"confirmedcases_{cols_dates[day]}"].fillna(0)
    deaths = df[f"deaths_{cols_dates[day]}"].fillna(0)
    text = df.location + '<br>Confirmed cases: ' + confirmed.astype(str) + '<br>Deaths: ' + deaths.astype(str)
    fig.update_geos(
        projection_type="natural earth",
        resolution=50,
        showcountries=True,
        countrycolor="rgb(0,10,18)",
        showland=True,
        landcolor="rgb(38,50,56)",
        showocean=True,
        oceancolor="rgb(79,91,98)",
        showrivers=False,
        showlakes=False,
    )
    fig.update_layout(height=500, margin={"r": 0, "t": 0, "l": 0, "b": 0})
    fig.add_trace(
        go.Scattergeo(
            lon=df.longitude,
            lat=df.latitude,
            hovertext=text,
            hoverinfo='text+lon+lat',
            mode='markers',
            marker=dict(
                size=confirmed,
                sizemin=3,
                sizemode='area',
                opacity=0.8,
                sizeref=10,
                color=deaths,
                colorscale='Cividis',
                showscale=True
            )
        )
    )
    return fig



# start Flask server
if __name__ == "__main__":
    app.run_server(debug=True)
