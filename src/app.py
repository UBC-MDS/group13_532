from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd


data = pd.read_csv("data/processed/clean_df.csv")

rating_list = [
    "TV-G",
    "TV-14",
    "TV-MA",
    "TV-PG",
    "R",
    "TV-Y7",
    "TV-Y",
    "PG",
    "G",
    "PG-13",
    "NR",
    "UR",
    "TV-Y7-FV",
    "NC-17",
]

default_rating_list = ["TV-G", "TV-14", "R", "TV-Y", "PG"]

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            dbc.Col(
                html.Div("Netflix Movie Trend"),
                width={"size": 3, "offset": 5},
                style={"font-weight": "bold"},
            )
        ),
        dbc.Row(
            [
                ############## Sufang Part
                dbc.Col(
                    dbc.Card(dbc.CardBody(html.H5("Sufang Part"))),
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [
                ############# Jasmin Part
                dbc.Col(dbc.Card(dbc.CardBody(html.H5("Jasmin Part"))), width=5),
                # Mahsa Part
                dbc.Col(
                    [
                        dbc.Label("Year", html_for="range-slider"),
                        html.Div(
                            [
                                dcc.RangeSlider(
                                    id="range-slider",
                                    min=1970,
                                    max=2020,
                                    value=[1995, 2020],
                                    marks={
                                        1970: "1970",
                                        1975: "1975",
                                        1980: "1980",
                                        1985: "1985",
                                        1990: "1990",
                                        1995: "1995",
                                        2000: "2000",
                                        2005: "2005",
                                        2010: "2010",
                                        2015: "2015",
                                        2020: "2020",
                                    },
                                ),
                                dbc.Label("Rating", html_for="rating_widget"),
                                dcc.Dropdown(
                                    id="rating_widget",
                                    value=default_rating_list,
                                    placeholder="Select Rating...",
                                    options=[
                                        {"label": rating, "value": rating}
                                        for rating in rating_list
                                    ],
                                    multi=True,
                                ),
                                html.Br(),
                                html.Iframe(
                                    id="line",
                                    style={
                                        "border-width": "0",
                                        "width": "100%",
                                        "height": "400px",
                                    },
                                ),
                            ]
                        ),
                    ]
                ),
            ]
        ),
    ]
)


@app.callback(
    Output("line", "srcDoc"),
    Input("range-slider", "value"),
    Input("rating_widget", "value"),
)
def rating_plot(year_range, ratings):
    line_plot = (
        alt.Chart(
            data[
                (data["release_year"] > year_range[0])
                & (data["release_year"] < year_range[1])
            ]
        )
        .mark_line()
        .encode(x="release_year:O", y="count():Q", color="rating:O")
        .transform_filter(alt.FieldOneOfPredicate(field="rating", oneOf=ratings))
        .interactive()
    )
    return line_plot.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)