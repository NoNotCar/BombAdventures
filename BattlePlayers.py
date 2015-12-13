from Entities import Entity, Bomb, iround
import pygame
from Img import img2


class Player(Entity):
    orect = pygame.Rect(10, 2, 12, 28)
    enemy = False
    bombs = 1
    rng = 2
    pen = False
    dy = 1
    iconv = {(0, -1): img2("Men/Man2u"), (0, 1): img2("Men/Man2"), (1, 0): img2("Men/Man2r"), (-1, 0): img2("Men/Man2l")}
    ms = 2
    akey = pygame.K_UP
    rd=False
    detonate=False
    def __init__(self,x,y,c):
        self.place(x,y)
        self.c=c


    def update(self, world, events):
        if self.detonate:
            self.detonate=False
        for d in self.c.get_dirs():
            if self.move(d[0], d[1], self.ms, world):
                break
        bpress=self.c.get_buttons(events)
        if bpress[0] and self.bombs:
            world.e.append(
                Bomb(iround((self.x * 32 + self.xoff) / 32.0), iround((self.y * 32 + self.yoff) / 32.0),
                     self.rng,
                     self))
            self.bombs -= 1
        if bpress[1] and self.rd:
            self.detonate=True
        if not self.moving:
            tile = world.t[self.x][self.y]
            if tile == 2:
                world.done = True
            elif tile == 8:
                world.done = True
                world.exitcode = "SECRET"
            elif tile == 9:
                world.done = True
                world.exitcode = "WARP"

    def get_img(self):
        return self.iconv[(self.dx, self.dy)]

class SmallPlayer(Player):
    orect = pygame.Rect(12, 4, 8, 24)
    rng = 1
    ms = 4
    iconv = {(0, -1): img2("Men/SManu"), (0, 1): img2("Men/SMan"), (1, 0): img2("Men/SManr"), (-1, 0): img2("Men/SManl")}


class FatPlayer(Player):
    orect = pygame.Rect(8, 2, 16, 28)
    rng = 2
    bombs = 2
    ms = 1.5
    pen = True
    sticky = True
    iconv = {(0, -1): img2("Men/FManu"), (0, 1): img2("Men/FMan"), (1, 0): img2("Men/FManr"), (-1, 0): img2("Men/FManl")}

class ThinPlayer(Player):
    orect = pygame.Rect(12, 2, 8, 28)
    rng = 3
    rd = True
    iconv = {(0, -1): img2("Men/TManu"), (0, 1): img2("Men/TMan"), (1, 0): img2("Men/TManr"), (-1, 0): img2("Men/TManl")}