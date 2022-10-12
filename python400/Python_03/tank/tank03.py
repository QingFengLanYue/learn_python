"""
author:风起于青萍之末，浪成于微澜之间
project:learn_python
date:2022/10/12
"""
# coding=utf8

import pygame
import os
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 500
BG_COLOR = pygame.Color(0, 0, 0)
TEXT_COLOR = pygame.Color(255, 0, 0)


class MainGame:
    window = None
    my_tank = None

    def __init__(self):
        pass

    def starGame(self):
        pygame.display.init()

        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])
        pygame.display.set_caption('坦克大战1.0')
        while True:
            self.getEvent()
            MainGame.window.fill(BG_COLOR)
            MainGame.window.blit(self.getTextSufacr(f'敌方坦克剩余数量:{6}'), (10, 10))
            MainGame.my_tank = Tank(100, 250)
            MainGame.my_tank.displaceTank()
            pygame.display.update()

    def endGame(self):
        print('退出')
        exit()

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
                    print('向左移动')
                elif event.key == pygame.K_RIGHT:
                    print('向右移动')
                elif event.key == pygame.K_UP:
                    print('向上移动')
                elif event.key == pygame.K_DOWN:
                    print('向下移动')


class Tank:
    def __init__(self, left, top):
        self.images = {'U': pygame.image.load('tankU.gif'),
                       'D': pygame.image.load('tankD.gif'),
                       'L': pygame.image.load('tankL.gif'),
                       'R': pygame.image.load('tankR.gif')
                       }
        self.direction = 'U'
        self.image = self.images[self.direction]
        self.rect = self.image.get_rect()
        self.rect.top = top
        self.rect.left = left

    def move(self):
        pass

    def shot(self):
        pass

    def displaceTank(self):
        self.image = self.images[self.direction]
        MainGame.window.blit(self.image, self.rect)


if __name__ == '__main__':
    x = MainGame()
    x.starGame()


