# Usefule sources:
# https://dash.plotly.com/basic-callbacks
# https://stackoverflow.com/questions/63589249/plotly-dash-display-real-time-data-in-smooth-animation

import pandas as pd
import plotly.express as px
import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output


def new_data(url):
    df = pd.read_json(url)
    df['lon'] = df.loc['longitude', 'iss_position']
    df['lat'] = df.loc['latitude', 'iss_position']
    df.reset_index(drop=True, inplace=True)
    df.drop(['iss_position', 'message'], axis=1, inplace=True)
    df.drop(0, axis=0, inplace=True)
    return df


url = 'http://api.open-notify.org/iss-now.json'
df = new_data(url)      # starting point

fig = px.line_geo(df, lat='lat', lon='lon', title='Where is ISS Now', projection='natural earth')
app = dash.Dash(__name__, update_title=None)  # remove "Updating..." from title
app.layout = html.Div([dcc.Graph(id='graph', figure=fig), dcc.Interval(id="interval")])

@app.callback(Output('graph', 'extendData'), [Input('interval', 'n_intervals')])
def add_data(n_intervals):
    df = new_data(url)
    return {'lon': [df['lon']], 'lat': [df['lat']]}


if __name__ == '__main__':
    app.run_server()