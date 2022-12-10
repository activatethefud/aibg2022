import db
import numpy as np
from tensorflow import keras
from serializer import GameState1DSerializer
import sys
import datetime as dt

gamma = 0.99

def prepare_training_data(from_timestamp = int(dt.datetime.now().timestamp())):

    _seralizer = GameState1DSerializer()
    replays = db.get_all_experiences()

    serialized = [
        _seralizer.serialize_single(x) for x in replays
    ]

    return serialized


r = prepare_training_data(0)
# Define the model architecture
model = keras.Sequential()
model.add(keras.layers.Input(shape=(3*628,)))
model.add(keras.layers.Dense(128, activation='relu'))
model.add(keras.layers.Dense(64, activation='relu'))
model.add(keras.layers.Dense(1, activation='linear'))

# Compile the model with an optimizer and a loss function
model.compile(optimizer='adam', loss='mean_squared_error')

# Generate some synthetic data to train the model
state = np.random.rand(628)
target = np.random.rand()

# Train the model
model.fit(state, target)