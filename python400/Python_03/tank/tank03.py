"""
author:风起于青萍之末，浪成于微澜之间
project:learn_python
date:2022/10/12
"""
# coding=utf8
import random

import pygame
import time
import os

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 200
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(255, 0, 0)
SPEED = 10


class MainGame:
    window = None
    my_tank = None
    enemyTankList = []
    enemyTankCount = 5
    myBulletlist=[]
    def __init__(self):
        pass

    def starGame(self):
        pygame.display.init()

        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        MainGame.my_tank = Tank(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.creatEnemyTank()
        pygame.display.set_caption('坦克大战1.0')
        while True:
            time.sleep(0.05)
            self.getEvent()
            MainGame.window.fill(BG_COLOR)
            MainGame.window.blit(self.getTextSufacr(f'敌方坦克剩余数量:{len(MainGame.enemyTankList)}'), (10, 10))
            MainGame.my_tank.displayTank()
            self.biltEnemyTank()
            self.biltMyBullet()
            if not MainGame.my_tank.stop:
                MainGame.my_tank.move()
            pygame.display.update()

    def endGame(self):
        print('退出')
        exit()

    def creatEnemyTank(self):
        top = 10
        for i in range(MainGame.enemyTankCount):
            left = random.randint(0, SCREEN_WIDTH)
            speed = random.randint(1, 4)
            enemy = EnemyTank(left, top, speed)
            print(left, top, speed)
            MainGame.enemyTankList.append(enemy)

    def biltEnemyTank(self):
        for enemyTank in MainGame.enemyTankList:
            # print(enemyTank)
            enemyTank.displayTank()
            enemyTank.randMove()

    def biltMyBullet(self):
        for myBullet in MainGame.myBulletlist:
            # print(enemyTank)
            myBullet.displayBullet()
    def getTextSufacr(self, text):
        pygame.font.init()
        # print(pygame.font.get_fonts())
        font = pygame.font.SysFont('kaiti', 18)
        return font.render(text, True, TEXT_COLOR)

    def getEvent(self):
        eventList = pygame.event.get()
        for event in eventList:
            if event.type == pygame.QUIT:
                self.endGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    MainGame.my_tank.direction = 'L'
                    # MainGame.my_tank.move()
                    MainGame.my_tank.stop = False
                    print('向左移动')
                elif event.key == pygame.K_RIGHT:
                    MainGame.my_tank.direction = 'R'
                    # MainGame.my_tank.move()
                    MainGame.my_tank.stop = False
                    print('向右移动')
                elif event.key == pygame.K_UP:
                    MainGame.my_tank.direction = 'U'
                    MainGame.my_tank.stop = False
                    # MainGame.my_tank.move()
                    print('向上移动')
                elif event.key == pygame.K_DOWN:
                    MainGame.my_tank.direction = 'D'
                    MainGame.my_tank.stop = False
                    # MainGame.my_tank.move()
                    print('向下移动')
                elif event.key == pygame.K_SPACE:
                    print('bububu')
                    myBullet=Bullet(MainGame.my_tank)
                    MainGame.myBulletlist.append(myBullet)
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT):
                    MainGame.my_tank.stop = True


class Tank:
    def __init__(self, left, top):
        self.images = {'U': pygame.image.load('img/tankU.gif'),
                       'D': pygame.image.load('img/tankD.gif'),
                       'L': pygame.image.load('img/tankL.gif'),
                       'R': pygame.image.load('img/tankR.gif')
                       }
        self.direction = 'R'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left
        self.speed = SPEED
        self.stop = True

    def move(self):
        if self.direction == 'L' and self.rect.left > 0:
            self.rect.left -= self.speed
        elif self.direction == 'R' and self.rect.left + self.rect.width < SCREEN_WIDTH:
            self.rect.left += self.speed
        elif self.direction == 'U' and self.rect.top - self.speed > 0:
            self.rect.top -= self.speed
        elif self.direction == 'D' and self.rect.top + self.rect.width < SCREEN_HEIGHT:
            self.rect.top += self.speed

    def shot(self):
        pass

    def displayTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


class EnemyTank(Tank):
    def __init__(self, left, top, speed):
        super().__init__(left, top)
        self.images = {'U': pygame.image.load('img/tankU.gif'),
                       'D': pygame.image.load('img/tankD.gif'),
                       'L': pygame.image.load('img/tankL.gif'),
                       'R': pygame.image.load('img/tankR.gif')
                       }
        self.direction = self.randDirection()
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.speed = speed
        self.flag = True
        self.step = 10

    def randDirection(self):
        num = random.randint(1, 4)
        if num == 1:
            return 'U'
        elif num == 2:
            return 'D'
        elif num == 3:
            return 'L'
        elif num == 4:
            return 'R'

    def randMove(self):
        if self.step <= 0:
            self.direction = self.randDirection()
            self.step = 20
        else:
            self.move()
            self.step -= 1

class Bullet:
    def __init__(self,tank):
        self.image = pygame.image.load('img/enemybullet.png')
        self.rect = self.image.get_rect()
        self.direction = tank.direction
        print(self.direction)
        if self.direction == 'U':
            self.rect.left = tank.rect.left + tank.rect.width/2 - self.rect.width*1.2
            self.rect.top = tank.rect.top - self.rect.height
        elif self.direction == 'D':
            self.rect.left = tank.rect.left + tank.rect.width / 2 - self.rect.width*1.75
            self.rect.top = tank.rect.top + tank.rect.height + self.rect.height
            print(f'坦克:{tank.rect.top},{tank.rect.left},{tank.rect.width},{tank.rect.height}')
            print(f'子弹:{self.rect.top},{self.rect.left},{self.rect.width},{self.rect.height}')
        elif self.direction == 'L':
            self.rect.left = tank.rect.left - self.rect.width / 2
            self.rect.top = tank.rect.top + tank.rect.width / 2 - self.rect.height
        elif self.direction == 'R':
            self.rect.left = tank.rect.left + tank.rect.width
            self.rect.top = tank.rect.top + tank.rect.width/2 - self.rect.height
        self.speed = 6
    def move(self):
        pass

    def displayBullet(self):
        MainGame.window.blit(self.image,self.rect)

if __name__ == '__main__':
    x = MainGame()
    x.starGame()
