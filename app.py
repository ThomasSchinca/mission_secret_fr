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

# List of words for the Hangman game
words = [
    "paris", "versailles", "marseille", "aixenprovence", "toulon","grenoble", "clermontferrand", "saintetienne", "chambery",
    "toulouse", "montpellier", "perpignan", "carcassonne",
    "amiens", "roubaix", "tourcoing","nantes", "saintnazaire", "cholet",
    "bordeaux", "limoges", "poitiers", "chateauroux"
]
# Initial setup
def setup_game():
    word_to_guess = random.choice(words)
    guessed_letters = set()
    attempts_left = 5
    return word_to_guess, guessed_letters, attempts_left

word_to_guess, guessed_letters, attempts_left = setup_game()


external_stylesheets=[dbc.themes.LUX]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = 'Mission de Markéta' 
app._favicon = ("question.ico")
server = app.server

done = base64.b64encode(open('done.png', 'rb').read()).decode('ascii')
load = base64.b64encode(open('load.png', 'rb').read()).decode('ascii')
ndone = base64.b64encode(open('ndone.png', 'rb').read()).decode('ascii')

app.layout = html.Div([
    
    html.H1(children='Bonjour Markéta',style = {'textAlign': 'center','marginBottom':40,'marginTop':20}),
    html.Div([dcc.Markdown('''
        Vážená Markéto,
        Úžasná práce! Zvládli jste všechny úkoly. Gratulujeme!
        Vaše odměna je na stole Thomase, v jeho pokoji. Dali jsme ji sem, protože je momentálně pryč.
        Nápovědu pro váš další úkol najdete na vašem pracovním laptopu.
        Francie vám děkuje. Manu je na vás hrdý.
        Kapitán Dupont.
        ''',
        style={'width': '80%','textAlign': 'center','margin-left':'150px','margin-right':'150px'},
    )]),
    html.Hr(style={'width': '70%','margin':'auto'}),
    html.Div([dcc.Markdown('Test 1',style={'margin-left':'350px'}),html.Img(src='data:image/png;base64,{}'.format(done),style={
            'height': '25px','width': '25px','margin-left':'12px'
        }),dcc.Markdown('Test 2',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(done),style={
            'height': '25px','width': '25px','margin-left':'12px'
        }),dcc.Markdown('Test 3',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(done),style={
            'height': '25px','width': '25px','margin-left':'12px'
        }),dcc.Markdown('Test 4',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(done),style={
            'height': '25px','width': '25px','margin-left':'12px'
        })],style={'display':'flex','flex-direction':'row','marginBottom':20,'marginTop':20}),
    html.Hr(style={'width': '70%','margin':'auto'}),
    html.Div([dcc.Markdown('''6-1-1''',
        style={'textAlign': 'center','marginTop':2000},
    )]),
])
            
if __name__ == "__main__":
    app.run_server(debug=True)
