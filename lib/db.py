import pymongo
import datetime
import sys 

client = pymongo.MongoClient("mongodb://aibg:aibgmatf@fossmatrix.ml:27017/aibg2022")
aibg_db = client.get_database("aibg2022")
replay_buffer_collection = aibg_db.get_collection("replay_buffer1")

try:
    print(client.server_info())
except:
    raise Exception("Error with database connection.")

def get_one_experience(query = {}):
    return replay_buffer_collection.find_one(query)

def get_all_experiences(query = {}):
    return list(replay_buffer_collection.find(query))

def add_experience(agent_id: str, old_state: dict, action: dict, new_state: dict, reward: float):

    try:
        replay_buffer_collection.insert_one({
            "time": int(datetime.datetime.now().timestamp()),
            "agent_id": agent_id,
            "s": old_state,
            "a": action,
            "sp": new_state,
            "r": reward
        })
    except Exception as e:
        print(f'db exception: {e}', file = sys.stderr)
        return False
    
    return True