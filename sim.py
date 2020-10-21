import tensorflow
import tensorforce
from tensorforce.agents import PPOAgent, DQNAgent
import numpy as np

class gameSim():
    
    def __init__(self):
        self.eventID_a = [1]
        self.eventID_b = [2, 6, 9]
        self.eventID_c = [3]
        self.eventID_d = [6]
        self.eventID_e = [9]
        self.eventID_f = [5, 1, 4, 7]
        self.eventID_g = [1, 4, 7, 2]
        self.eventID_h = [1, 4, 7, 6]