import pygame as pg


#시스템 설정
size = [700,700] 
screen = pg.display.set_mode(size)
clock = pg.time.Clock()
FPS = 60
life = 3
ball_vel = 6
brick_column = 12
brick_row = 5
episode = 1