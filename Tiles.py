__author__ = 'NoNotCar'
import Img, Entities


class Tile(object):
    img = None
    solid = True
    slippery = False


class Grass(Tile):
    img = Img.img2("Grass")


class Goal(Tile):
    img = Img.imgsz("Goal", (32, 40))


class Ice(Tile):
    img = Img.img2("Ice")
    slippery = True


class SokoHole(Tile):
    img = Img.img2("SokoHol")


class SokoHoleFilled(Tile):
    img = Img.img2("SokoHolFilled")


tiles = (Grass(), Goal(), Ice(), SokoHole(), SokoHoleFilled())
eobjs = ((Img.img2("Block"), 1), (Img.imgstrip("Ghost")[0], 0), (Img.img2("Man2"), 0), (Img.imgstrip2("Thud")[0], 0),
         (Img.img32("RangeUp"), 0), (Img.img2("Grass2"), 1), (Img.imgstrip("FGhost")[0], 0), (Img.img2("SokoBlok"), 0),
         (Img.img2("SokoLok"), 1), (Img.img2("ExpBlock"), 1), (Img.img2("Pen"), 0), (Img.img2("ExBomb"), 0),
         (Img.imgsz("GhostSpawn",(32,40)), 1))
eents = {2: Entities.Ghost, 4: Entities.Thud, 5: Entities.RangeUp, 7: Entities.FGhost, 8: Entities.SokoBlock,
         11: Entities.Penetrating, 12: Entities.BombPlus}
