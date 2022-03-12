from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd

alt.data_transformers.disable_max_rows()

data = pd.read_csv("data/processed/clean_df.csv")

#Sufang data wrangling
data['duration'] = data['duration'].apply(lambda x: int(x.split(" ")[0]))

data = data.assign(country=data["country"].str.split(", ")).explode("country").dropna()

# Jasmine data wrangling
data["cast_list"] = data["cast"].str.split(",")
data["cast_count"] = data["cast_list"].str.len()
cast_df = data[["title", "cast", "listed_in", "cast_count", "release_year"]]

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

app = Dash(external_stylesheets=[dbc.themes.MINTY])
server = app.server

app.title = "Netflix Movie Dashboard"

app.layout = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            dbc.Col(
                html.Div("Netflix Movie Dashboard: Visualize movie trends on the world's most popular streaming platform!"),
                width={"size": 3, "offset": 5},
                style={"font-weight": "bold"},
            )
        ),
        dbc.Row(
            [
                # Sufang Part
                dbc.Col(
                    dbc.Card(dbc.CardBody([
                        html.H5(""),
                        html.Div([
        dbc.Label("Year", html_for="range-slider"),
        dcc.RangeSlider(id='year', min = min(data['release_year']), max= max(data['release_year']), value=[1995, 2015], marks={
                                        1950: "1950",
                                        1955: "1955",
                                        1960: "1960",
                                        1965: "1965",
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
                                    },),
        dbc.Label("Duration", html_for="range-slider"),
        dcc.RangeSlider(id='duration', min = min(data['duration']), max = max(data['duration']), value=[90, 120], marks={
                                        10: "10",
                                        30: "30",
                                        50: "50",
                                        70: "70",
                                        90: "90",
                                        110: "110",
                                        130: "130",
                                        150: "150",
                                        170: "170",
                                        190: "190",
                                        210: "210",
                                        230: "230",
                                    },),
        html.Iframe(
            id='bar',
            style={'border-width': '0', 'width': '100%', 'height': '400px'})])

                
                    ]
                    )),
                ),
            ]
        ),
        html.Br(),
        dbc.Row(
            [

                # Jasmine Part
                dbc.Col(
                    dbc.Card(dbc.CardBody(
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
                                       ),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                        ]
                    )
                    ))
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
            ], title="Number of film produced based on movie rating"
        )
        .mark_line().encode(
            x=alt.X("release_year:O",
                title="Movie Release Year",
                # scale=alt.Scale(domain=[1942, 2020]),
                # axis=alt.Axis(format='f')
                ),

            y=alt.Y("count():Q",
                title="Number of Movie Produced",
                axis=alt.Axis(tickMinStep=1)
                ),

            color=alt.Color('rating:O',
                     scale=alt.Scale(scheme='dark2'), 
                     legend=alt.Legend(title="Rating by color")))
        .transform_filter(alt.FieldOneOfPredicate(field="rating", oneOf=ratings))
        .interactive()
    )
    return line_plot.to_html()


# Jasmin Call back
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

# Sufang Call Back
@app.callback(
    Output('bar', 'srcDoc'),
    Input('year','value'),
    Input('duration','value'))

# Sufang plot function
def plot_altair(year_range, duration_range):
    chart = alt.Chart(data[(data["release_year"] > year_range[0]) & (data["release_year"] < year_range[1]) 
                & (data["duration"] > duration_range[0])
                & (data["duration"] < duration_range[1])],
        title='Which Country Make the Most Movies ?').mark_bar().encode(
    alt.X('country', sort='-y', title='Country'),
    alt.Y('count()', title='Number of Movies Produced'),
    color=alt.condition(
        alt.datum.country == 'United State',  
        alt.value('orange'),     # which sets the bar orange.
        alt.value('steelblue')
    )).interactive()
    return chart.to_html()


if __name__ == "__main__":
    app.run_server(debug=True)
