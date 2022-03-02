from dash import Dash, html, dcc, Input, Output
import altair as alt
import dash_bootstrap_components as dbc
import pandas as pd


data = pd.read_csv('data/processed/clean_df.csv')
plot=alt.Chart(data).mark_line().encode(
         x='release_year',
         y='count()',
         color='rating')

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# server= src.app.server

app.layout = dbc.Container([
    html.H1('Netflix Movie Trend'),
    dbc.Row(
        html.Iframe(
                id='line',
                srcDoc=plot.to_html(),
                style={'border-width': '0', 'width': '100%', 'height': '400px'})
    )
    ])



# def plot_altair():
#     plot=alt.Chart(data).mark_line().encode(
#         x='release_year',
#         y='count()',
#         color='rating')
#     return plot.to_html()

if __name__ == '__main__':
    app.run_server(debug=True)