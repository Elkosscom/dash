import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash.dependencies import Input, Output


df = pd.read_excel("data.xlsx", sheet_name=1)
df["Month"] = pd.DatetimeIndex(df["Date"]).month


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

#### ROWS
row1 = html.Div(
    [
        html.Div(
            [
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id="graph_x",
                    options=[{"label": i, "value": i} for i in ["Date", "Month"]],
                    value="Date",
                    multi=False,
                ),
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id="graph_y",
                    options=[
                        {"label": i, "value": i} for i in ["Quantity", "Gross", "Net"]
                    ],
                    value="Net",
                    multi=False,
                ),
                html.Label("Colour:"),
                dcc.Dropdown(
                    id="graph_color",
                    options=[
                        {"label": i, "value": i} for i in ["Client", "Depo", "Item"]
                    ],
                    value="Item",
                    multi=False,
                ),
            ],
            style={
                "width": "25%",
                "float": "left",
                "height": "50%",
                "verticalAlign": "center",
                "paddingTop": "60px",
            },
        ),
        dcc.Graph(id="graph", style={"width": "75%", "display": "inline-block"}),
    ]
)

row2 = html.Div(
    [
        html.Div(
            [
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id="graph2_x",
                    options=[
                        {"label": i, "value": i}
                        for i in ["Date", "Net", "Gross", "Vat", "Quantity"]
                    ],
                    value="Date",
                    multi=False,
                ),
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id="graph2_y",
                    options=[
                        {"label": i, "value": i}
                        for i in ["Date", "Net", "Gross", "Vat", "Quantity"]
                    ],
                    value="Gross",
                    multi=False,
                ),
                html.Label("Colour:"),
                dcc.Dropdown(
                    id="graph2_color",
                    options=[
                        {"label": i, "value": i}
                        for i in ["Depo", "Client", "Item", "Month"]
                    ],
                    value="Item",
                    multi=False,
                ),
                html.Label("Facet row:"),
                dcc.Dropdown(
                    id="graph2_facet_row",
                    options=[
                        {"label": i, "value": i}
                        for i in ["Depo", "Client", "Item", "Month"]
                    ],
                    value=None,
                    multi=False,
                ),
                html.Label("Facet column:"),
                dcc.Dropdown(
                    id="graph2_facet_col",
                    options=[
                        {"label": i, "value": i}
                        for i in ["Depo", "Client", "Item", "Month"]
                    ],
                    value=None,
                    multi=False,
                ),
            ],
            style={
                "width": "25%",
                "float": "left",
                "height": "50%",
                "verticalAlign": "center",
                "paddingTop": "60px",
            },
        ),
        dcc.Graph(id="graph2", style={"width": "75%", "display": "inline-block"}),
    ]
)

row3 = html.Div(
    [
        html.Div(
            [
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id="graph3_x",
                    options=[
                        {"label": i, "value": i}
                        for i in ["Date"]
                    ],
                    value="Date",
                    multi=False,
                    disabled=True
                ),
                html.Label("Y Axis:"),
                dcc.Dropdown(
                    id="graph3_y",
                    options=[
                        {"label": i, "value": i}
                        for i in ["Net", "Gross", "VAT", "Quantity"]
                    ],
                    value="Gross",
                    multi=False,
                ),
                html.Label("Colour:"),
                dcc.Dropdown(
                    id="graph3_color",
                    options=[
                        {"label": i, "value": i}
                        for i in ["Depo", "Client", "Item"]
                    ],
                    value="Item",
                    multi=False,
                ),
                dcc.Checklist(
                    "graph3_cum", options=[{"label": "Cumulative", "value": 1}]
                )
            ],
            style={
                "width": "25%",
                "float": "left",
                "height": "50%",
                "verticalAlign": "center",
                "paddingTop": "60px",
            },
        ),
        dcc.Graph("graph3", style={"width": "75%", "display": "inline-block"}),
    ]
)
#### Layout
app.layout = html.Div(
    [row1, row2, row3],
    style={
        "display": "block",
        "marginLeft": "auto",
        "marginRight": "auto",
        "width": "80%",
    },
)


#### Interactivity
@app.callback(
    Output("graph", "figure"),
    [
        Input("graph_x", "value"),
        Input("graph_y", "value"),
        Input("graph_color", "value"),
    ],
)
def update_graph(x, y, color):
    return px.scatter(df, x=x, y=y, color=color, title="Sales graph")


@app.callback(
    Output("graph2", "figure"),
    [
        Input("graph2_x", "value"),
        Input("graph2_y", "value"),
        Input("graph2_color", "value"),
        Input("graph2_facet_row", "value"),
        Input("graph2_facet_col", "value"),
    ],
)
def update_graph2(x, y, color, facet_row, facet_col):
    return px.scatter(
        df,
        x=x,
        y=y,
        color=color,
        facet_row=facet_row,
        facet_col=facet_col,
        title="Sales graph 2",
    )


@app.callback(
    Output("graph3", "figure"),
    [
        Input("graph3_x", "value"),
        Input("graph3_y", "value"),
        Input("graph3_color", "value"),
        Input("graph3_cum", "value"),
    ],
)
def update_graph3(x, y, color, cumulative):
    df_return = df.groupby(by=(x,color), axis=0).agg(
        Quantity=("Quantity", "sum"),
        Price=("Price", np.mean),
        Net=("Net", "sum"),
        VAT=("VAT", "sum"),
        Gross=("Gross", "sum"),
    )
    if cumulative:
        df_return = df_return.groupby(level=1).cumsum()
    df2 = df_return.reset_index(level=[0,1])
    fig = go.Figure()
    for line in df[color].unique():
        fig.add_trace(go.Scatter(x=df2[df2[color]==line][x],y=df2[df2[color]==line][y],mode='lines',name=line))
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
