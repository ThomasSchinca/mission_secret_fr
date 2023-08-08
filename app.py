# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:03:09 2023

@author: thoma
"""

import base64
import io
import numpy as np
import dash
from dash.dependencies import Input, Output, State,ALL
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import random

external_stylesheets=[dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Mission de Markéta' 
app._favicon = ("question.ico")
server = app.server

done = base64.b64encode(open('done.png', 'rb').read()).decode('ascii')
load = base64.b64encode(open('load.png', 'rb').read()).decode('ascii')
ndone = base64.b64encode(open('ndone.png', 'rb').read()).decode('ascii')

num=[1,1,2,2,3,3,4,4,5,5,6,6,7,7,8,8,9,9,10,10,11,11,12,12,13,13,14,14,15,15,16,16]
random.shuffle(num)

app.layout = html.Div([
    
    html.H1(children='Bonjour Markéta',style = {'textAlign': 'center','marginBottom':40,'marginTop':20}),
    html.Div([dcc.Markdown('''
        Vážená Markéto,
        Dobrý špion by měl mít skvělou paměť. Aby ses dostala/o přes další test,
        potřebuješ vyhrát hru "50 odstínů Manu". Musíš najít páry stejné barvy Manu. 
        Pokud nenajdeš pár, vybrané karty se ihned schovají. Někdy se hra trochu sekne,
        takže neváhej/a klikat několikrát pro výběr karty.
        Hodně štěstí!
        Kapitán Dupont.
        ''',
        style={'width': '100%','margin-left':'15px','margin-right':'15px'},
    )]),
    html.Hr(style={'width': '70%','margin':'auto'}),
    html.Div([dcc.Markdown('Test 1',style={'margin-left':'350px'}),html.Img(src='data:image/png;base64,{}'.format(done),style={
            'height': '25px','width': '25px','margin-left':'12px'
        }),dcc.Markdown('Test 2',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(done),style={
            'height': '25px','width': '25px','margin-left':'12px'
        }),dcc.Markdown('Test 3',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(ndone),style={
            'height': '25px','width': '25px','margin-left':'12px'
        }),dcc.Markdown('Test 4',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(ndone),style={
            'height': '25px','width': '25px','margin-left':'12px'
        })],style={'display':'flex','flex-direction':'row','marginBottom':20,'marginTop':20}),
    html.Hr(style={'width': '70%','margin':'auto'}),
    dcc.Store(id='memory'),
    dcc.Store(id='memory_found'),
    html.Div([
        html.Button('', id={'type': 'my-button', 'index': i},className='custom-button-clicked')
        for i in range(32)
    ], style={'display': 'grid', 'grid-template-columns': 'repeat(8, 4cm)', 'gap': '10px','margin-left':'75px'}),
    html.Hr(style={'width': '70%','margin':'auto','marginBottom':20,'marginTop':20}),
    html.Div(id='out',style={'textAlign': 'center'})
])
    

@app.callback(
    Output({'type': 'my-button', 'index': ALL}, 'className'),
    Output('memory', 'data'),
    Output('memory_found', 'data'),
    Output('out','children'),
    Input({'type': 'my-button', 'index':ALL}, 'n_clicks'),
    State({'type': 'my-button', 'index': ALL}, 'className'),
    State('memory', 'data'),
    State('memory_found', 'data'),
    prevent_initial_call=True
)

def update_button_class(n_clicks, current_class,memory,memory_found):
    ctx = dash.callback_context
    button_index = ctx.triggered[0]['prop_id'][9:].split(',')[0]
    if int(button_index)==memory:
        raise PreventUpdate
    if memory_found is not None:
        if num[int(button_index)] in memory_found:
            raise PreventUpdate
    if memory == None:
        if n_clicks[int(button_index)] is not None and n_clicks[int(button_index)] % 2 == 1:
            current_class[int(button_index)]='custom-button'+str(num[int(button_index)])
            memory=int(button_index)
        else:
            current_class[int(button_index)]= 'custom-button-clicked'
    else:
        if num[int(button_index)] == num[memory]:
            current_class[int(button_index)]='custom-button'+str(num[int(button_index)])
            if memory_found is not None:  
                memory_found.append(num[int(button_index)])
            else:
                memory_found=[num[int(button_index)]]
            memory = None
        else:
            memory = None
            if memory_found is not None:
                for i in range(32):
                    if num[i] in memory_found:
                        current_class[i]='custom-button'+str(num[i])
                    else:
                        current_class[i]= 'custom-button-clicked'
            else:
                for i in range(32):
                    current_class[i]= 'custom-button-clicked'
    out=' '
    if memory_found is not None:                    
        if len(memory_found)==16:
            out=dcc.Markdown('''# Good job !''')
    return current_class,memory,memory_found,out
if __name__ == '__main__':
    app.run(debug=True)