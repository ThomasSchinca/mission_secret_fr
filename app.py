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

im=[]
for i in range(1,28):
    im.append(base64.b64encode(open('History/'+str(i)+'.png', 'rb').read()).decode('ascii'))

current_page = "start"
story_data = {
    "start": {
        "text": "Markéta, you are standing outside an embassy in Dublin. What do you do?",
        "choices": [
            {"text": "Enter the embassy through the main entrance.", "next_page": "main_entrance"},
            {"text": "Look for a discreet entrance at the back.", "next_page": "back_entrance"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[0])),
    },
    "main_entrance": {
        "text": "You confidently walk through the main entrance, showing your forged ID to the guards. You find yourself in the embassy's lobby. What's your next move?",
        "choices": [
            {"text": "Approach the receptionist and ask for directions.", "next_page": "receptionist"},
            {"text": "Head straight to the hallway leading to offices.", "next_page": "hallway"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[1])),
    },
    "back_entrance": {
        "text": "You discreetly make your way to the back of the embassy and find a small door. It seems to be locked. What's your plan?",
        "choices": [
            {"text": "Pick the lock using your spy tools.", "next_page": "lock_picking"},
            {"text": "Wait and observe for any embassy staff entering or exiting.", "next_page": "observation"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[2])),
    },
    "receptionist": {
        "text": "You strike up a conversation with the receptionist and gather some information about the embassy layout. She seems suspicious of you. What's your next move?",
        "choices": [
            {"text": "Try to charm her and continue the conversation.", "next_page": "charming"},
            {"text": "Thank her and head to the hallway leading to offices.", "next_page": "hallway"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[3])),
    },
    "hallway": {
        "text": "You find yourself in a hallway lined with office doors. The folder is likely in one of these offices. What's your plan?",
        "choices": [
            {"text": "Start searching offices systematically, starting from the first.", "next_page": "search_first_office"},
            {"text": "Use your intuition to choose a specific office to search.", "next_page": "intuitive_choice"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[4])),
    },
    "lock_picking": {
        "text": "With skillful precision, you pick the lock and slip inside. You find yourself in a dimly lit storage room. What's your next move?",
        "choices": [
            {"text": "Search the storage room for any clues or the folder.", "next_page": "search_storage"},
            {"text": "Try to find a way to access the main hallway of the embassy.", "next_page": "access_main_hallway"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[5])),
    },
    "charming": {
        "text": "Your charming demeanor wins the receptionist over. She offers to show you around. As she leads you, you spot the hallway leading to offices. What do you do?",
        "choices": [
            {"text": "Politely ask her to continue showing you around.", "next_page": "continue_tour"},
            {"text": "Thank her and excuse yourself to explore on your own.", "next_page": "explore_alone"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[6])),
    },
    "search_first_office": {
        "text": "You search the first office thoroughly and find some important documents, but not the folder. What's your next move?",
        "choices": [
            {"text": "Continue searching the remaining offices one by one.", "next_page": "search_remaining_offices"},
            {"text": "Return to the hallway and choose a different office to search.", "next_page": "intuitive_choice"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[7])),
    },
    "intuitive_choice": {
        "text": "You follow your instincts and choose an office to search. Inside, you discover the classified folder hidden among other files. What do you do?",
        "choices": [
            {"text": "Take the folder and leave the office discreetly.", "next_page": "mission_accomplished"},
            {"text": "Take a photo of the folder with your hidden camera and put it back.", "next_page": "stealth_photo"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[8])),
    },
    "search_remaining_offices": {
        "text": "You methodically search the remaining offices but still can't find the folder. Time is running out. What's your plan?",
        "choices": [
            {"text": "Return to the hallway and choose a different office to search.", "next_page": "intuitive_choice"},
            {"text": "You see a little room that might be interesting and hidden. Try this room.", "next_page": "report_failure"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[9])),
    },
    "access_main_hallway": {
        "text": "You manage to sneak into the main hallway undetected. You see the office doors on either side. What's your plan?",
        "choices": [
            {"text": "Search the office doors on one side of the hallway.", "next_page": "search_one_side"},
            {"text": "Carefully search the office doors on both sides of the hallway.", "next_page": "search_both_sides"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[10])),
    },
    "explore_alone": {
        "text": "You explore the embassy alone, trying not to draw attention to yourself. As you wander, you spot the hallway leading to offices. What do you do?",
        "choices": [
            {"text": "Enter the hallway and start searching the offices.", "next_page": "hallway"},
            {"text": "Continue exploring other areas of the embassy.", "next_page": "explore_other_areas"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[10])),
    },
    "mission_accomplished": {
        "text": "Congratulations, Markéta ! You've successfully retrieved the classified folder and completed your mission. Time to make your exit.",
        "choices": [
            {"text": "Report it to your superiors", "next_page": "report_success"},
            {"text": "Celebrate, you clearely deserve it !", "next_page": "police"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[11])),
    },
    "mission_accomplished_full": {
        "text": dcc.Markdown('''Congratulations, Markéta ! You've successfully retrieved the classified
                             folder and even more, gathered more information than needed. 
                             [Your superiors will be happy with your work !](https://docs.google.com/forms/d/e/1FAIpQLSc8WEjaC3ylt97_juz59UYXS4SyXLuFs16QOCZ79Tz1XP7QeQ/viewform?usp=sf_link)'''
                             ),
        "choices": [
            {"text": "Play again", "next_page": "start"},
            {"text": "Play again", "next_page": "start"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[11])),   
    },
    "stealth_photo": {
        "text": "You discreetly take a photo of the folder with your hidden camera. The information is captured. What's your next move?",
        "choices": [
            {"text": "Leave the office and report back to your superiors.", "next_page": "report_success"},
            {"text": "Search for any more valuable information before leaving.", "next_page": "police"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[13])),
    },
    "report_success": {
        "text": "You exit the embassy and report the successful mission to your superiors. But they are not happy, it seems that they want more than just this folder.They ask you to go again and gather more information.",
        "choices": [
            {"text": "Accept the mission.", "next_page": "start"},
            {"text": "Try to negociate and see if you can go home without doing it.", "next_page": "no"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[12])),
    },
    "no": {
        "text": "You try but of course, it's not possible... You work for Manu, you have to show your skills",
        "choices": [
            {"text": "Accept to go back.", "next_page": "start"},
            {"text": "Do not accept but go back anyway, you just have no choice.", "next_page": "start"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[26])),    
    },
    "search_storage": {
        "text": "You search the storage room meticulously and find some useful documents, but not the folder. What's your next move?",
        "choices": [
            {"text": "Exit the storage room and explore other parts of the embassy.", "next_page": "explore_other_areas"},
            {"text": "Try to find another way to access the main hallway.", "next_page": "access_main_hallway"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[14])),
    },
    "continue_tour": {
        "text": "You continue the tour with the receptionist. She shows you various rooms, but you're keen on getting to the offices. What do you do?",
        "choices": [
            {"text": "Politely request to cut the tour short and head to the hallway.", "next_page": "hallway"},
            {"text": "Engage in more conversation to build rapport before making a move.", "next_page": "rapport_building"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[15])),
    },
    "rapport_building": {
        "text": "You engage in a deeper conversation with the receptionist, building rapport. However, time is ticking. What's your plan?",
        "choices": [
            {"text": "Seize a suitable opportunity to excuse yourself and head to the hallway.", "next_page": "hallway"},
            {"text": "Continue the conversation and risk losing valuable time.", "next_page": "continue_conversation"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[16])),
    },
    "continue_conversation": {
        "text": "You talk for hours. You might have an opportunity to have fun but the embassy is now closed. Too bad, you can come back tommorow.",
        "choices": [
            {"text": "Wait for the next day.", "next_page": "start"},
            {"text": "Try to threat the receptionist to find the folder, there is no time left !", "next_page": "police"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[16])),
    },
    "observation": {
        "text": "You discreetly observe embassy staff entering and exiting the door. After a while, an employee enters, and you manage to slip in behind them. Where do you go?",
        "choices": [
            {"text": "Explore the lobby and common areas to gather information.", "next_page": "explore_common_areas"},
            {"text": "Find a way to access the main hallway without drawing attention.", "next_page": "access_main_hallway"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[17])),
    },
    "explore_common_areas": {
        "text": "You explore the common areas of the embassy, learning about its layout. You spot the hallway leading to offices. What's your plan?",
        "choices": [
            {"text": "Enter the hallway and start searching the offices.", "next_page": "hallway"},
            {"text": "Continue exploring other parts of the embassy for more information.", "next_page": "explore_other_areas"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[1])),
    },
    "explore_other_areas": {
        "text": "You decide to explore other areas of the embassy in search of more information. Time is of the essence. What's your plan?",
        "choices": [
            {"text": "Return to the hallway and begin searching the offices.", "next_page": "hallway"},
            {"text": "Continue exploring the remaining areas to gather more intel.", "next_page": "final_exploration"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[18])),
    },
    "final_exploration": {
        "text": "You continue to gather more information in a different area, but luck is not on your side. What's your plan?",
        "choices": [
            {"text": "Go to the basement and try to find more infos there.", "next_page": "secret_tunnel"},
            {"text": "Continue to explore, there is a room with light that could be interesting.", "next_page": "report_failure"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[19])),
    },
    "report_failure": {
        "text": "You enter and find a room full of snakes. AHHHHHHHH ! ",
        "choices": [
            {"text": "You run as far as you can and leave the ambassy", "next_page": "start"},
            {"text": "You shout strongly to make them leave !", "next_page": "police"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[20])),
    },
    "search_one_side": {
        "text": "You start searching the office doors on one side of the hallway. After meticulously checking a few offices, you finally find the classified folder hidden in a desk drawer. What's your next move?",
        "choices": [
            {"text": "Take the folder and discreetly leave the embassy.", "next_page": "mission_accomplished"},
            {"text": "Double-check the folder for any additional information before leaving.", "next_page": "double_check_folder"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[8])),
    },
    "search_both_sides": {
        "text": "You cautiously search the office doors on both sides of the hallway. After careful inspection, you discover the classified folder neatly tucked away in a filing cabinet. What's your plan?",
        "choices": [
            {"text": "Secure the folder and exit the embassy discreetly.", "next_page": "mission_accomplished"},
            {"text": "Take photos of other relevant documents before leaving.", "next_page": "police"},
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[7])),
    },
    "double_check_folder": {
        "text": "You take a moment to double-check the contents of the folder. Everything seems in order. It's time to make your exit from the embassy.",
        "choices": [
            {"text": "Leave the office and exit the embassy.", "next_page": "mission_accomplished"},
            {"text": "Celebrate the victory.", "next_page": "police"}
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[13])),
    },
    "police": {
        "text": "You made too much noise. The police has arrived and arrested you... They nicely bring you outside of the embassy.",
        "choices": [
            {"text": "Accept and follow them.", "next_page": "start"},
            {"text": "Do not accept and try to run. Maybe it can work ?", "next_page": "start"}
        ],
        "image": html.Img(src='data:image/png;base64,{}'.format(im[21])),
    },
}
story_data["secret_tunnel"] = {
    "text": "While exploring the embassy's basement, you stumble upon a concealed door leading to a secret tunnel. You venture through the tunnel, and to your surprise, it leads directly to the room containing the classified folder. It seems like fate is on your side. What's your next move?",
    "choices": [
        {"text": "Retrieve the folder and exit through the tunnel for a stealthy escape.", "next_page": "mission_accomplished"},
        {"text": "Investigate the tunnel further before retrieving the folder.", "next_page": "investigate_tunnel"},
    ],
    "image": html.Img(src='data:image/png;base64,{}'.format(im[23])),
}

story_data["investigate_tunnel"] = {
    "text": "As you explore the secret tunnel, you come across some interesting clues and hidden caches of information. It's risky, but you could gather valuable intelligence before completing your mission. What will you do?",
    "choices": [
        {"text": "Prioritize the mission; retrieve the folder and exit the tunnel.", "next_page": "mission_accomplished"},
        {"text": "Take some extra time to gather intelligence before leaving.", "next_page": "gather_intelligence"},
    ],
    "image": html.Img(src='data:image/png;base64,{}'.format(im[24])),
}

story_data["gather_intelligence"] = {
    "text": "You invest additional time in collecting intelligence from the hidden caches. It's a gamble, but the information could prove valuable for future operations. Finally, you retrieve the folder and make your way back through the tunnel.",
    "choices": [
        {"text": "Exit the tunnel and complete the mission, carrying both the folder and gathered intelligence.", "next_page": "mission_accomplished_full"},
        {"text": "Celebrate the victory.", "next_page": "police"}
    ],
    "image": html.Img(src='data:image/png;base64,{}'.format(im[25])),
}

app.layout = html.Div([
    
    html.H1(children='Bonjour Markéta',style = {'textAlign': 'center','marginBottom':40,'marginTop':20}),
    html.Div([dcc.Markdown('''
        Vážená Markéto,
        Dobrý špion musí umět proniknout a získat informace. Jelikož by bylo příliš nebezpečné
        vás poslat bez tréninku, provedli jsme simulaci. Vaším cílem je najít tajný spis ukrytý v
        ambasádě, ale možná i víc...
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
        }),dcc.Markdown('Test 4',style={'margin-left':'120px'}),html.Img(src='data:image/png;base64,{}'.format(ndone),style={
            'height': '25px','width': '25px','margin-left':'12px'
        })],style={'display':'flex','flex-direction':'row','marginBottom':20,'marginTop':20}),
    html.Hr(style={'width': '70%','margin':'auto'}),
    html.Div([
    html.Div(id="story-text",style = {'textAlign': 'center','marginBottom':20,'marginTop':20,'font-size':'25px'}),
    html.Div(id='image',style={'display': 'block','margin-left': 450,'margin-right': 'auto','width': '50%','marginBottom':20}),
    html.Div([
        html.Button(id="choice-button-1", n_clicks=0,style={'font-size': '20px','height': '100px', 'width': '380px','marginLeft':310}),
        html.Button(id="choice-button-2", n_clicks=0,style={'font-size': '20px','height': '100px', 'width': '380px','marginLeft':40}),
    ],style={'height':'80%'}),
    dcc.Store(id='memory')
])
])

@app.callback(
    Output("story-text", "children"),
    Output("choice-button-1", "children"),
    Output("choice-button-2", "children"),
    Output("memory",'data'),
    Output('image','children'),
    Input("choice-button-1", "n_clicks"),
    Input("choice-button-2", "n_clicks"),
    State('memory', 'data'),
)
def update_story_page(click_1, click_2,current_page):
    if current_page is None :
        current_page = 'start'
        
    triggered_button = dash.callback_context.triggered[0]["prop_id"].split(".")[0]
    if triggered_button == "choice-button-1":
        next_page = story_data[current_page]["choices"][0]["next_page"]
    elif triggered_button == "choice-button-2":
        next_page = story_data[current_page]["choices"][1]["next_page"]
    else :
        next_page='start'
    page_text = story_data[next_page]["text"]
    choices = story_data[next_page]["choices"]
    image= story_data[next_page]["image"]
        
    return page_text, choices[0]["text"], choices[1]["text"],next_page,image

if __name__ == '__main__':
    app.run(debug=True)