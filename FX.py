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

class TPFX(FX):
    imgs=Img.imgstrip("TeleportFX")
    anitick=0
    img=imgs[0]
    def update(self,world):
        self.anitick+=1
        self.img=self.imgs[self.anitick//2]
        if self.anitick==11:
            world.fx.remove(self)
class Missile(FX):
    img=Img.img2("Missile")
    def __init__(self,x,y,ty):
        self.x=x
        self.y=y
        self.ty=ty
    def update(self,world):
        if self.y<self.ty-16:
            self.y+=4
        else:
            world.fx.remove(self)
class MissileTarget(FX):
    rimg=Img.img2("Target")
    wimg=Img.img2("TargetW")
    imgn=0
    img=rimg
    def __init__(self,x,y,m):
        self.x=x
        self.y=y
        self.m=m
    def update(self,world):
        if self.m not in world.fx:
            world.fx.remove(self)
            world.create_exp(self.x//32,self.y//32,20, True)
        if self.imgn<3:
            self.imgn+=1
        else:
            self.imgn=0
        self.img=[self.rimg,self.wimg][self.imgn//2]
class Fez(FX):
    img = Img.img2("Fez")
    def update(self,world):
        self.x=world.p.x*32+world.p.xoff+6
        self.y=world.p.y*32+world.p.yoff-10