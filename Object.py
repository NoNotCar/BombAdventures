import Img
class Object(object):
    is3d=True
    img=None
    destructible=True
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def get_img(self):
        return self.img
    def update(self,world):
        pass
    def explode(self,world):
        pass
class Block(Object):
    img=Img.img2("Block")
class Indest(Object):
    img=Img.img2("Grass2")
    destructible = False
class SokoLock(Object):
    img=Img.img2("SokoLok")
    img2=Img.img2("SokoLokOpen")
    destructible = False
    lockopen = False
    updtick=0
    def get_img(self):
        return self.img2 if self.lockopen else self.img
    def update(self,world):
        if not self.lockopen:
            if self.updtick!=60:
                self.updtick+=1
            else:
                self.updtick=0
                breaking=False
                for row in world.t:
                    for t in row:
                        if t==4:
                            breaking=True
                            break
                    if breaking:
                        break
                else:
                    self.lockopen=True
                    self.destructible=True
class ExplosiveBlock(Object):
    img=Img.img2("ExpBlock")
    destructible = False
    timer=None
    eimgs=[Img.img2("ExpBlockAct"+str(n+1)) for n in range(2)]
    def update(self,world):
        if self.timer is not None:
            self.timer-=1
            if self.timer==0:
                world.o[self.x][self.y]=None
                world.create_exp(self.x,self.y,2)
    def explode(self,world):
        self.timer=30
    def get_img(self):
        if self.timer is None:
            return self.img
        return self.eimgs[self.timer//3%2]
