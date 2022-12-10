import requests
import time
import json
import datetime as dt
import threading

SERVER_IP = 'aibg2022.com'
CONNECTION_JSON = {
    'username': 'JutricKafica',
    'password': 'q8K^Hx9%L6'
}

SECOND = 1

def craft_aibg_url(url, port):
    return f'http://{SERVER_IP}:{port}/{url}'

def get_token():
    r = requests.post(craft_aibg_url('user/login', 8081), json=CONNECTION_JSON)
    return r.json()['token']

TOKEN = get_token()

def create_game(token):
    header = {
        'Authorization': f'Bearer {token}',
    }
    body = {
        'mapName': 'test1.txt',
        'playerIdx': '1',
        'time': '1'
    }
    r = requests.post(craft_aibg_url('game/train', 8081), headers=header, json=body)

    if(r.status_code in [200, 202]):
        json.dump(json.loads(r.content),open("../initial_state.json",'w'))
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

game_creation_thread.start()