from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd

alt.data_transformers.disable_max_rows()

data = pd.read_csv("data/processed/clean_df.csv")

# Jasmine data wrangling
data["cast_list"] = data["cast"].str.split(",")
data["cast_count"] = data["cast_list"].str.len()
cast_df = data[["title", "cast", "listed_in", "cast_count", "release_year"]]


# Mahsa data wrangling
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
                html.Div("Netflix Movie Trends"),
                width={"size": 3, "offset": 5},
                style={"font-weight": "bold"},
            )
        ),
        dbc.Row(
            [
                # Sufang Part
                dbc.Col(
                    dbc.Card(dbc.CardBody(html.H5("Sufang Part"))),
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [

                # Jasmine Part
                dbc.Col(
                    html.Div(
                        [
                            html.Iframe(
                                id="scatter",
                                style={
                                    'border-width': '0',
                                    'width': '100%',
                                    'height': '400px'
                                }
                            ),
                            dcc.Slider(id='xslider',
                                       min=1942, max=2020,
                                       value=2020,
                                       marks={
                                           1942: '1942',
                                           1962: '1962',
                                           1980: '1980',
                                           2000: '2000',
                                           2020: '2020'
                                       }
                                       )
                        ]
                    )
                ),


                # Mahsa Part
                dbc.Col(
                    dbc.Card(dbc.CardBody(
                    [
                        html.Div(
                            [
                                html.Iframe(
                                    id="line",
                                    style={
                                        "border-width": "0",
                                        "width": "100%",
                                        "height": "400px",
                                    },
                                ),
                                dcc.RangeSlider(
                                    id="range-slider",
                                    min=1942,
                                    max=2020,
                                    value=[2003, 2020],
                                    marks={
                                        1942: '1942',
                                        1962: '1962',
                                        1980: '1980',
                                        2000: '2000',
                                        2020: '2020'
                                        # 1970: "1970",
                                        # 1975: "1975",
                                        # 1980: "1980",
                                        # 1985: "1985",
                                        # 1990: "1990",
                                        # 1995: "1995",
                                        # 2000: "2000",
                                        # 2005: "2005",
                                        # 2010: "2010",
                                        # 2015: "2015",
                                        # 2020: "2020",
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
                            ]
                        ),
                    ]
                ))),
            ]
        ),
    ]
)


@app.callback(
    Output("line", "srcDoc"),
    Input("range-slider", "value"),
    Input("rating_widget", "value"),
)
# Mahsa plot function
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


# this doesnt appear to do anything
@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xslider', 'value'),
)
# Jasmine plot function
def plot_cast(xmax):
    cast_plot = alt.Chart(cast_df[cast_df["release_year"] < xmax], title="Average Cast Size Per Year").mark_circle().encode(
        x=alt.X("release_year",
                title="Movie Release Year",
                scale=alt.Scale(domain=[1942, 2020]),
                axis=alt.Axis(format='f')),

        y=alt.Y("mean(cast_count)",
                title="Average Cast Size",
                axis=alt.Axis(tickMinStep=1)
                )
    )
    return cast_plot.to_html()


def update_output(xmax):
    return plot_cast(xmax)


if __name__ == "__main__":
    app.run_server(debug=True)
