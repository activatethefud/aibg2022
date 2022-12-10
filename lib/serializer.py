import numpy as np
import json
import db

class GameState1DSerializer():

    def __init__(self):
        pass

    def serialize_single(self, replay: dict):

        # sledeca linija hvata samo prvi, prepravi da radi sa celom listom

        old_state = replay["s"]
        action = replay["a"]["action"].split(",")

        json_map = old_state
        
        tiles_list = []
        
        for row in json_map['map']['tiles']:
        
            for tile in row:
        
                q = tile['q']
        
                r = tile['r']
        
                if tile['entity']['type'] == 'EMPTY':
        
                    tiles_list.append((q,r,0))
        
                elif tile['entity']['type'] == 'BLACK_HOLE':
        
                    tiles_list.append((q,r,1))
        
                elif tile['entity']['type'] == 'WORM_HOLE':
        
                    tiles_list.append((q,r,2))
        
                elif tile['entity']['type'] == 'HEALTH':
        
                    tiles_list.append((q,r,3))
        
                elif tile['entity']['type'] == 'EXPERIENCE':
        
                    tiles_list.append((q,r,4))
        
                elif tile['entity']['type'] == 'ASTEROID':
        
                    tiles_list.append((q,r,5))
        
                elif tile['entity']['type'] == 'BOSS':
        
                    tiles_list.append((q,r,6))
        

        
        for p in json_map['scoreBoard']['players']:
        
            q,r = p['q'],p['r']
        
            if p['name']!='JutricKafica':
        
                ind = tiles_list.index((q,r,0))
        
                if ind != -1:
        
                    tiles_list[ind] = (q,r,7)
        
                else:
        
                    ind = tiles_list.index((q,r,1))
        
                    if ind != -1:
        
                        tiles_list[ind] = (q,r,7)
        
                res = np.array(tiles_list)
        
        return res[:,2]

    def serialize_action(self, data: dict):
        action = data["action"].split(",")
        return [0 if action[0] == "attacK" else 1, action[1], action[2]]

    def serialize_multiple(self, states: list):
        pass



r = GameState1DSerializer().serialize_single(db.get_one_experience())