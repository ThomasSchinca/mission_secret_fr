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

# Initial game state
word_to_guess, guessed_letters, attempts_left = setup_game()

app.layout = html.Div([
    
    html.H1(children='Bonjour Markéta',style = {'textAlign': 'center','marginBottom':40,'marginTop':20}),
    html.Div([dcc.Markdown('''
        Vážená Markéto,
        Poslední zkouška se točí kolem slov. Pro špiona je nezbytné ovládat slova dovedně.
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
        }),dcc.Markdown('Test 3',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(done),style={
            'height': '25px','width': '25px','margin-left':'12px'
        }),dcc.Markdown('Test 4',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(load),style={
            'height': '25px','width': '25px','margin-left':'12px'
        })],style={'display':'flex','flex-direction':'row','marginBottom':20,'marginTop':20}),
    html.Hr(style={'width': '70%','margin':'auto'}),
    html.Div(
        style={"display": "flex", "flexDirection": "column", "alignItems": "center", "justifyContent": "center", "height": "30vh"},
        children=[
            html.H1("Guess the Word", style={"fontSize": "24px", "marginBottom": "10px"}),
            html.Div(id="word-display",children=["_"] * len(word_to_guess), style={"fontSize": "24px", "marginBottom": "10px"}),
            dcc.Input(id="input-letter", type="text", maxLength=1, style={"fontSize": "18px", "marginBottom": "10px"}),
            html.Button("Guess", id="guess-button", n_clicks=0, style={"fontSize": "18px", "padding": "10px 20px"}),
            html.Div(id="attempts-left", children=f"Attempts Left: {attempts_left}", style={"fontSize": "18px", "marginTop": "10px"}),
            html.Div(id="game-status", children="", style={"fontSize": "24px", "marginTop": "20px"}),
        ])
])

@app.callback(
    Output("word-display", "children"),
    Output("attempts-left", "children"),
    Output("game-status", "children"),
    State("input-letter", "value"),
    State("word-display", "children"),
    State("attempts-left", "children"),
    State("game-status", "children"),
    Input("guess-button", "n_clicks"),
)
def update_game_state(input_letter, current_word_display, current_attempts_left, current_game_status, n_clicks):
    global word_to_guess, guessed_letters, attempts_left
    
    if current_game_status == "Game Over":
        return current_word_display, f"Attempts Left: {attempts_left}", "Game Over"
    elif current_game_status == "Congratulations! You've won!":
        return current_word_display, f"Attempts Left: {attempts_left}", "Congratulations! You've won!"
    if n_clicks > 0 and input_letter and input_letter.isalpha():
        letter = input_letter.lower()
        
        if letter in guessed_letters:
            return current_word_display, current_attempts_left, "Letter already guessed!"
        
        guessed_letters.add(letter)
        
        if letter in word_to_guess:
            word_display = [
                letter if word_to_guess[i] == letter else current_word_display[i]
                for i in range(len(word_to_guess))
            ]
            
            if "_" not in word_display:
                return word_display, current_attempts_left, dcc.Markdown("Congratulations! [You've won!](https://docs.google.com/forms/d/e/1FAIpQLSfp5Ja6PFaOH8SjWd_NRtwf_F4r-i7lKjYswCfUkkoTGSD3lg/viewform?usp=sf_link)")
            current_game_status=''
        else:
            attempts_left -= 1
            if attempts_left == 0:
                return current_word_display, f"Attempts Left: {attempts_left}", "Game Over"
            current_game_status=''
            word_display=current_word_display
        return word_display, f"Attempts Left: {attempts_left}", current_game_status
    
    return current_word_display, current_attempts_left, current_game_status

if __name__ == "__main__":
    app.run_server(debug=True)
