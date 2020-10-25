
import os
import logging

import tensorflow as tf

from tensorforce.agents import Agent
from tensorforce.environments import Environment
from tensorforce.execution import Runner

from sim import gameSim

class CustomEnvironment(Environment):
    def __init__(self):
        super().__init__()
        self.resourceNum = 1
    
    def states(self):
        return dict(type='float', shape=(10,))

    # Events
    def actions(self):
        return {"1": dict(type="float", min_value=0, max_value=1),
                "2": dict(type="float", min_value=0, max_value=1),
                "3": dict(type="float", min_value=0, max_value=1),
                "4": dict(type="float", min_value=0, max_value=1),
                "5": dict(type="float", min_value=0, max_value=1),
                "6": dict(type="float", min_value=0, max_value=1),
                "7": dict(type="float", min_value=0, max_value=1),
                "8": dict(type="float", min_value=0, max_value=1),
                }

    # Optional, should only be defined if environment has a natural maximum
    # episode length
    def max_episode_timesteps(self):
        return super().max_episode_timesteps()

    # Optional
    def close(self):
        super().close()

    def reset(self):
        gsim = gameSim()
        return gsim.getState()
        
    def execute(self, actions):
        if self.gsim.isHome(self.resourceNum):
            reward = self.gsim.updateGameAction(actions)
        else:
            reward = self.gsim.updateGameNoAction(self.resourceNum)
        terminal = self.gsim.isGameOver()
        if self.resourceNum == 9:
            self.resourceNum = 1
        else:
            self.resourceNum += 1
        return self.gsim.getState(), terminal, reward
