import pygame
from random import *
from consts import *
class Unit:
    def __init__(self, hp, pos, attack, img, name):
        self.alive = True
        self.maxhp = hp
        self.hp = hp
        self.x = pos[0]
        self.y = pos[1]
        self.attack = attack
        self.img = img
        self.name = name
        self.tick = 0

    def unit_pos(self):
        return [self.x, self.y]

    def unit_attack(self):
        return self.attack

    def unit_move(self, v):
        if self.x + v[0] > board_size[0] - 52:
            self.x = board_size[0] - 52
        elif self.x + v[0] < 0:
            self.x = 0
        else: self.x += v[0]
        if self.y + v[1] > board_size[1] - 80:
            self.y = board_size[1] - 80
        elif self.y + v[1] < 80:
            self.y = 80
        else: self.y += v[1]

    def unit_heal(self, h):
        if self.hp + h >  self.maxhp:
            self.hp = self.maxhp
        else:
            self.hp += h

    def unit_hurt(self, h):
        self.hp -= h
        if self.hp <= 0:
            self.alive = False

    def draw_unit(self):
        screen.blit(self.img, (self.x, self.y))


