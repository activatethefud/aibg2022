import pymongo
import json

client = pymongo.MongoClient("mongodb://aibg:aibgmatf@fossmatrix.ml:27017/aibg2022")
aibg_db = client.get_database("aibg2022")
replay_buffer_collection = aibg_db.get_collection("replay_buffer")

try:
    print(client.server_info())
except:
    raise Exception("Error with database connection.")

def get_all_experiences():
    return list(replay_buffer_collection.find())

def add_experience(agent_id: str, old_state: dict, action: dict, new_state: dict, reward: float):

    try:
        replay_buffer_collection.insert_one({
            "agent_id": agent_id,
            "s": old_state,
            "a": action,
            "sp": new_state,
            "r": reward
        })
    except:
        return False
    
    return True