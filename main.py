import pygame as pg
import time
import numpy as np
#from Agent import agent
from sprites import *
import setting

#색상 변수

myfont= pg.font.Font('C:\\Users\\jihun\\Desktop\\breakout\\font\\neodgm_pro.ttf',30)#한글 도트 폰트 위치
pg.display.set_caption("Break out")

#하트
heart = pg.image.load(r"C:\\Users\\jihun\\Desktop\\breakout\\images\\heart.png").convert_alpha()#하트 사진 불러오기
heart = pg.transform.scale(heart, (70,70))



#시간 체크
start_time = time.time()
game_start = True
restart = False
done = 1
#루프
while done:
    #fps 설정
    setting.clock.tick(setting.FPS)

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
        restart = False
        episode +=1
        ball_group.empty()
        ball1 = ball(setting.size[0]/2,setting.size[1]/3*2)
        ball_group.add(ball1)
        brick_group.empty()
        for row in range(setting.brick_row):
            for column in range(setting.brick_column):
                brick1 = brick(brick_interval+column*(brick_width+brick_interval),setting.size[1]/10+brick_interval+row*(brick_height+brick_interval),\
                    brick_width,brick_height)
                brick_group.add(brick1)
        setting.life = 3
        start_time = time.time()


    #스크린 배경 색상
    setting.screen.fill(Black)

    #공이 바닥에 떨어지면 생명-1,새로운 공 발사
    if not len(ball_group):
        setting.life -=1
        ball1 = ball(setting.size[0]/2,setting.size[1]/3*2,speed=setting.ball_vel)
        ball_group.add(ball1)
    #패들 업데이트(에이전트 업데이트)
    paddle_group.update()    
    #공 업데이트
    ball_group.update()
    

    #하트 없어지면 '게임 오버' 메세지 출력 후시작 화면으로 
    if not setting.life:
        restart = True            
    #벽돌을 다 때면 종료
    if not len(brick_group):
        pg.quit()      # 벽돌을 다깨면 종료

    #벽돌 업데이트
    brick_group.update()

    #하트 업데이트
    for i in range(setting.life,0,-1):
        setting.screen.blit(heart, (10+50*(i-1), 10))
    #프레임 표시 
    msg_fps = myfont.render("fps : {}".format(int((setting.clock.get_fps()))),True,White)
    setting.screen.blit(msg_fps,(setting.size[0]-200,70))
    #시간 표시
    msg_time = myfont.render("time : {}s".format(int(time.time()-start_time)+1),True,White)
    setting.screen.blit(msg_time,(setting.size[0]-200,40))
    pg.display.flip()
pg.quit()

"""
---벽돌깨기 ai계획---
    1.다시 사작(reset)기능 추가
    2.보상(점수) 기능 추가
    3.agent->play(action) 기능
    4.게임 반복
"""