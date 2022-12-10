import requests
import time
import json
import datetime as dt
import threading
import config
import random

SERVER_IP = 'aibg2022.com'
CONNECTION_JSON = {
    'username': 'JutricKafica',
    'password': 'q8K^Hx9%L6'
}

SECOND = 1

mapNames = ['test1.txt', 'test2.txt']
playerIdxs = [1, 2, 3, 4]
matchTime = 2

def craft_aibg_url(url, port):
    return f'http://{SERVER_IP}:{port}/{url}'

def get_token():
    r = requests.post(craft_aibg_url('user/login', config.PORT), json=CONNECTION_JSON)
    return r.json()['token']

TOKEN = get_token()

def create_game(token):
    header = {
        'Authorization': f'Bearer {token}',
    }
    body = {
        'mapName': f'{random.choice(mapNames)}',
        'playerIdx': f'{random.choice(playerIdxs)}',
        'time': f'{matchTime}'
    }
    # print(body)
    r = requests.post(craft_aibg_url('game/train', config.PORT), headers=header, json=body)
    # print(f'body {body}')

    if(r.status_code in [200, 202]):
        print(f"response: {r.text[:150]}")
        json.dump(json.loads(json.loads(r.content)["gameState"]),open("../initial_state.json",'w'))
        # json.dump(json.loads(r.content),open("../initial_state.json",'w'))

        

        return True
    
    return False

def keep_creating_games():

    print("Starting game creation thread...")

    while True:
        if(create_game(TOKEN)):
            print(f"[{dt.datetime.now()}] Game created")
        time.sleep(5*SECOND)

game_creation_thread = threading.Thread(
    None,
    keep_creating_games
)

game_creation_thread.setDaemon(True)

game_creation_thread.start()