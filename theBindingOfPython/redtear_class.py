import pygame
from tear_class import *

class Redtear(Tear):
    def shot_newton(self, newton):
        self.shoot()

    def dmg_newton(self, newton):
        if 0 < self.x + 10 - newton.x < 52 and 0 < self.y + 10 - newton.y < 80:
            return True
        return False
