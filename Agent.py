import random


class agent:
    def __init__(self):
        self.action = 0 # 0: left /1: right /2:stop
    def move(self):
        if random.random()<0.5:
            self.action = 1
        else:
            self.action = 0