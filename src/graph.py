import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from datetime import datetime

currentyear = datetime.now().year

football = pd.read_csv('football.csv')
football['date'] = pd.to_datetime(football['date'])

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


def homeawayrecord(result, country, year):
    global currentyear
    country = country.capitalize()
    negara = result[((result['home_team'] == country) | (result['away_team'] == country)) & (result['year'] > currentyear-year)]

    negara['win'] = negara['who wins'].apply(lambda x : 1 if x == country else 0)
    negara['draw'] = negara['who wins'].apply(lambda x : 1 if x == 'draw' else 0)
    negara['lose'] = negara['who wins'].apply(lambda x : 1 if (x != country)&(x != 'draw') else 0)
    
    negaraHome = negara[(negara['home_team'] == country) & (negara['neutral'] == False)]
    negaraNeutral = negara[negara['neutral'] == True]
    negaraAway = negara[(negara['away_team'] == country) & (negara['neutral'] == False)]
    
    columnNegara = {'home' : negaraHome, 'neutral' : negaraNeutral, 'away' :negaraAway}
    
    traces = []
    x = 0
    for i in columnNegara.keys():
        labels = ['win', 'draw',' lose']
        values = [columnNegara[i]['win'].sum(),
                 columnNegara[i]['draw'].sum(),
                 columnNegara[i]['lose'].sum()]
        domain = {'x' : [x , x+0.3], 'y' : [0.1 , 1] }
        trace = go.Pie(labels = labels,
                   values = values,
                   domain = domain,
                   hoverinfo = 'label+percent+name',
                   sort = False, 
                   title = i + ' record\n')
        traces.append(trace)
        x += 0.33
        
    figure = {
        'data' : traces,
        'layout' : {'title' : '{}\'s home-neutral-away record last {} year'.format(country, year), 'titlefont':{'size' : 20}}
    }
    return figure



def rivalresult(result, country):
    country = country.capitalize()
    negara = result[((result['home_team'] == country) | (result['away_team'] == country))]
    
    negara['win'] = negara['who wins'].apply(lambda x : 1 if x == country else 0)
    negara['draw'] = negara['who wins'].apply(lambda x : 1 if x == 'draw' else 0)
    negara['lose'] = negara['who wins'].apply(lambda x : 1 if (x != country)&(x != 'draw') else 0)
    
    daftarRival = (negara['home_team'].value_counts() + negara['away_team'].value_counts()).sort_values(ascending = False)[1:6] 
    listRival = []
    for i in daftarRival.index:
        rival = negara[(negara['home_team'] == i) | (negara['away_team'] == i)]
        listRival.append([i,rival['win'].sum(),rival['draw'].sum(),rival['lose'].sum()])
    
    listRival = pd.DataFrame(listRival, columns = ['rival', 'win', 'draw','lose'])#.sort_values(by = 'win', ascending = False)   

    figure = {
                'data': [
                    {'x': listRival['rival'], 'y': listRival['win'], 'type': 'bar', 'name': 'win'},
                    {'x': listRival['rival'], 'y': listRival['draw'], 'type': 'bar', 'name': 'draw'},
                    {'x': listRival['rival'], 'y': listRival['lose'], 'type': 'bar', 'name': 'lose'}
                ],
                'layout': {'title': 'Top 5 {}\'s Fiercest Rival\'s'.format(country), 'barmode' : 'stack'}
            }
    return figure

def showrivaldataframe(result, country, rival):
    country = country.capitalize()
    rival = rival.capitalize()
    negara = result[((result['home_team'] == country) | (result['away_team'] == country))]
    negaraRival = negara[((negara['home_team'] == rival) | (negara['away_team'] == rival))].tail()
    negaraRival = negaraRival[['date','home_team','home_score','away_score','away_team','tournament','city','country']]
    negaraRival = negaraRival.sort_values(by = 'date', ascending = False)
    tab = dash_table.DataTable(
                id='form-table',
                columns=[{"name": i, "id": i} for i in negaraRival.columns],
                data=negaraRival.to_dict('records'),
                page_action = 'native',
                page_current = 0,
                page_size = 10
            )

    return tab

