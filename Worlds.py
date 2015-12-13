import Img


class World(object):
    def __init__(self, txt, mus, back, load):
        self.textures = txt
        self.music = mus
        self.back = back
        self.loadcolour = load


worlds = [World([Img.img2("Grass"), Img.img2("Block"), Img.img2("Grass2")], "Cumulo", (125, 255, 255), (125, 225, 0)),
          World([Img.img2("Snow"), Img.img2("CastleBlock"), Img.img2("FrozenIn")], "Chr", (240, 240, 240),
                (255, 255, 255)),
          World([Img.img2("Spacefloor"), Img.img2("CastleBlock"), Img.img2("CastleIn")], "Spacetime", (0, 0, 0),
                (50, 50, 50)),
          World([Img.img2("Sand"), Img.img2("Block"), Img.img2("CastleInGrey"), Img.img2("Oil")], "Desert",
                (181, 117, 0), (250, 250, 0)),
          World([Img.img2("Spacefloor"), Img.img2("CastleBlock"), Img.img2("PuzzBlock"),Img.img2("IceSpace")], "ChOrDs", (255, 255, 255),
                (255, 255, 255)),
          World([Img.img2("RockSnow"), Img.img2("RedBlock"), Img.img2("CastleIn"), Img.img2("RockIce")], "W5V",
                (255, 93, 0), (200, 59, 0)),
          World([Img.img2("PinkGround"), Img.img2("PinkBlock"), Img.img2("Pink2"), Img.img2("PinkIce")], "DOMINIK_4", (255, 186, 245),
                (255, 81, 226)),
          World([Img.img2("RedGrass"), Img.img2("RedBlock"), Img.img2("CastleIn"), Img.img2("RockIce")], "Devil",
                (84, 2, 0), (133, 5, 1))]
castle = World([Img.img2("CastleFloor"), Img.img2("CastleBlock"), Img.img2("CastleIn")], "Flags", (125, 125, 125),
               (200, 200, 200))
