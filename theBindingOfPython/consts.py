import pygame
from math import sqrt
board_size = [800, 600]


window = pygame.display.set_mode(board_size)
screen = pygame.display.get_surface()
clock  = pygame.time.Clock()

heart_img = pygame.image.load('models/heart.png')
empty_heart_img = pygame.image.load('models/empty_heart.png')
newton_img = pygame.image.load('models/newton.png')
tear_img = pygame.image.load('models/tear.png')
board_img = pygame.image.load('models/board.png')
slowmob_img = pygame.image.load('models/slowmob.png')
redtear_img = pygame.image.load('models/redtear.png')
lose_img = pygame.image.load('models/lose.png')


def vector(p, q, s): #używam żeby policzyć jak ma sie przesunąć npc w stronę gracza
    x = p / (q + 0.000001)
    x = sqrt(s / (x*x + 1))
    y = sqrt( s - x)
    if p > 0 and q > 0:
        v = [-y, -x]
    elif p > 0 and q < 0:
        v = [-y, x]
    elif p < 0 and q > 0:
        v = [y, -x]
    else: v = [y, x]
    return v

