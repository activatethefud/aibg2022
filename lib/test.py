import db
import numpy as np
from tensorflow import keras
from serializer import GameState1DSerializer
import sys
import datetime as dt
import numpy as np

gamma = 0.99

def prepare_training_data(from_timestamp = 0):
    
    if(isinstance(from_timestamp, dt.datetime)):
        from_timestamp = int(from_timestamp.timestamp())
        
    replays = db.get_all_experiences({ "time": { "$gt": from_timestamp}})
    
    def _get_score_from_state(state: dict):
        return [player["score"] for player in state["scoreBoard"]["players"] if player["name"] == "JutricKafica"][0]
    
    rewards = [_get_score_from_state(replay["sp"]) - _get_score_from_state(replay["s"]) for replay in replays]

    _seralizer = GameState1DSerializer()

    serialized = [
        _seralizer.serialize_single(x) for x in replays
    ]
    
    rewards = [
        x["r"] for x in replays
    ]

    return serialized, rewards

model = keras.Sequential()
model.add(keras.layers.Input(shape=(3*628,)))
model.add(keras.layers.Dense(128, activation='relu'))
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(1, activation='linear'))

# Compile the model with an optimizer and a loss function
model.compile(optimizer='adam', loss='mean_squared_error')

def create_targets(model, training_data, rewards):
    
    n = len(training_data)
    model_inputs = []
    
    for i in range(2, n):
        model_inputs.append(np.hstack(training_data[i], training_data[i-1], training_data[i-2]))
    
    targets = []
    return model_inputs, targets
    

serialized, rewards = prepare_training_data(dt.datetime.now() - dt.timedelta(minutes = 15))    