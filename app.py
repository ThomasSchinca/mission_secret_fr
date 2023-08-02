# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 15:03:09 2023

@author: thoma
"""

import base64
import io
import numpy as np
import dash
from dash.dependencies import Input, Output, State
from dash import dcc, html, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

external_stylesheets=[dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Mission de Markéta' 
app._favicon = ("question.ico")
server = app.server

done = base64.b64encode(open('done.png', 'rb').read()).decode('ascii')
load = base64.b64encode(open('load.png', 'rb').read()).decode('ascii')
ndone = base64.b64encode(open('ndone.png', 'rb').read()).decode('ascii')

sudoku_puzzle = pd.DataFrame(np.array([
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]))
sudoku_puzzle = sudoku_puzzle.reset_index()
sudoku_puzzle.iloc[:,0]=sudoku_puzzle.iloc[:,0]+1
sudoku_puzzle[sudoku_puzzle==0]=float('NaN')
sudoku_results = pd.DataFrame(np.array([
    [5, 3, 4, 6, 7, 8, 9, 1, 2],
    [6, 7, 2, 1, 9, 5, 3, 4, 8],
    [1, 9, 8, 3, 4, 2, 5, 6, 7],
    [8, 5, 9, 7, 6, 1, 4, 2, 3],
    [4, 2, 6, 8, 5, 3, 7, 9, 1],
    [7, 1, 3, 9, 2, 4, 8, 5, 6],
    [9, 6, 1, 5, 3, 7, 2, 8, 4],
    [2, 8, 7, 4, 1, 9, 6, 3, 5],
    [3, 4, 5, 2, 8, 6, 1, 7, 9]
]))

sudoku_puzzle.columns=[' ','A','B','C','D','E','F','G','H','I']

app.layout = html.Div([
    
    html.H1(children='Bonjour Markéta',style = {'textAlign': 'center','marginBottom':40,'marginTop':20}),
    html.Div([dcc.Markdown('''
        Vážená Markéto,
        V tomto srpnovém měsíci má francouzská vláda tu čest svěřit vám misi nesmírné důležitosti. Vaše pověst jako zkušené a oddané špionky nás přesvědčila, že jste ideální osobou pro zvládnutí této klíčové úlohy.
        Vaše tajná mise, pokud ji přijmete, proběhne po celý srpen a bude obsahovat čtyři náročné testy, jeden každý týden. Každý test bude zaměřen na hodnocení vašich mimořádných vlastností jako špionky a vaší schopnosti přizpůsobit se nejnáročnějším situacím.
        Vězte, že úspěch v každém testu bude bohatě odměněn, a na konci této mise na vás čeká zvláštní překvapení. Jsme přesvědčeni, že se této úlohy zhostíte s patřičnou hrdostí a váš oddaný přístup k povinnosti přispěje k ochraně naší země.
        Hodně štěstí, Markéto, ať vás tato mise nechá zazářit jako hvězda na noční obloze!
        Váš vládní kontakt,
        Kapitán Dupont.
        ''',
        style={'width': '100%','margin-left':'15px','margin-right':'15px'},
    )]),
    html.Hr(style={'width': '70%','margin':'auto'}),
    html.Div([dcc.Markdown('Test 1',style={'margin-left':'350px'}),html.Img(src='data:image/png;base64,{}'.format(done),style={
            'height': '25px','width': '25px','margin-left':'12px'
        }),dcc.Markdown('Test 2',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(ndone),style={
            'height': '25px','width': '25px','margin-left':'12px'
        }),dcc.Markdown('Test 3',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(ndone),style={
            'height': '25px','width': '25px','margin-left':'12px'
        }),dcc.Markdown('Test 4',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(ndone),style={
            'height': '25px','width': '25px','margin-left':'12px'
        })],style={'display':'flex','flex-direction':'row','marginBottom':20,'marginTop':20}),
    html.Hr(style={'width': '70%','margin':'auto'}),
    html.H5(children='Good luck !',style = {'textAlign': 'center','marginBottom':20,'marginTop':20}),
     html.Div([dash_table.DataTable(editable=True,
         style_header={
        'backgroundColor': 'grey'
    },
    style_cell={
                'textAlign': 'center',
                'backgroundColor': [
                    ['lightgrey' if (row // 3) % 2 == 0 and (col // 3) % 2 == 0
                     else 'grey' if (row // 3) % 2 == 0 and (col // 3) % 2 != 0
                     else 'grey' if (row // 3) % 2 != 0 and (col // 3) % 2 == 0
                     else 'lightgrey'
                     for col in range(9)]
                    for row in range(9)
                ]
            },
        data=sudoku_puzzle.to_dict('records'), columns=[{"name": i, "id": i} for i in sudoku_puzzle.columns])],
         style={'width': '30%','margin':'auto'}),
    html.Div([
        "I3 * H5 * B9  = ",
        dcc.Input(id='my-input', value='Maybe 8 ?', type='text')
    ],style={'margin-left':'550px','marginTop':20}),
    html.Div(id='print',style={'margin-left':'550px'})
])


@app.callback(Output('print', 'children'),
              Input('my-input', 'value'))

def update_output(input_1):
    if input_1 == '252':
        ret = dcc.Markdown('Congrats. You can pass to the next [test](https://docs.google.com/forms/d/e/1FAIpQLSeGouQx-YEYVJJ1k7WAhDldYb9aqxMGzvi11EjPB0ywVvaaaw/viewform?usp=sf_link)')
    elif input_1 == 'Maybe 8 ?' or input_1 == '' :
        ret= '   '
    else:    
        ret = 'Nope, it is a mistake.'
    return ret

if __name__ == '__main__':
    app.run(debug=True)