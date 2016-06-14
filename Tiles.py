__author__ = 'NoNotCar'
import Img, Entities


class Tile(object):
    img = None
    solid = True
    slippery = False

    def update(self, world, x, y):
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

    def update(self, world, x, y):
        gent = world.get_ent(x, y)
        if gent and gent.name == "Sokoblock":
            world.t[x][y] = 7


class SokoPlateAct(Tile):
    img = Img.img2("SokoPlateAct")

    def update(self, world, x, y):
        gent = world.get_ent(x, y)
        if not gent or gent.name != "Sokoblock":
            world.t[x][y] = 6


class ManPlate(Tile):
    img = Img.img2("ManPlate")

    def update(self, world, x, y):
        gent = world.get_ent(x, y)
        if gent and gent in world.ps:
            world.t[x][y] = 11


class ManPlateAct(Tile):
    img = Img.img2("ManPlateAct")

    def update(self, world, x, y):
        gent = world.get_ent(x, y)
        if not gent or gent not in world.ps:
            world.t[x][y] = 10


class DarkMatter(Tile):
    img = Img.img2("DarkMatter")

    def update(self, world, x, y):
        gent = world.get_ent(x, y)
        if gent and not gent.moving and not gent.darkresist:
            if gent in world.ps:
                world.playerdead = True
            else:
                world.e.remove(gent)
            world.create_exp(x, y, 0, True)


tiles = (Grass(), Goal(), Ice(), SokoHole(), SokoHoleFilled(), SokoPlate(), SokoPlateAct(), BonusGoal(), WarpGoal(),
         ManPlate(), ManPlateAct(), DarkMatter())
eobjs = (
            (Img.img2("Block"), 1), (Img.imgstrip("Ghost")[0], 0), (Img.img2("Men/Man2"), 0),
            (Img.imgstrip2("Thud")[0], 0),
            (Img.img32("RangeUp"), 0), (Img.img2("Grass2"), 1), (Img.imgstrip("FGhost")[0], 0),
            (Img.img2("SokoBlok"), 0),
            (Img.img2("SokoLok"), 1), (Img.img2("ExpBlock"), 1), (Img.img2("Pen"), 0), (Img.img2("ExBomb"), 0),
            (Img.imgsz("GhostSpawn", (32, 40)), 1), (Img.imgstrip2("Slime")[0], 0), (Img.img2("CannonBlock"), 1),
            (Img.img2("Men/SMan"), 0), (Img.img2("Men/FMan"), 0), (Img.img2("Men/TMan"), 0),
            (Img.img2("SokoBlokIce"), 0),
            (Img.img2("Null"), 0), (Img.img2("SokoBlokGoo"), 0), (Img.imgstrip("TGhost")[0], 0)) + tuple(
    [(Img.imgstrip2("GraviBlok")[n], 0) for n in range(4)]) + (
        (Img.img2("FireballL2"), 0), (Img.imgstrip("FireGhost")[0], 0), (Img.img2("FireballL3"), 0))
tilemenus = ([0], (2, 11), (1, 7, 8), (3, 4, 5, 8, 9))
objmenus = (
(0, 5, 9), (1, 3, 6, 12, 13, 14, 21, 26, 27, 28), (2, 15, 16, 17), (7, 8, 18, 20), (4, 10, 11, 19), (22, 23, 24, 25))
eents = {2: Entities.Ghost, 4: Entities.Thud, 5: Entities.RangeUp, 7: Entities.FGhost, 8: Entities.SokoBlock,
         11: Entities.Penetrating, 12: Entities.BombPlus, 14: Entities.Slime, 19: Entities.SokoBlokSlippy,
         20: Entities.NullPower, 21: Entities.SokoBlockGoo, 22: Entities.TGhost, 27: Entities.FireballLauncher,
         28: Entities.FireGhost, 29: Entities.HFireballLauncher}
