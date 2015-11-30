import Img
class Object(object):
    is3d=True
    img=None
    destructible=True
    def get_img(self):
        return self.img
    def update(self,world):
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
