import Img
from random import randint

class FX(object):
    img=None
    dead=False
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def update(self):
        pass
class Snow(FX):
    img=Img.img2("SnowFX")
    def update(self):
        self.y+=randint(1,3)
        self.x+=randint(-1,1)
        if self.y>640:
            self.dead=True