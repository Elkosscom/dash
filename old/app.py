import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import dash_table

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
currency_data.main()
target_currencies = currency_data.bases[1:]

# Load and transform currency data to small buy/sell table with GBP base

df_currency_mini = pd.read_csv(currency_data.filename, index_col=(0, 1), header=0)
curr_last_date = df_currency_mini.index.levels[0][-1]

df_currency_mini = df_currency_mini.loc[
    (df_currency_mini.index.get_level_values(1).isin(currency_data.bases))
    & (df_currency_mini.index.get_level_values(0) == curr_last_date)
]
df_currency_mini = pd.DataFrame(df_currency_mini.droplevel(0))

currency_dict = {}
for curr in target_currencies:
    currency_dict[curr] = {
        "Buy": df_currency_mini.at[curr, "GBP"],
        "Sell": df_currency_mini.at["GBP", curr],
    }

df_currency_mini = pd.DataFrame.from_dict(currency_dict, orient="index")
df_currency_mini = (
    df_currency_mini.round(5)
    .reset_index()
    .rename(columns={"index": "Currency"})
    .sort_values("Currency", axis=0)
)

df_currency = pd.read_csv(currency_data.filename, index_col=(0, 1), header=0)

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
                "paddingLeft": "5px",
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
                "paddingLeft": "5px",
            },
        ),
        dcc.Graph(
            "graph3", style={"width": "73%", "display": "inline-block", "margin": "3"}
        ),
    ],
    style=style_div,
)

sales_tab_content = (
    html.Div(
        [
            html.Div(
                dcc.Markdown(
                    """Sales data is random, source file available on the github repo."""
                ),
                style={
                    **style_div,
                    **{
                        "paddingTop": "3px",
                        "paddingBottom": "2px",
                        "paddingLeft": "2px",
                        "paddingRight": "2px",
                    },
                },
            ),
            html.P(" "),
            sales_scatter_div,
            html.P(" "),
            sales_line_div,
        ]
    ),
)


#####
currency = html.Div(
    [
        html.Div(
            [
                html.Label(f"Currency rates as at {curr_last_date}:"),
                dash_table.DataTable(
                    data=df_currency_mini.to_dict(orient="records"),
                    columns=[{"id": c, "name": c} for c in df_currency_mini.columns],
                    id="currency-table",
                    selected_cells=[{"row": 0, "column": 1, "column_id": "Buy"}],
                ),
            ],
            style={
                "width": "25%",
                "float": "left",
                "verticalAlign": "center",
                "paddingTop": "25px",
                "paddingLeft": "5px",
            },
        ),
        html.Div(
            dcc.Graph(id="graph-currency"),
            style={"display": "inline-block", "width": "73%", "margin": "3"},
        ),
    ],
    style={**style_div, **{"height": "100%"}},
)

currency_tab_content = html.Div([currency], style=style_div)


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
    style=style_div,
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
    style={"backgroundColor": colors["bg"], "height": "100%"},
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


@app.callback(
    Output("graph-currency", "figure"), [Input("currency-table", "selected_cells")]
)
def update_graph_currency(selection):
    fig = go.Figure(layout={"title": "GBP Currency Rates"})
    for item in selection:
        if item["column"] == 1:
            base = df_currency_mini.iloc[item["row"]]["Currency"]
            target = "GBP"
        elif item["column"] == 2:
            base = "GBP"
            target = df_currency_mini.iloc[item["row"]]["Currency"]
        else:
            base = "GBP"
            target = "GBP"
        fig.add_trace(
            go.Scatter(
                x=df_currency[
                    df_currency.index.get_level_values(1) == base
                ].index.get_level_values(0),
                y=df_currency[df_currency.index.get_level_values(1) == base][
                    target
                ].values,
                name=f"{target}/{base}",
                mode="lines",
            )
        )
    return fig


# start Flask server
if __name__ == "__main__":
    app.run_server(debug=False)
