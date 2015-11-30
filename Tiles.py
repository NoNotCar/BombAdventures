__author__ = 'NoNotCar'
import Img, Entities


class Tile(object):
    img = None
    solid = True
    slippery=False


class Grass(Tile):
    img = Img.img2("Grass")


class Goal(Tile):
    img = Img.imgsz("Goal", (32, 40))
class Ice(Tile):
    img=Img.img2("Ice")
    slippery = True


tiles = (Grass(), Goal(), Ice())
eobjs = ((Img.img2("Block"), 1), (Img.imgstrip("Ghost")[0], 0), (Img.img2("Man2"), 0), (Img.imgstrip2("Thud")[0], 0),
         (Img.img32("RangeUp"), 0),(Img.img2("Grass2"),1),(Img.imgstrip("FGhost")[0], 0),(Img.img2("SokoBlok"),0))
eents = {2: Entities.Ghost, 4: Entities.Thud, 5: Entities.RangeUp,7:Entities.FGhost,8:Entities.SokoBlock}
