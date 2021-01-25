import pygame
import os
from unit_class import *
from newton_class import *
class Tear:
    def __init__(self, pos, attack, img, direction):

        self.x = pos[0]
        self.y = pos[1]
        self.speed = 5
        self.dmg = attack
        self.direction = direction
        self.img = img

    def draw_tear(self):
        screen.blit(self.img, (self.x, self.y))


    def shoot(self):
        if 0 < self.x < board_size[0] and 0 < self.y < board_size[1]:
            self.x += self.direction[0]
            self.y += self.direction[1]

    def hit_wall(self):
        if 0 < self.x < board_size[0] and 0 < self.y < board_size[1]:
            return False
        return True

    def collision(self, board):
        for mob in board.mob:
            if 0 < self.x + 10 - mob.x < 63 and 0 < self.y + 10 - mob.y < 63:
                mob.hp -= self.dmg
                if mob.hp <= 0:
                    mob.alive = False
                return True
        return False








