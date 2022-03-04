import altair as alt
import pandas as pd
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, Input, Output

df = pd.read_csv("data/processed/clean_df.csv")

#Data wrangling
for i, movie in enumerate(df['duration'].str.split()):
    df['duration'][i] = int(movie[0])

df = df.assign(country=df["country"].str.split(", ")).explode("country").dropna()

app = Dash(__name__)
server = app.server 

app.layout = html.Div([
        dbc.Label("Year", html_for="range-slider"),
        dcc.RangeSlider(id='year', min = min(df['release_year']), max= max(df['release_year']), value=[1995, 2020], marks={
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
        dcc.RangeSlider(id='duration', min = min(df['duration']), max = max(df['duration']), value=[60, 120], marks={
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

@app.callback(
    Output('bar', 'srcDoc'),
    Input('year','value'),
    Input('duration','value'))

def plot_altair(year_range, duration_range):
    chart = alt.Chart(df[(df["release_year"] > year_range[0]) & (df["release_year"] < year_range[1]) 
                & (df["duration"] > duration_range[0])
                & (df["duration"] < duration_range[1])],
        title='Which Country Make the Most Movies ?').mark_bar().encode(
    alt.X('country', sort='-y', title='Country'),
    alt.Y('count()', title='Number of Movies Produced'),
    color=alt.condition(
        alt.datum.country == 'United State',  
        alt.value('oeange'),     # which sets the bar orange.
        alt.value('steelblue')
    )).interactive()
    return chart.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)