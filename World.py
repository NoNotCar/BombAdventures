__author__ = 'NoNotCar'
import pygame, Img, Entities, Tiles, Object, sys

powerup=Img.sndget("powerup")
class World(object):
    def __init__(self, edit,level=None):
        self.edit = edit
        self.playerdead=False
        self.done=False
        if edit:
            self.t = []
            self.o = []
            for _ in range(20):
                self.t.append([0] * 20)
                self.o.append([0] * 20)
            self.e = []
        else:
            self.p = Entities.Player(0, 0)
            self.e = [self.p]
            savfile = open(Img.np("lvls//%s-%s.sav"%tuple(level)), "r")
            self.t = []
            self.o = []
            savr = savfile.readlines()
            self.fltext=savr[0][:-1]
            del savr[0]
            for row in savr[:20]:
                self.t.append([int(s) for s in row.split()])
            for x, row in enumerate(savr[20:]):
                self.o.append([None] * 20)
                crow = [int(s) for s in row.split()]
                for y, n in enumerate(crow):
                    if n:
                        eo = self.eoconvert(n)
                        if eo[1] == "obj":
                            self.o[x][y] = eo[0]()
                        elif eo[1]=="ent":
                            self.e.append(eo[0](x,y))
                        elif eo[1] == "spawn":
                            self.p.place(x,y)
            savfile.close()

    def update(self, ev):
        for e in self.e[:]:
            if e.moving:
                e.mupdate(self)
            e.update(self, ev)
        for e in self.e:
            e.rerect()
        dangers = [d.rect for d in self.e if d.denemy]
        for e in [e for e in self.e if not e.denemy and e.enemy]:
            if e.rect.collidelist(dangers) != -1:
                self.e.remove(e)
        if self.p.rect.collidelist([e.rect for e in self.e if e.enemy]) != -1:
            self.playerdead=True

    def render(self, s):
        for x, r in enumerate(self.t):
            for y, t in enumerate(r):
                if t:
                    s.blit(Tiles.tiles[t - 1].img, (x * 32, y * 32))
        for e in self.e:
            s.blit(e.img, (e.x * 32 + e.xoff, e.y * 32 + e.yoff))
        if self.edit:
            for x, r in enumerate(self.o):
                for y, o in enumerate(r):
                    if o:
                        s.blit(Tiles.eobjs[o - 1][0], (x * 32, y * 32 - Tiles.eobjs[o - 1][1] * 8))
        else:
            for x, r in enumerate(self.o):
                for y, o in enumerate(r):
                    if o:
                        s.blit(o.get_img(), (x * 32, y * 32 - 8 * o.is3d))

    def save(self):
        savfile = open("lvls//save.sav", "w")
        for row in self.t:
            savfile.write(" ".join([str(t) for t in row]) + "\n")
        for row in self.o:
            savfile.write(" ".join([str(t) for t in row]) + "\n")
        savfile.close()

    def inworld(self, x, y):
        return 0 <= x < 20 and 0 <= y < 20

    def is_clear(self, x, y, ent=None):
        for e in self.e:
            if e.x == x and e.y == y:
                if ent and (ent is self.p and (e.enemy or e.powerup)) or (ent.enemy and e is self.p):
                    if e.powerup:
                        self.e.remove(e)
                        e.collect(ent)
                        powerup.play()
                    pass
                else:
                    return False
        if self.o[x][y]:
            return False
        return self.inworld(x, y) and self.t[x][y]
    def get_tile(self,x,y):
        return Tiles.tiles[self.t[x][y]-1]
    def get_ent(self,x,y):
        for e in self.e:
            if (e.x,e.y)==(x,y):
                return e
    def eoconvert(self, eo):
        if eo == 1:
            return Object.Block, "obj"
        elif eo in Tiles.eents.keys():
            return Tiles.eents[eo],"ent"
        elif eo==3:
            return None,"spawn"
        elif eo==6:
            return Object.Indest, "obj"

    def create_exp(self, fx, fy, r):
        self.explode(fx, fy)
        for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            x, y = fx + dx, fy + dy
            for n in range(r):
                if self.explode(x, y):
                    break
                x += dx
                y += dy

    def explode(self, x, y):
        if self.inworld(x, y):
            if self.o[x][y]:
                if self.o[x][y].destructible:
                    self.o[x][y] = None
                    self.e.append(Entities.Explosion(x, y))
                return True
            else:
                self.e.append(Entities.Explosion(x, y))
        else:
            return True
