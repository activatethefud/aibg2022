import requests as req
import json
import db

SERVER_IP = 'aibg2022.com'
CONNECTION_JSON = {
    'username': 'JutricKafica',
    'password': 'q8K^Hx9%L6'
}

ACTION_URL = "game/actionTrain"

def real():
    ACTION_URL = "game/doAction"

def craft_aibg_url(url, port):
    return f'http://{SERVER_IP}:{port}/{url}'

def get_token():
    r = req.post(craft_aibg_url('user/login', 8081), json=CONNECTION_JSON)
    return r.json()['token']

TOKEN = get_token()
HEADERS = {
        'Authorization': f'Bearer {TOKEN}',
}

def action(player_id: int, agent_id: str, old_state: dict, data: dict):
    resp = req.post(craft_aibg_url(ACTION_URL, 8081), headers=HEADERS, json=data)


    if(resp.status_code in [200, 202]):

        try:
            new_state = json.loads(resp.content)
            gameState = json.loads(new_state["gameState"])
            players = gameState["scoreBoard"]["players"]

            def _myself_score(state: dict):
                myself = [player for player in players if player["name"] == "JutricKafica"][0]
                return myself["score"]
        

            reward = _myself_score(new_state) - _myself_score(old_state)
        except:
            reward = 0

        return db.add_experience(
            agent_id,
            old_state,
            data,
            new_state,
            reward
        )
    
    else:
        return resp



def move(player_id:int, agent_id: str, old_state: dict, x: int, y: int):
    return action(player_id, agent_id, old_state, {
        "action": f"move,{x},{y}"
    })

def attack(player_id: int, agent_id: str, old_state: dict, x: int, y: int):
    return action(player_id, agent_id, old_state, {
        "attack": f"attack,{x},{y}"
    })

#move(1, "test_agent", {"gameState": {"scoreBoard": {"players":[{"name":"JutricKafica","score":0}]}}}, -5,-7)