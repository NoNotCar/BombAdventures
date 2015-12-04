import Img
from random import randint
import pygame

class FX(object):
    img=None
    dead=False
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def update(self,world):
        pass
class Snow(FX):
    img=Img.img2("SnowFX")
    def update(self,world):
        self.y+=randint(1,3)
        self.x+=randint(-1,1)
        if self.y>640:
            self.dead=True

class Star(FX):
    simg=pygame.Surface((2,2))
    img2=pygame.Surface((2,2))
    pygame.draw.rect(simg,(255,255,255),pygame.Rect(0,0,2,2))
    img=simg
    def update(self,world):
        if not randint(0,240):
            self.img=self.img2
        else:
            self.img=self.simg

class Fez(FX):
    img = Img.img2("Fez")
    def update(self,world):
        self.x=world.p.x*32+world.p.xoff+6
        self.y=world.p.y*32+world.p.yoff-10