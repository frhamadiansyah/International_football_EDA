import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWlwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

football = pd.read_csv('results.csv')

app.layout = html.Div(children=[
    html.H1('Football Dashboard'),
    html.P('Created by Fandri'),
    ]
)




if __name__ == '__main__':
    app.run_server(debug = True)
