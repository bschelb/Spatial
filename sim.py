# import tensorflow
# import tensorforce
# from tensorforce.agents import PPOAgent, DQNAgent
from big_map import getOpenSpaces
from bfs import getPath
import operator
# import numpy as np
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
        # Resources
        # [[Coordinates], [Speed], [ID], [Destination Event], Checked]
        self.resourceID_a = [[self.homeBase], [10], [1], [0], False]
        self.resourceID_b = [[self.homeBase], [10], [2], [0], False]
        self.resourceID_c = [[self.homeBase], [15], [3], [0], False]
        self.resourceID_d = [[self.homeBase], [10], [4], [0], False]
        self.resourceID_e = [[self.homeBase], [5], [5], [0], False]
        self.resourceID_f = [[self.homeBase], [20], [6], [0], False]
        self.resourceID_g = [[self.homeBase], [15], [7], [0], False]
        self.resourceID_h = [[self.homeBase], [15], [8], [0], False]
        self.resourceID_i = [[self.homeBase], [10], [9], [0], False]
        # Events
        # [[Coordinates], [Required Resources], [Time Start & Finish], Active, [ID]]
        self.eventID_a = [eventCoordinates[0], [1], [1, 411], True, [1]]
        self.eventID_b = [eventCoordinates[1], [2, 6, 9], [41, 441], False, [2]]
        self.eventID_c = [eventCoordinates[2], [3], [126, 526], False, [3]]
        self.eventID_d = [eventCoordinates[3], [6], [156, 556], False, [4]]
        self.eventID_e = [eventCoordinates[4], [9], [226, 626], False, [5]]
        self.eventID_f = [eventCoordinates[5], [5, 1, 4, 7], [256, 656], False, [6]]
        self.eventID_g = [eventCoordinates[6], [1, 4, 7, 2], [329, 729], False, [7]]
        self.eventID_h = [eventCoordinates[7], [1, 4, 7, 6], [359, 759], False, [8]]

    def getState(self, resource):
        state = []
        if self.eventID_a[3] == True:
            state.append(self.getDistanceToEvent(resource, self.eventID_a)[1])
        elif all([x == True for x in self.eventID_a[1]]):
            state.append(-2)
        else:
            state.append(-1)

        if self.eventID_b[3] == True:
            state.append(self.getDistanceToEvent(resource, self.eventID_b)[1])
        elif all([x == True for x in self.eventID_b[1]]):
            state.append(-2)
        else:
            state.append(-1)

        if self.eventID_c[3] == True:
            state.append(self.getDistanceToEvent(resource, self.eventID_c)[1])
        elif all([x == True for x in self.eventID_c[1]]):
            state.append(-2)
        else:
            state.append(-1)

        if self.eventID_d[3] == True:
            state.append(self.getDistanceToEvent(resource, self.eventID_d)[1])
        elif all([x == True for x in self.eventID_d[1]]):
            state.append(-2)
        else:
            state.append(-1)

        if self.eventID_e[3] == True:
            state.append(self.getDistanceToEvent(resource, self.eventID_e)[1])
        elif all([x == True for x in self.eventID_e[1]]):
            state.append(-2)
        else:
            state.append(-1)

        if self.eventID_f[3] == True:
            state.append(self.getDistanceToEvent(resource, self.eventID_f)[1])
        elif all([x == True for x in self.eventID_f[1]]):
            state.append(-2)
        else:
            state.append(-1)

        if self.eventID_g[3] == True:
            state.append(self.getDistanceToEvent(resource, self.eventID_g)[1])
        elif all([x == True for x in self.eventID_g[1]]):
            state.append(-2)
        else:
            state.append(-1)

        if self.eventID_h[3] == True:
            state.append(self.getDistanceToEvent(resource, self.eventID_h)[1])
        elif all([x == True for x in self.eventID_h[1]]):
            state.append(-2)
        else:
            state.append(-1)
        
        return state

    def updateEventsActivity(self):
        if self.eventID_a[2][1] < self.time:
            self.eventID_a[3] = False

        if self.eventID_b[2][0] < self.time:
            if all([x == True for x in self.eventID_b[1]]):
                self.eventID_b[3] = False
            else:
                self.eventID_b[3] = True
                new = True
        elif self.eventID_b[2][1] < self.time:
            self.eventID_b[3] = False
        
        if self.eventID_c[2][0] < self.time:
            if all([x == True for x in self.eventID_c[1]]):
                self.eventID_c[3] = False
            else:
                self.eventID_c[3] = True
                new = True
        elif self.eventID_c[2][1] < self.time:
            self.eventID_c[3] = False
        
        if self.eventID_d[2][0] < self.time:
            if all([x == True for x in self.eventID_d[1]]):
                self.eventID_d[3] = False
            else:
                self.eventID_d[3] = True
                new = True
        elif self.eventID_d[2][1] < self.time:
            self.eventID_d[3] = False
        
        if self.eventID_e[2][0] < self.time:
            if all([x == True for x in self.eventID_e[1]]):
                self.eventID_e[3] = False
            else:
                self.eventID_e[3] = True
                new = True
        elif self.eventID_e[2][1] < self.time:
            self.eventID_e[3] = False
        
        if self.eventID_f[2][0] < self.time:
            if all([x == True for x in self.eventID_f[1]]):
                self.eventID_f[3] = False
            else:
                self.eventID_f[3] = True
                new = True
        elif self.eventID_f[2][1] < self.time:
            self.eventID_f[3] = False
        
        if self.eventID_g[2][0] < self.time:
            if all([x == True for x in self.eventID_g[1]]):
                self.eventID_g[3] = False
            else:
                self.eventID_g[3] = True
                new = True
        elif self.eventID_g[2][1] < self.time:
            self.eventID_g[3] = False
        
        if self.eventID_h[2][0] < self.time:
            if all([x == True for x in self.eventID_h[1]]):
                self.eventID_h[3] = False
            else:
                self.eventID_h[3] = True
                new = True
        elif self.eventID_h[2][1] < self.time:
            self.eventID_h[3] = False
        return new

    def getDistanceToEvent(self, resource, event):
        self.path = self.getPathList(resource, event)
        distance = len(self.path)
        if resource[2] in event[1]:
            self.reward += 1
        if distance == 1 and all([x == True for x in event[1]]):
            None
        elif (distance == 1):
            for requirement in event[1]:
                if requirement == resource[2]:
                    requirement = True
            self.goToHomeBase(resource)
            resource[3] == 0
        return self.path, distance

    def goToHomeBase(self, resource):
        self.path = self.getPathList(resource, self.homeBase)
        return self.path

    def moveResource(self, resource):
        self.path.pop(0)
        resource[0] = self.path[0]

    def getPathList(self, resource, event):
        self.path = getPath(resource[0], event[0], resource[1])
        return self.path

    def isHome(self, resource):
        if resource == 1:
            resource = self.resourceID_a
        elif resource == 2:
            resource = self.resourceID_b
        elif resource == 3:
            resource = self.resourceID_c
        elif resource == 4:
            resource = self.resourceID_d
        elif resource == 5:
            resource = self.resourceID_e
        elif resource == 6:
            resource = self.resourceID_f
        elif resource == 7:
            resource = self.resourceID_g
        elif resource == 8:
            resource = self.resourceID_h
        else:
            resource = self.resourceID_i
        if resource[0] == self.homeBase and self.updateEventsActivity():
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

    def updateGameAction(self, action, resource):
        self.updateEventsActivity()
        if resource == 1:
            resource = self.resourceID_a
            resource[4] = True
        elif resource == 2:
            resource = self.resourceID_b
            resource[4] = True
        elif resource == 3:
            resource = self.resourceID_c
            resource[4] = True
        elif resource == 4:
            resource = self.resourceID_d
            resource[4] = True
        elif resource == 5:
            resource = self.resourceID_e
            resource[4] = True
        elif resource == 6:
            resource = self.resourceID_f
            resource[4] = True
        elif resource == 7:
            resource = self.resourceID_g
            resource[4] = True
        elif resource == 8:
            resource = self.resourceID_h
            resource[4] = True
        else:
            resource = self.resourceID_i
            resource[4] = True
        max_value = max(action.items(), key=operator.itemgetter(1))[1]
        for item in action.items():
            if item[1] == max_value:
                event = item[0]
        resource[3] = event
        if event == 1:
            event = self.eventID_a
        elif event == 2:
            event = self.eventID_b
        elif event == 3:
            event = self.eventID_c
        elif event == 4:
            event = self.eventID_d
        elif event == 5:
            event = self.eventID_e
        elif event == 6:
            event = self.eventID_f
        elif event == 7:
            event = self.eventID_g
        else:
            event = self.eventID_h
        self.getDistanceToEvent(resource, event)
        self.moveResource(resource)
        self.timeLapse()
        return self.reward
    
    def updateGameNoAction(self, resource):
        self.updateEventsActivity()
        if resource == 1:
            resource = self.resourceID_a
        elif resource == 2:
            resource = self.resourceID_b
        elif resource == 3:
            resource = self.resourceID_c
        elif resource == 4:
            resource = self.resourceID_d
        elif resource == 5:
            resource = self.resourceID_e
        elif resource == 6:
            resource = self.resourceID_f
        elif resource == 7:
            resource = self.resourceID_g
        elif resource == 8:
            resource = self.resourceID_h
        else:
            resource = self.resourceID_i
        if resource[3] == 0:
            self.goToHomeBase(resource)
            self.moveResource(resource)
            self.timeLapse()
            noGoEvent = True
        elif resource[3] == 1:
            event = self.eventID_a
        elif resource[3] == 2:
            event = self.eventID_b
        elif resource[3] == 3:
            event = self.eventID_c
        elif resource[3] == 4:
            event = self.eventID_d
        elif resource[3] == 5:
            event = self.eventID_e
        elif resource[3] == 6:
            event = self.eventID_f
        elif resource[3] == 7:
            event = self.eventID_g
        else:
            event = self.eventID_h
        if noGoEvent == False:
            self.getDistanceToEvent(resource, event)
            self.moveResource(resource)
            self.timeLapse()




        

a = gameSim()
a.getState(a)