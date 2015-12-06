__author__ = 'NoNotCar'
import Img, Entities


class Tile(object):
    img = None
    solid = True
    slippery = False
    def update(self,world,x,y):
        pass


class Grass(Tile):
    img = Img.img2("Grass")


class Goal(Tile):
    img = Img.imgsz("Goal", (32, 40))


class BonusGoal(Tile):
    img = Img.imgsz("BonusGoal", (32, 40))

class WarpGoal(Tile):
    img = Img.img2("Warp")


class Ice(Tile):
    img = Img.img2("Ice")
    slippery = True


class SokoHole(Tile):
    img = Img.img2("SokoHol")


class SokoHoleFilled(Tile):
    img = Img.img2("SokoHolFilled")

class SokoPlate(Tile):
    img = Img.img2("SokoPlate")
    def update(self,world,x,y):
        gent=world.get_ent(x,y)
        if gent and gent.name=="Sokoblock":
            world.t[x][y]=7

class SokoPlateAct(Tile):
    img = Img.img2("SokoPlateAct")
    def update(self,world,x,y):
        gent=world.get_ent(x,y)
        if not gent or gent.name!="Sokoblock":
            world.t[x][y]=6



tiles = (Grass(), Goal(), Ice(), SokoHole(), SokoHoleFilled(),SokoPlate(),SokoPlateAct(), BonusGoal(),WarpGoal())
eobjs = ((Img.img2("Block"), 1), (Img.imgstrip("Ghost")[0], 0), (Img.img2("Man2"), 0), (Img.imgstrip2("Thud")[0], 0),
         (Img.img32("RangeUp"), 0), (Img.img2("Grass2"), 1), (Img.imgstrip("FGhost")[0], 0), (Img.img2("SokoBlok"), 0),
         (Img.img2("SokoLok"), 1), (Img.img2("ExpBlock"), 1), (Img.img2("Pen"), 0), (Img.img2("ExBomb"), 0),
         (Img.imgsz("GhostSpawn",(32,40)), 1),(Img.imgstrip2("Slime")[0],0),(Img.img2("CannonBlock"),1))
eents = {2: Entities.Ghost, 4: Entities.Thud, 5: Entities.RangeUp, 7: Entities.FGhost, 8: Entities.SokoBlock,
         11: Entities.Penetrating, 12: Entities.BombPlus, 14:Entities.Slime}
