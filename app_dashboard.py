import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from src.graph import matchresult, homeawayrecord, rivalresult, showrivaldataframe

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWlwgP.css']

app = dash.Dash(__name__, external_stylesheets = external_stylesheets)

football = pd.read_csv('football.csv')
football['date'] = pd.to_datetime(football['date'])

app.layout = html.Div(children=[
    html.H1('International Football Dashboard', style = {'text-align' : 'center','padding' : '25px'}),
    html.P('Created by Fandri', style = {'text-align' : 'center'}),

    html.Div(children = [
        html.P('Choose country : ', className = 'col-3',style = {'margin-left' : '0px'}),
        html.P('n-year : ', className = 'col-3',style = {'margin-left' : '0px'})
        ], className = 'row'),
    html.Div(children = [
        html.Div(dcc.Input(id='choose-country', value='Indonesia', type='text'),className = 'col-3', style = {'margin-left' : '0px'}),
        html.Div(dcc.Input(id='n-year', value=15, type='number'),className = 'col-3', style = {'margin-left' : '0px'})
        ], className = 'row'),
    ## Add search button
    html.Div(html.Button('Search', id = 'search'), style = {'margin-top' : '25px', 'margin-bottom' : '25px'}),
    ## Add tab
    dcc.Tabs(value = 'tabs', id = 'tabs-1',children = [
        dcc.Tab(label= 'Match Result', value = 'tab-nol', children = [
            ## Add graph
            html.Div(children = dcc.Graph(
                id='total-bar-chart',
                figure = matchresult(football, 'Indonesia', 15)
            ), className = 'col-12')
        ]
        ),
        dcc.Tab(label= 'location-record', value = 'tab-satu', children = [
            ## Add graph
            html.Div(children = dcc.Graph(
                id='pie-chart',
                figure=homeawayrecord(football, 'Indonesia', 15)
            ), className = 'col-12')
        ]
        ),
        dcc.Tab(label= 'rival-tab', value = 'tab-dua', children = [
            ## Add graph
            html.Div(children = dcc.Graph(
                id='rival-chart',
                figure=rivalresult(football, 'Indonesia')
            ), className = 'col-12')
        ]
        ),
        dcc.Tab(label= 'head-to-head', value = 'tab-tiga', children = [
            ## Add graph
            html.P('Choose Rival : '),
            html.Div(dcc.Input(id='rival-input', value='Malaysia', type='text')),
            html.Div(html.Button('Search', id = 'rival-search'), style = {'margin-top' : '25px', 'margin-bottom' : '25px'}),
            html.Div(id = 'rival-form', children = showrivaldataframe(football, 'Indonesia', 'Malaysia'))

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

## Input awal,(pilih negara dan jumlah tahun)
@app.callback(
    [Output(component_id = 'total-bar-chart', component_property = 'figure'),
    Output(component_id = 'pie-chart', component_property = 'figure'),
    Output(component_id = 'rival-chart', component_property = 'figure')],
    [Input(component_id = 'search', component_property = 'n_clicks')],
    [State(component_id = 'choose-country', component_property = 'value'),
    State(component_id = 'n-year', component_property = 'value')]
)

def show_graph(n_clicks, x1, x2):
    bar_chart = matchresult(football, x1, x2)
    pie_chart = homeawayrecord(football, x1, x2)
    rival_bar = rivalresult(football, x1)
    return bar_chart, pie_chart, rival_bar



## Input kedua,(pilih negara rival)
@app.callback(
    Output(component_id = 'rival-form', component_property = 'children'),
    [Input(component_id = 'rival-search', component_property = 'n_clicks')],
    [State(component_id = 'choose-country', component_property = 'value'),
    State(component_id = 'rival-input', component_property = 'value')])

def show_graph(n_clicks, x1, x2):
    rival_table = showrivaldataframe(football, x1, x2)
    return rival_table


if __name__ == '__main__':
    app.run_server(debug = True)
