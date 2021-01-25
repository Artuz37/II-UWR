import pygame
from random import *
from consts import *
from unit_class import *


class Newton(Unit):
    def show_hp(self):
        pos = [0, 0]
        for i in range (1, self.maxhp + 1):
            if self.hp >= i:
                screen.blit(heart_img, pos)
            else:
                screen.blit(empty_heart_img, pos)
            pos[0] += 85
