import random
import agent_wrapper
from typing import Tuple, Any
import numpy as np

# gets out position from state
def get_my_position(state) -> Tuple[int, int]:
    try:
        players = state["scoreBoard"]["players"]
    except:
        print("BAD STATE IN get_my_position()", str(state))
    myself = [player for player in players if player["name"] == "JutricKafica"][0]

    r = myself['r']
    q = myself['q']

    return (q, r)

# Picks a random action fot the given state.
# Can try moving or attacking an invalid target in range,
# including (0, 0) ie itself.
def pick_rand_action(state) -> Tuple[str, int, int]:
    q, r = get_my_position(state)

    action_list = ['move', 'attack']
    action = random.choice(action_list)
    
    if action == 'move':
        dr_list = [-1, 0, 1]
        dq_list = [-1, 0, 1]
    else:
        dr_list = [-3, -2, -1, 0, 1, 2, 3]
        dq_list = [-3, -2, -1, 0, 1, 2, 3]

    dr = random.choice(dr_list)
    dq = random.choice(dq_list)

    q += dq
    r += dr

    return (action, q, r)

# checks if the position is out of bounds for the map
def is_valid_coords(pos) -> bool:
    q, r = pos[0], pos[1]
    if q < -14 or q > 14:
        return False
    if r < -14 or r > 14:
        return False
    if q + r < -14 or q + r > 14:
        return False
    return True

def validateMapForValidXTileFunctions(map):
    # print(f"validate map = {str(map)[:150]}")

    for i in range(3):
        if isinstance(map, list):
            if isinstance(map[0], list):
                l = []
                for el in map:
                    l += el
                map = l
        else: 
            map = map['tiles']
    
    # print(f"after validate map = {str(map)[:150]}")

    return map

# checks if it is legal to move to position pos
# does NOT check if the player is next to the pos 
def is_valid_move_tile(pos, map) -> bool:
    q, r = pos[0], pos[1]

    if not is_valid_coords(pos):
        return False

    map = validateMapForValidXTileFunctions(map)

    for tile in map:
        if int(tile['q']) == q and int(tile['r']) == r:
            return tile["tileType"] == "NORMAL"

# checks if the tile contains a player
def is_player_on_tile(state, q: int, r: int) -> bool:
    players = state['scoreBoard']['players']
    players = list([player for player in players])

    for player in players:
        pq = player['q']
        pr = player['r']

        if pq == q and pr == r:
            return True
    
    return False

# checks if it is legal to attack position pos
# does NOT check if the player is within 3 tiles of pos 
def is_valid_attack_tile(pos, state) -> bool:
    map = state['map']
    q, r = pos[0], pos[1]

    if not is_valid_coords(pos):
        return False

    mapList = validateMapForValidXTileFunctions(map)

    for tile in mapList:
        #print(f'tile: {tile} \n---------------------\n')
        # print(f'tile = {tile}')
        qq = tile['q']
        #print(f"qq = {qq}")
        # if isinstance(qq, str):
        #     qq = json.load(qq)

        rr = tile['r']
        # if isinstance(qq, str):
        #     rr = json.load(rr)
        
        if int(qq) == q and int(qq) == r:
            typ = tile["entity"]['type']
            return typ == "BOSS" or typ == "ASTEROID" or is_player_on_tile(state, q, r)

"""
# checks if there is an object blocking out attack
# (q,  r) is out position
# (tq, tr) is the position of our target
def exists_blocking_object(q: int, r: int, tq: int, tr: int) -> bool:

    return False
"""

# checks if the given action is legal for the given state
def is_valid_action(action: str, new_q: int, new_r: int, state) -> bool:
    q, r = get_my_position(state)

    # TODO check if the attack hits an obsticle before target

    if action == 'move':
        if abs(q - new_q) > 1 or abs(r - new_r) > 1 or (new_q == 0 and new_r == 0):
            print("This is a fuckup in a PICK ACTION function, for MOVE action")
            return False
        
        map = state['map']
        map = validateMapForValidXTileFunctions(map)

        return is_valid_move_tile((new_q, new_r), map)
    elif action == 'attack':
        if abs(q - new_q) > 3 or abs(r - new_r) > 3 or (new_q == 0 and new_r == 0):
            print("This is a fuckup in a PICK ACTION function, for ATTACK action")
            return False
        return is_valid_attack_tile((new_q, new_r), state)
    else:
        print(f"This is a fuckup in a PICK ACTION function, invalid action: {action}")
        return False

def pick_random_valid_action(state) -> Tuple[str, int, int]:
    action, q, r = pick_rand_action(state)

    counter = 0
    while not is_valid_action(action, q, r, state):
        action, q, r = pick_rand_action(state)
        if counter > 10 and counter % 10 == 0:
            print(f'counter = {counter}')

    return (action, q, r)

# calls the agent_wrapper function to send the execute the given action
# returns new state and a bool (True -> resp code 200 or 202, otherwise False)
def do_action(agentID: str, oldState, action: str, x: int, y: int) -> Tuple[Any, Any]:
    state, isGoodResp = None, None
    if action == 'move':
        state, isGoodResp = agent_wrapper.move(agentID, oldState,  x, y)
    else:
        state, isGoodResp = agent_wrapper.attack(agentID, oldState, x, y)

    return (state, isGoodResp)

# TODO check for bugs
# TODO HAVE CODE TO CHECK FOR BUGS WHEN RUNNING MATCHES

# -------------------------------------------------------------------------------------
# EXAMPLE OF USE

# Example of any move
# action, q, r = pick_rand_action(state)
# doAction(action, q, r)

# Example of legal only move
# action, q, r = pick_random_valid_action(state)
# doAction(action, q, r)
# -------------------------------------------------------------------------------------