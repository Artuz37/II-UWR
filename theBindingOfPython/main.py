import pygame
from time import sleep
from random import *
from consts import *
from unit_class import *
from newton_class import *
from board_class import *
from slowmob_class import *
from timer_class import *

pygame.init()
myfont = pygame.font.SysFont("comicsans", 40)

timer = Timer()
board = Board()
newton = board.newton
board.draw_board()
done = True



def update():
    make_action()
    new_tear_list = []
    new_redtear_list = []
    new_mob_list = []
    if timer.tick % 300 == 0:
        board.gen_mob(timer.tick)
    for mob in board.mob:
        mob.chase(newton)
        if mob.tick % 100 == 0:
            board.gen_redtear(mob, newton)
        if mob.hit(newton) and not timer.if_immune():
            newton.hp -= 1
            timer.immunity()
        if mob.alive:
            new_mob_list.append(mob)
        mob.tick += 1
    for tear in board.tear:
        tear.shoot()
        if not tear.collision(board) and not tear.hit_wall():
            new_tear_list.append(tear)
    for redtear in board.redtear:
        redtear.shot_newton(newton)
        if not redtear.dmg_newton(newton) and not redtear.hit_wall():
            new_redtear_list.append(redtear)
        if redtear.dmg_newton(newton) and not timer.if_immune():
            newton.hp -= 1
            timer.immunity()
    if newton.hp == 0:
        newton.alive = False
    board.mob = new_mob_list
    board.tear = new_tear_list
    board.redtear = new_redtear_list
    board.draw_board()
    timer.progress()
    label = myfont.render(str(timer.sec), 1, (255, 255, 0))
    screen.blit(label, (700, 13))

def event_action(event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            board.gen_tear([0, -5])
        if event.key == pygame.K_DOWN:
            board.gen_tear([0, 5])
        if event.key == pygame.K_LEFT:
            board.gen_tear([-5, 0])
        if event.key == pygame.K_RIGHT:
            board.gen_tear([5, 0])


def make_action():
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]: newton.unit_move((0, -3))
    if pressed[pygame.K_s]: newton.unit_move((0, 3))
    if pressed[pygame.K_a]: newton.unit_move((-3, 0))
    if pressed[pygame.K_d]: newton.unit_move((3, 0))

board.gen_mob(0)
while done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or not newton.alive:
            done = False
        if not newton.alive:
            screen.blit(lose_img, (0, 0))
            pygame.display.flip()
            sleep(5)
            done = False
        event_action(event)
    update()
    pygame.display.flip()
    clock.tick(60)