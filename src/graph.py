import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

football = pd.read_csv('football.csv')

def matchresult(result, country, year):
    country = country.capitalize()
    france = result[(result['home_team'] == country) | (result['away_team'] == country)]

    france['win'] = france['who wins'].apply(lambda x : 1 if x == country else 0)
    france['draw'] = france['who wins'].apply(lambda x : 1 if x == 'draw' else 0)
    france['lose'] = france['who wins'].apply(lambda x : 1 if (x != country)&(x != 'draw') else 0)
    franceYear = france.groupby('year')
    # franceYear.count().head()

    franceWin = franceYear.agg({'win' : 'sum', 'draw' : 'sum', 'lose' : 'sum'})
    
    # plotMatch = go.Scatter(x = indonesiaYear.count().index, y = indonesiaYear.count()['win'], mode = 'lines+markers', name = 'Indonesia-match')
    figure = {
                'data': [
                    {'x': franceWin.tail(year).index, 'y': franceWin['win'].tail(year), 'type': 'bar', 'name': 'win'},
                    {'x': franceWin.tail(year).index, 'y': franceWin['draw'].tail(year), 'type': 'bar', 'name': 'draw'},
                    {'x': franceWin.tail(year).index, 'y': franceWin['lose'].tail(year), 'type': 'bar', 'name': 'lose'}
                ],
                'layout': {'title': '{}\'s Match Result in last {} Years'.format(country, year), 'barmode' : 'stack'}
            }
    return figure