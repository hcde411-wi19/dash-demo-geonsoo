# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import numpy as np
import pandas as pd

# initialize Dash app and initialize the static folder
app = dash.Dash(__name__, static_folder='static')
df = pd.read_csv('static/daily_MSFT.csv')


#print(df.iloc[:50, :2])

series = []

for i in df.iloc[:200, 0:1]:
    series.append(
        go.Scatter(
            x=df["timestamp"],
            y=df["open"],
            mode='lines+markers',
            name="open"
        )

    )

# initialize Dash app
app = dash.Dash(__name__)

# set up an layout
app.layout = html.Div(children=[
    # H1 title on the page
    html.H1(children='Microsoft Stock Line Chart'),


    # append the visualization to the page
    dcc.Graph(
        id='linechart',
        figure={
            # configure the data
            'data': series,
            'layout': {
                'Microsoft': 'Stock Information (Open Price)',
            }
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)