from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd


data = pd.read_csv('data/processed/clean_df.csv')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
server= app.server

app.layout = dbc.Container([
    html.Br(),
    dbc.Row(dbc.Col(html.Div("Netflix Movie Trend"),
                width={"size": 3, "offset": 5},
                style={'font-weight': 'bold'})),
    dbc.Row(
            [
                dbc.Col(dbc.Card(dbc.CardBody(html.H5('Sufang Part'))),
                       ),
            ]),
    html.Br(),
    dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody(html.H5('Jasmin Part'))),
                       width= 5),
                dbc.Col([
                    dbc.Label("Year", html_for="range-slider"),
                    html.Div([
                    dcc.RangeSlider(id="range-slider", min = 1970, max = 2020, value=[1995, 2020],  marks={
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
            }),
         html.Iframe(
                id='line',
                style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    ])
                ]),
            ]
        ),
    ])


@app.callback(
    Output('line', 'srcDoc'),
    Input('range-slider', 'value'))

def rating_plot(year_range):
    line_plot = alt.Chart(data[(data['release_year']> year_range[0]) & (data['release_year']< year_range[1])]).mark_line().encode(
                x='release_year:O',
                y='count():Q',
                color='rating:O').interactive()
    return line_plot.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)