import math
import pygame as pg
import time
import random
import numpy as np
from Agent import agent
pg.init()
#색상 변수
White = (255,255,255)
Red = (255,0,0)
Yellow = (255,255,0)
Green = (0,255,0)
Blue = (0,0,255)
Vivid_Blue = (0,153,255)
Purple = (138,43,226)
Gray = (128,128,128)
Black = (0,0,0)

#시스템 설정 
size = [1366,768] 
screen = pg.display.set_mode(size)
clock = pg.time.Clock()
FPS = 60
done = 1
myfont= pg.font.Font('C:\\Users\\jihun\\Desktop\\breakout\\font\\neodgm_pro.ttf',30)#한글 도트 폰트 위치
pg.display.set_caption("Break out")
life = 3
score = 0
ball_vel = 6
#소리
game_over_sound = pg.mixer.Sound('C:\\Users\\jihun\\Desktop\\breakout\\sounds\\mixkit-retro-arcade-game-over-470.wav')
play_game_over_sound = 1

#agent initialize
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
            global score
            self.brick_collision_count += len(collided_brick)
            score += 50*len(collided_brick) +10*self.brick_collision_count# 기본 점수:50점|추가 점수:10점
            
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
            collided_brick[0].kill()

    #업데이트
    def update(self):
        self.move()
        self.pad_collide()
        self.brick_collide()
#공
ball_size = 15
ball_group= pg.sprite.Group()

ball1 = ball(size[0]/2,size[1]/3*2)
ball_group.add(ball1)

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


brick_column = 18
brick_row = 6

brick_width = size[0]/(brick_column+1)#벽돌 가로 길이
brick_height = brick_width/2#벽돌 세로 길이
brick_interval = size[0]*1/((brick_column+1)*(brick_column+1))#벽돌간 간격

#벽돌 그룹 생성
brick_group = pg.sprite.Group()
for row in range(brick_row):
    for column in range(brick_column):
        brick1 = brick(brick_interval+column*(brick_width+brick_interval),size[1]/10+brick_interval+row*(brick_height+brick_interval),\
            brick_width,brick_height)
        brick_group.add(brick1)
#패들 그룹 생성
paddle_group = pg.sprite.Group()
paddle1 = paddle()
paddle_group.add(paddle1)
#아이템 그룹 생성
item_group = pg.sprite.Group()
#하트
heart = pg.image.load(r"C:\\Users\\jihun\\Desktop\\breakout\\images\\heart.png").convert_alpha()#하트 사진 불러오기
heart = pg.transform.scale(heart, (70,70))

#게임 시작화면
msg_game_start = myfont.render("press spacebar to start game",True,White)
msg_game_start_rect = msg_game_start.get_rect(center=(size[0]/2, size[1]/2))
game_start = True
#게임 오버 화면
msg_lose = myfont.render("GAME OVER!",True,White)
msg_lose_rect = msg_lose.get_rect(center=(size[0]/2, size[1]/2))
restart = False
#게임 성공 화면
msg_win = myfont.render(f"CLEAR!",True,White)
msg_win_rect = msg_win.get_rect(center=(size[0]/2, size[1]/2))

#시간 체크
start_time = time.time()

#루프
while done:
    #fps 설정
    clock.tick(FPS)

    #이벤트 처리
    keys = pg.key.get_pressed()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = 0
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                done = 0
            
    #다시시작
    if restart:
        #초기화
        game_start = True
        ball_group.empty()
        item_group.empty()
        ball1 = ball(size[0]/2,size[1]/3*2)
        ball_group.add(ball1)
        brick_group.empty()
        for row in range(brick_row):
            for column in range(brick_column):
                brick1 = brick(brick_interval+column*(brick_width+brick_interval),size[1]/10+brick_interval+row*(brick_height+brick_interval),\
                    brick_width,brick_height)
                brick_group.add(brick1)
        score = 0
        life = 3
        restart = False

    #스크린 배경 색상
    screen.fill(Black)

    #게임 시작화면
    if not restart and game_start:
        #공이 바닥에 떨어지면 생명-1,새로운 공 발사
        if not len(ball_group):
            life -=1
            ball1 = ball(size[0]/2,size[1]/3*2,speed=ball_vel)
            ball_group.add(ball1)
        
        #공 업데이트
        ball_group.update()
        #패들 업데이트
        paddle_group.update()

    #하트 없어지면 '게임 오버' 메세지 출력 후시작 화면으로 
    if not life:
        restart = True
        
    
    #벽돌을 다 때면 종료
    if not len(brick_group):
        restart = True      #TODO: 벽돌을 다깨면 종료
        
    
    
    #벽돌 업데이트
    brick_group.update()
    #아이템 업데이트
    item_group.update()
    #하트 업데이트
    for i in range(life,0,-1):
        screen.blit(heart, (10+50*(i-1), 10))
    #프레임 표시 
    msg_fps = myfont.render("fps : {}".format(int((clock.get_fps()))),True,White)
    screen.blit(msg_fps,(size[0]-200,70))
    #점수 표시
    msg_score = myfont.render("score : {}".format(score),True,White)
    screen.blit(msg_score,(size[0]-200,10))
    #시간 표시
    msg_time = myfont.render("time : {}s".format(int(time.time()-start_time)+1),True,White)
    screen.blit(msg_time,(size[0]-200,40))
    pg.display.flip()
    
pg.quit()


"""
---벽돌깨기 ai계획---
    1.다시 사작(reset)기능 추가
    2.보상(점수) 기능 추가
    3.agent->play(action) 기능
    4.게임 반복
"""