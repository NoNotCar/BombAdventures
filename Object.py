import Img
class Object(object):
    is3d=True
    img=None
    destructible=True
    def get_img(self):
        return self.img
class Block(Object):
    img=Img.img2("Block")
class Indest(Object):
    img=Img.img2("Grass2")
    destructible = False