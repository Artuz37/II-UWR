import pygame
from consts import *
from unit_class import *


class Slowmob(Unit):
    def chase(self, newton):
        self.unit_move(vector(self.x - newton.x, self.y - newton.y, 4))

    def hit(self, newton):
        return -63 < self.x - newton.x < 52 and -63 < self.y - newton.y < 80





