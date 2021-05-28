'''
author:cai
project:learn_python
date:2021/5/25
'''
from turtle import *
import random
# 设置色彩模式是RGB:
colormode(255)

lt(90)

lv1 = 14
lv=25
l = 120
s = 45

width(lv1)

# 初始化RGB颜色:
r = 0
g = 0
b = 0
pencolor(r, g, b)

penup()
bk(l)
pendown()
fd(l)

def draw_tree(l, level):
    global r, g, b
    # save the current pen width
    w = width()

    # narrow the pen width
    width(w * 3.0 / (3.0+random.random()))
    # set color:
    r = r + 1
    g = g + 2
    b = b + 3
    pencolor(r % 200, g % 200, b % 200)

    l = 3.0 / 4.0 * l

    lt(s)
    fd(l)

    if level < random.randint(5,lv):
        draw_tree(l, level + 1)
    bk(l)
    rt(2 * s)
    fd(l)

    if level < random.randint(8,lv):
        draw_tree(l, level + 1)
    bk(l)
    lt(s)

    # restore the previous pen width
    width(w)

speed("fastest")

draw_tree(l, 2)

done()