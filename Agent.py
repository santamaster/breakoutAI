import random
import torch

class agent:
    def __init__(self):
        self.action = 0 # 0: left /1: right /2:stop
    def policy(self,status):
        i = random.random()
        if i<0.33:
            self.action = 1
        elif 0.33<i<0.66:
            self.action = 0
        else:
            self.action = 2
    def training(self,status,reward):
        #get status reward and self.action
        #TODO:training 
        pass
