import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np


#########################
# Loading Data
#########################


#########################
# Dashboard Sections
#########################
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
colors = {
    "bg": "#373737",
    "bglight": "#dfdce3",
    "accent1": "#e37222",
    "accent2": "#07889b",
}


#########################
# Dashboard Layout / View
#########################

app.layout = html.Div(
    html.Div(
        dcc.Graph(id='map'),
        style={
            "display": "block",
            "marginLeft": "auto",
            "marginRight": "auto",
            "width": "80%",
            "height": "105%",
        },
    ),
    style={"backgroundColor": colors["bg"], "height": "100%"},
)