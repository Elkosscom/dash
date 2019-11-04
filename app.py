import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np
import currency_data


#########################
# Loading Data
#########################
# Sales data
df_sales = pd.read_excel("data.xlsx", sheet_name=1)
df_sales["Month"] = pd.DatetimeIndex(df_sales["Date"]).month
df_sales["Month"].replace({1: "Jan", 2: "Feb", 3: "Mar"}, inplace=True)

# Currency data
df = pd.read_json(currency_data.filename)


#########################
# Lists and declarations
#########################
external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
colors = {
    "bg": "#373737",
    "bglight": "#dfdce3",
    "accent1": "#e37222",
    "accent2": "#07889b",
}
style_text = {"backgroundColor": colors["bg"], "color:": colors["accent1"]}
borders = {"border": "1px solid black", "border-radius": "15px"}
style_div = {**borders, **{"backgroundColor": colors["bglight"]}}

#########################
# Dashboard Sections
#########################
##### Sales tab
sales_scatter_div = html.Div(
    [
        html.Div(
            [
                html.H6("Options:", style={"verticalAlign": "top"}),
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
            id="graph2", style={"width": "73%", "display": "inline-block", "margin": 3}
        ),
    ],
    style=style_div,
)

sales_line_div = html.Div(
    [
        html.Div(
            [
                html.H6("Options:", style={"verticalAlign": "top"}),
                html.Label("X Axis:"),
                dcc.Dropdown(
                    id="graph3_x",
                    options=[{"label": i, "value": i} for i in ["Date"]],
                    value="Date",
                    multi=False,
                    disabled=True,
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
                        {"label": i, "value": i} for i in ["Depo", "Client", "Item"]
                    ],
                    value="Item",
                    multi=False,
                ),
                html.H4("   "),
                dcc.Checklist(
                    "graph3_cum", options=[{"label": "Cumulative", "value": 1}]
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
            "graph3", style={"width": "73%", "display": "inline-block", "margin": 3}
        ),
    ],
    style=style_div,
)

sales_tab_content = (
    html.Div(
        [
            dcc.Markdown(
                """Sales data is random, source file available on the github repo."""
            ),
            html.P(" "),
            sales_scatter_div,
            html.P(" "),
            sales_line_div,
        ]
    ),
)


##### TODO: Currency tab
currency_tab_content = None


##### Page header
page_header = html.Div(
    [
        dcc.Markdown(
            """ ## **Dash**
### _A dashboard made in Python_""",
            style={"textAlign": "center", "backgroundColor": colors["bglight"]},
        ),
        dcc.Markdown(
            """
Welcome to the test page of Dash. This website is made completely in Python and
serves as a playground for learning Dash library. 
For source code visit [my repository](https://github.com/Elkosscom/dash)."""
        ),
    ],
    style=style_div,
)


##### Tab bar
tabs = dcc.Tabs(
    id="tab-bar",
    value="sales-tab",
    children=[
        dcc.Tab(label="Sales", value="sales-tab"),
        dcc.Tab(label="Currency", value="currency-tab"),
    ],
)

tab_content = html.Div(id="tab-content")
#########################
# Dashboard Layout / View
#########################

app.layout = html.Div(  # Back-background
    html.Div(  # Background narrow
        [page_header, tabs, html.P(" "), tab_content],
        style={
            "display": "block",
            "marginLeft": "auto",
            "marginRight": "auto",
            "width": "80%",
            "height": "105%",
        },
    ),
    style={"backgroundColor": colors["bg"]},
)


#############################################
# Interaction Between Components / Controller
#############################################
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
        df_sales,
        x=x,
        y=y,
        color=color,
        facet_row=facet_row,
        facet_col=facet_col,
        title="Sales Scatter Graph",
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
    df_return = df_sales.groupby(by=[x, color], axis=0).agg(
        Quantity=("Quantity", "sum"),
        Price=("Price", np.mean),
        Net=("Net", "sum"),
        VAT=("VAT", "sum"),
        Gross=("Gross", "sum"),
    )
    if cumulative:
        df_return = df_return.groupby(level=1).cumsum()
    df2 = df_return.reset_index(level=[0, 1])
    fig = go.Figure(layout={"title": "Sales Line Graph"})
    for line in df_sales[color].unique():
        fig.add_trace(
            go.Scatter(
                x=df2[df2[color] == line][x],
                y=df2[df2[color] == line][y],
                mode="lines",
                name=line,
            )
        )
    return fig


@app.callback(Output("tab-content", "children"), [Input("tab-bar", "value")])
def update_tab_content(tab):
    if tab == "sales-tab":
        return sales_tab_content
    elif tab == "currency-tab":
        return currency_tab_content


# start Flask server
if __name__ == "__main__":
    app.run_server(debug=True)
