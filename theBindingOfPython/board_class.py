import pygame
from random import *
from consts import *
from redtear_class import *
from tear_class import *
from unit_class import *
from newton_class import *
from slowmob_class import *
from timer_class import *


class Board:
    def __init__(self):
        self.lose = False
        self.newton = self.gen_newton()
        self.redtear = []
        self.tear = []
        self.mob = []

    def gen_tear(self, direction):
        self.tear.append(Tear(self.newton.unit_pos(), self.newton.unit_attack(), tear_img, direction))

    def gen_redtear(self, mob, newton):
        self.redtear.append(Redtear(mob.unit_pos(), 1, redtear_img, vector(mob.x - newton.x - 30, mob.y - newton.y - 40, 21)))


    def gen_mob(self, time):
        self.mob.append(Slowmob(10 + time // 600, [randint(0,700), randint(0, 500)], 1, slowmob_img, 'kolejak'))

    def gen_newton(self):
        return Newton(5, [400, 400], 1, newton_img, '')

    def draw_board(self):
        screen.blit(board_img, (0,0))
        self.newton.draw_unit()
        self.newton.show_hp()
        for e in self.tear:
            e.draw_tear()
        for e in self.redtear:
            e.draw_tear()
        for e in self.mob:
            e.draw_unit()





