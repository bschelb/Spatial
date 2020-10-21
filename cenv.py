
import os
import logging

import tensorflow as tf

from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner

from sim import gameSim

class CustomEnvironment(Environment):
    gsim = gameSim()
    def __init__(self):
        super().__init__()
    
    def states(self):
        return dict(type='float', shape=(10,))

    def actions(self):
        return {"id_1": dict(type="int", min_value=0, max_value=9),
                 "id_2": dict(type="int", min_value=0, max_value=9),
                 "id_3": dict(type="int", min_value=0, max_value=9),
                 "id_4": dict(type="int", min_value=0, max_value=9),
                 "id_5": dict(type="int", min_value=0, max_value=9),
                 "id_6": dict(type="int", min_value=0, max_value=9),
                 "id_7": dict(type="int", min_value=0, max_value=9),
                 "id_8": dict(type="int", min_value=0, max_value=9),
                 }

    # Optional, should only be defined if environment has a natural maximum
    # episode length
    def max_episode_timesteps(self):
        return super().max_episode_timesteps()

    # Optional
    def close(self):
        super().close()

    def reset(self):
        self.gsim.new_hand()
        return self.gsim.state()

    def execute(self, actions):
        
        return self.gsim.state(), terminal, reward
