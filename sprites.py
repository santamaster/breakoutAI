import random
import math
import pygame as pg
import time
import numpy as np
from  Agent import agent
from setting import *
pg.init()

#<-----변수 설정----->
White = (255,255,255)
Red = (255,0,0)
Yellow = (255,255,0)
Green = (0,255,0)
Blue = (0,0,255)
Vivid_Blue = (0,153,255)
Purple = (138,43,226)
Gray = (128,128,128)
Black = (0,0,0)




brick_width = size[0]/(brick_column+1)#벽돌 가로 길이
brick_height = brick_width/2#벽돌 세로 길이
brick_interval = size[0]*1/((brick_column+1)*(brick_column+1))#벽돌간 간격
player = agent()



class ball(pg.sprite.Sprite):
    def __init__(self,x,y,speed=6):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.degree = random.uniform(200,340)
        self.vel = speed
        self.rect = pg.Rect(0,0,ball_size,ball_size)
        self.brick_collision_count = -1
        self.time = time.time()
    #공 움직임
    def move(self):
        global ball_vel
        if time.time()-self.time>5 and self.vel <=14:#5초마다 속도가 0.5씩 빨라짐(최대 속도 :17)
            self.vel +=0.5
            ball_vel = self.vel
            self.time = time.time()
        if self.x <= 0:
            self.degree = 180 - self.degree
            self.x = 0
        elif self.x >= size[0]:
            self.degree = 180 - self.degree
            self.x = size[0]
        if self.y <= 0:
            self.degree = 360 - self.degree
        if self.y >= size[1]:
            self.kill()
            
        self.x += self.vel * math.cos(math.radians(self.degree))
        self.y += self.vel * math.sin(math.radians(self.degree))
        self.rect = pg.Rect(0,0,ball_size,ball_size)
        self.rect.center = [self.x,self.y]
        pg.draw.ellipse(screen,Red,self.rect)
    #공 패들 충돌
    def pad_collide(self):
        collided_paddle=pg.sprite.spritecollide(self,paddle_group,False)
        if collided_paddle:
            c_pad = collided_paddle[0]
            self.degree = 200 + (self.x-c_pad.rect.x)/c_pad.width*140
            self.y = size[1]*9/10 - ball_size
            self.brick_collision_count = -1# 추가 점수 초기화
    #공 벽돌 충돌
    def brick_collide(self):
        if self.degree<0:
            self.degree +=360
        if self.degree>360:
            self.degree -=360
        collided_brick = pg.sprite.spritecollide(self,brick_group,False)
        if collided_brick:
            self.brick_collision_count += len(collided_brick)
            reward = 50*len(collided_brick) +10*self.brick_collision_count# 기본 점수:50점|추가 점수:10점
            collided_b = collided_brick[0].rect
            if self.degree<90:
                if abs(self.rect.bottomright[0]-collided_b.topleft[0])>abs(collided_b.topleft[1]-self.rect.bottomright[1]):
                    self.degree = 360-self.degree
                    self.y = collided_b.y-ball_size-self.vel/2
                else:
                    self.degree = 180-self.degree
                    self.x = collided_b.x-ball_size-self.vel/2
            elif self.degree<180:
                if abs(collided_b.topright[0]-self.rect.bottomleft[0])>abs(collided_b.topright[1]-self.rect.bottomleft[1]):
                    self.degree = 360-self.degree
                    self.y = collided_b.y-ball_size-self.vel/2
                else:
                    self.degree = 180-self.degree
                    self.x = collided_b.x+brick_width+self.vel/2
            elif self.degree<270:
                if abs(collided_b.bottomright[0]-self.rect.topleft[0])>abs(self.rect.topleft[1]-collided_b.bottomright[1]):
                    self.degree = 360 - self.degree
                    self.y = collided_b.y+brick_height+self.vel/2
                else:
                    self.degree = 540-self.degree
                    self.x = collided_b.x+brick_width+self.vel/2
            elif self.degree<360:
                if abs(self.rect.topright[0]-collided_b.bottomleft[0])>abs(collided_b.bottomleft[1]-self.rect.topright[1]):
                    self.degree = 360- self.degree
                    self.y = collided_b.y+brick_height+self.vel/2
                else:
                    self.degree = 540-self.degree
                    self.x = collided_b.x-ball_size-self.vel/2
            #아이템 생성
            if random.random()<0.0:#0%확률로 아이템 생성(아이템 생성 X)
                item1 = item(collided_b.x+brick_width/2,collided_b.y+brick_height/2)
                item_group.add(item1)
            index = list(brick_group).index(collided_brick[0])
            np.put(brick_array,index,0)

            collided_brick[0].kill()

    #업데이트
    def update(self):
        self.move()
        self.pad_collide()
        self.brick_collide()
        


#패들
class paddle(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.width= size[0]/7
        self.height = 10
        self.rect = pg.Rect(size[0]/2,size[1]*9/10,self.width,self.height)
        self.vel = 25
    def draw(self):
        pg.draw.rect(screen,White,self.rect)
    def move(self):
        player.move()
        if player.action == 1: # right
            if self.rect.right<size[0]:
                self.rect.x += self.vel

        elif player.action == 0: # left
            if self.rect.left>0:
                self.rect.x -= self.vel
    #아이템 충돌
    def item_collide(self):
        collided_item = pg.sprite.spritecollide(self,item_group,False)
        if collided_item:
            for _ in range(2):
                ball1 = ball(self.rect.x+self.width/2,self.rect.y-40,speed=ball_vel)
                ball_group.add(ball1)
            collided_item[0].kill()

    def update(self):
        self.move()
        self.draw()
        #self.item_collide()
#벽돌
class brick(pg.sprite.Sprite):
    def __init__(self,x,y,width,height):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pg.Rect(self.x,self.y,self.width,self.height)
    def draw(self):
        pg.draw.rect(screen,Purple,self.rect)
    def update(self):
        self.draw()

#아이템
class item(pg.sprite.Sprite):
    def __init__(self,x,y):
        pg.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = self.height = 30
        self.rect = pg.Rect(self.x,self.y,self.width,self.height)
        self.vel = 3
    def draw(self):
        pg.draw.rect(screen,Vivid_Blue,self.rect)
    def move(self):
        self.rect.y +=self.vel
        if self.rect.y>size[1]:
            self.kill()
    def update(self):
        self.draw()
        self.move()


#<-----스프라이트 그룹 생성----->

#공
ball_size = 15
ball_group= pg.sprite.Group()

ball1 = ball(size[0]/2,size[1]/3*2)
ball_group.add(ball1)

#벽돌 그룹 생성
brick_group = pg.sprite.Group()
for row in range(brick_row):
    for column in range(brick_column):
        brick1 = brick(brick_interval+column*(brick_width+brick_interval),size[1]/10+brick_interval+row*(brick_height+brick_interval),\
            brick_width,brick_height)
        brick_group.add(brick1)

#벽돌 배열 생성(1차원)
brick_array = np.ones(shape=(brick_row*brick_column,),dtype=np.int8)

#패들 그룹 생성
paddle_group = pg.sprite.Group()
paddle1 = paddle()
paddle_group.add(paddle1)

#아이템 그룹 생성
item_group = pg.sprite.Group()