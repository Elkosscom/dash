import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output


df = pd.read_excel("data.xlsx", sheet_name=1)
df["Month"] = pd.DatetimeIndex(df["Date"]).month


external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    [
        # ROW 1
        html.Div(
            [
                html.Div(
                    [
                        html.Label("X Axis:"),
                        dcc.Dropdown(
                            id="graph_x",
                            options=[
                                {"label": i, "value": i} for i in ["Date", "Month"]
                            ],
                            value="Date",
                            multi=False,
                        ),
                        html.Label("Y Axis:"),
                        dcc.Dropdown(
                            id="graph_y",
                            options=[
                                {"label": i, "value": i}
                                for i in ["Quantity", "Gross", "Net"]
                            ],
                            value="Net",
                            multi=False,
                        ),
                        html.Label("Colour:"),
                        dcc.Dropdown(
                            id="graph_color",
                            options=[
                                {"label": i, "value": i}
                                for i in ["Client", "Depo", "Item"]
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
                dcc.Graph(
                    id="graph", style={"width": "75%", "display": "inline-block"}
                ),
            ]
        ),
        # ROW 2
        html.Div(
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
                dcc.Graph(
                    id="graph2", style={"width": "75%", "display": "inline-block"}
                ),
            ]
        ),
    ],
    style={
        "display": "block",
        "marginLeft": "auto",
        "marginRight": "auto",
        "width": "80%",
    },
)


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


if __name__ == "__main__":
    app.run_server()
