import pygame
from random import *
from consts import *

class Timer:
    def __init__(self):
        self.tick = 1
        self.sec = 0
        self.immune = 0


    def progress(self):
        self.tick += 1
        if self.immune > 0:
            self.immune -= 1
        if self.tick % 60 == 0:
            self.sec += 1



    def immunity(self):
        self.immune = 120

    def if_immune(self):
        return self.immune > 0




