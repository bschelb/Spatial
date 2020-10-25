import tensorflow
import tensorforce
from tensorforce.agents import PPOAgent, DQNAgent
from big_map import getOpenSpaces
from bfs import getPath
import operator
import numpy as np
import random

class gameSim():

    def __init__(self):
        availableCoordinates = getOpenSpaces()
        eventCoordinates = random.sample(availableCoordinates, 8)
        self.homeBase = [66, 124]
        self.time = 0
        self.reward = 0
        self.path = []
        self.eventActives = []
        self.gameState = {
            "Resources": {
                "resourceID_a": {
                    "Location": self.homeBase,
                    "Speed": 10,
                    "ID": 1,
                    "Destination": 0,
                    "Checked": False,
                },
                "resourceID_b": {
                    "Location": self.homeBase,
                    "Speed": 10,
                    "ID": 2,
                    "Destination": 0,
                    "Checked": False,
                },
                "resourceID_c": {
                    "Location": self.homeBase,
                    "Speed": 15,
                    "ID": 3,
                    "Destination": 0,
                    "Checked": False,
                },
                "resourceID_d": {
                    "Location": self.homeBase,
                    "Speed": 10,
                    "ID": 4,
                    "Destination": 0,
                    "Checked": False,
                },
                "resourceID_e": {
                    "Location": self.homeBase,
                    "Speed": 5,
                    "ID": 5,
                    "Destination": 0,
                    "Checked": False,
                },
                "resourceID_f": {
                    "Location": self.homeBase,
                    "Speed": 20,
                    "ID": 6,
                    "Destination": 0,
                    "Checked": False,
                },
                "resourceID_g": {
                    "Location": self.homeBase,
                    "Speed": 15,
                    "ID": 7,
                    "Destination": 0,
                    "Checked": False,
                },
                "resourceID_h": {
                    "Location": self.homeBase,
                    "Speed": 15,
                    "ID": 8,
                    "Destination": 0,
                    "Checked": False,
                },
                "resourceID_i": {
                    "Location": self.homeBase,
                    "Speed": 10,
                    "ID": 9,
                    "Destination": 0,
                    "Checked": False,
                }
            },
            "Events": {
                "eventID_a": {
                    "Location": eventCoordinates[0],
                    "Ordered": False,
                    "Resources": [1],
                    "Start": 1,
                    "Finish": 411,
                    "Active": True,
                    "ID": 1,
                },
                "eventID_b": {
                    "Location": eventCoordinates[1],
                    "Ordered": True,
                    "Resources": [2,6,9],
                    "Start": 41,
                    "Finish": 441,
                    "Active": False,
                    "ID": 2,
                },
                "eventID_c": {
                    "Location": eventCoordinates[2],
                    "Ordered": False,
                    "Resources": [3],
                    "Start": 126,
                    "Finish": 526,
                    "Active": False,
                    "ID": 3,
                },
                "eventID_d": {
                    "Location": eventCoordinates[3],
                    "Ordered": False,
                    "Resources": [6],
                    "Start": 156,
                    "Finish": 556,
                    "Active": False,
                    "ID": 4,
                },
                "eventID_e": {
                    "Location": eventCoordinates[4],
                    "Ordered": False,
                    "Resources": [9],
                    "Start": 226,
                    "Finish": 626,
                    "Active": False,
                    "ID": 5,
                },
                "eventID_f": {
                    "Location": eventCoordinates[5],
                    "Ordered": False,
                    "Resources": [5, 1, 4, 7],
                    "Start": 256,
                    "Finish": 656,
                    "Active": False,
                    "ID": 6,
                },
                "eventID_g": {
                    "Location": eventCoordinates[6],
                    "Ordered": False,
                    "Resources": [1, 4, 7, 2],
                    "Start": 329,
                    "Finish": 729,
                    "Active": False,
                    "ID": 7,
                },
                "eventID_h": {
                    "Location": eventCoordinates[7],
                    "Ordered": False,
                    "Resources": [5, 1, 4, 7],
                    "Start": 359,
                    "Finish": 759,
                    "Active": False,
                    "ID": 8,
                },
            }
        }

    def getState(self, resource):
        state = []
        for key in self.gameState["Resources"]:
            if self.gameState["Resources"][key]["ID"] == resource:
                resource = key
        for key in self.gameState["Events"]:
            if self.gameState["Events"][key]["Active"] == True:
                state.append(self.getDistanceToEvent(resource, key)[1])
            elif all([x == True for x in self.gameState["Events"][key]["Resources"]]):
                state.append(-2)
            else:
                state.append(-1)
        return state

    def updateEventsActivity(self):
        newEvent = False
        for key in self.gameState["Events"]:
            if self.gameState["Events"][key]["Start"] < self.time:
                self.gameState["Events"][key]["Active"] = True
                newEvent = True
            
            if all([x == True for x in self.gameState["Events"][key]["Resources"]]):
                self.gameState["Events"][key]["Active"] = False
            elif self.gameState["Events"][key]["Resources"] < self.time:
                self.gameState["Events"][key]["Active"] = False
        return newEvent

    def getDistanceToEvent(self, resource, event):
        self.getPathList(resource, event)
        distance = len(self.path)
        if self.gameState["Resources"][resource]["Destination"] in self.gameState["Events"][event]["Resources"]:
            self.reward += 1
        if distance == 1 and all([x == True for x in self.gameState["Events"][event]["Resources"]]):
            None
        elif (distance == 1) and (self.gameState["Resources"][resource]["Destination"] != 10):
            for requirement in self.gameState["Events"][event]["Resources"]:
                if requirement == self.gameState["Resources"][resource]["ID"]:
                    requirement = True
            self.goToHomeBase(resource)
            self.gameState["Resources"][resource]["Destination"] = 10
        elif distance == 1 and self.gameState["Resources"][resource]["Destination"] != 10:
            None
        self.gameState["Resources"][resource]["Destination"] = self.gameState["Events"][event]["ID"]
        self.gameState["Resources"][resource]["Checked"] = True
        return self.path, distance

    def goToHomeBase(self, resource):
        self.getPathList(resource, self.homeBase)

    def moveResource(self, resource):
        if self.getDistance(resource) >= 2:
            self.path.pop(0)
            self.gameState["Resources"][resource]["Location"] = self.path[0]
        else:
            None

    def getPathList(self, resource, event):
        print(resource)
        self.path = getPath(self.gameState["Resources"][resource]["Location"], 
                            self.gameState["Events"][event]["Location"], 
                            self.gameState["Resources"][resource]["Speed"])

    def getDistance(self, resource):
        destination = None
        for key in self.gameState["Events"]:
            if self.gameState["Resources"][resource]["Destination"] == self.gameState["Events"][key]["ID"]:
                destination = self.gameState["Events"][key]["Location"]
            else:
                destination = self.homeBase
        distance = getPath(self.gameState["Resources"][resource]["Location"], 
                            destination, 
                            self.gameState["Resources"][resource]["Speed"])
        distance = len(distance)
        return distance

    def isHome(self, resource):
        for key in self.gameState["Resources"]:
            if self.gameState["Resources"][key]["ID"] == resource:
                resource = key
        if self.gameState["Resources"][resource]["Destination"] == 10:
            if self.getDistanceHome(resource) == 1:
                return True
        if self.gameState["Resources"][resource]["Location"] == self.homeBase and self.updateEventsActivity():
            return True
        else:
            return False
    
    def isGameOver(self):
        if self.time >= 760:
            return True
        else:
            return False

    def timeLapse(self):
        self.time += 5

    def resetReward(self):
        self.reward = 0

    def updateGameAction(self, action, resource):
        self.updateEventsActivity()
        for key in self.gameState["Resources"]:
            if self.gameState["Resources"][key]["ID"] == resource:
                resource = key
        self.gameState["Resources"][resource]["Checked"] = True
        max_value = max(action.items(), key=operator.itemgetter(1))[1]
        event = None
        for item in action.items():
            if item[1] == max_value:
                event = item[0]
        for key in self.gameState["Events"]:
            if self.gameState["Events"][key]["ID"] == event:
                event = key
        self.gameState["Resources"][resource]["Destination"] = self.gameState["Events"][event]["ID"]
        self.getDistanceToEvent(resource, event)
        self.moveResource(resource)
        self.timeLapse()
        return self.reward
    
    def updateGameNoAction(self, resource):
        self.updateEventsActivity()
        event = None
        for key in self.gameState["Resources"]:
            if self.gameState["Resources"][key]["ID"] == resource:
                resource = key
        for key in self.gameState["Events"]:
            if self.gameState["Events"][key]["ID"] == self.gameState["Resoruces"][resource]["Destination"]:
                event = key
        if self.gameState["Resources"][resource]["Destination"] == 10:
            self.goToHomeBase(resource)
            self.moveResource(resource)
            self.timeLapse()
        else:
            self.getDistanceToEvent(resource, event)
            self.moveResource(resource)
            self.timeLapse()
        self.resetReward()
        return self.reward