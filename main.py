import os, sys
import random, time
random.seed(time.time())
from core.Characters import *

class Engine():
    def __init__(self, *robots):
        super().__init__()
        self.robots=[bot for bot in robots if (isinstance(bot, Robot) or issubclass(bot, Robot))]
        self.selected=self.robots[0]
    
    def run(self):
        while True:
            try:
                self.selected.parser(input('>> '))
            except Exception as e:
                print(e)

Game=Engine(Robot(4,5))
Game.run()