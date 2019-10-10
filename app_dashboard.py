import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from src.graph import matchresult

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWlwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

football = pd.read_csv('football.csv')

app.layout = html.Div(children=[
    html.H1('Football Dashboard', style = {'text-align' : 'center','padding' : '25px'}),
    html.P('Created by Fandri', style = {'text-align' : 'center'}),

    html.Div(children = [
        html.P('Choose country : ', className = 'col-3',style = {'margin-left' : '25px'}),
        html.P('n-year : ', className = 'col-3',style = {'margin-left' : '25px'})
        ], className = 'row'),
    html.Div(children = [
        html.Div(dcc.Input(id='choose-country', value='Indonesia', type='text'),className = 'col-3', style = {'margin-left' : '25px'}),
        html.Div(dcc.Input(id='n-year', value=15, type='number'),className = 'col-3', style = {'margin-left' : '25px'})
        ], className = 'row'),
    ## Add search button
    html.Div(html.Button('Search', id = 'search'), style = {'padding' : '15px'}),
    ## Add tab
    dcc.Tabs(value = 'tabs', id = 'tabs-1',children = [
        dcc.Tab(label= 'Match Result', value = 'tab-nol', children = [
            ## Add graph
            html.Div(children = dcc.Graph(
                id='graph-scatter',
                figure = matchresult(football, 'Indonesia', 15)
            ), className = 'col-12')
        ]
        ),
        dcc.Tab(label= 'Home-record', value = 'tab-satu', children = [
            ## Add graph
            html.P('lalala')
        ]
        )
    ], content_style = {
        'fontFamily' : 'Arial',
        'borderBottom' : '1px solid #d6d6d6',
        'borderLeft' : '1px solid #d6d6d6',
        'borderRight' : '1px solid #d6d6d6',
        'padding' : '44px'
    })

    ],
    style = {
    'maxWidth': '1100px',
    'margin' : '0 auto'
}
)


@app.callback(
    Output(component_id = 'graph-scatter', component_property = 'figure'),
    [Input(component_id = 'search', component_property = 'n_clicks')],
    [State(component_id = 'choose-country', component_property = 'value'),
    State(component_id = 'n-year', component_property = 'value')]
)

def show_bar_graph(n_clicks, x1, x2):
    figure = matchresult(football, x1, x2)
    return figure




if __name__ == '__main__':
    app.run_server(debug = True)
