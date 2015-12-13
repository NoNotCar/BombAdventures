__author__ = 'NoNotCar'
import Img, Entities, Tiles, Object, FX, pygame
from random import randint
import BattlePlayers

powerup = Img.sndget("powerup")
exp = Img.sndget("explode")


class World(object):
    pconv=[BattlePlayers.Player,BattlePlayers.FatPlayer,BattlePlayers.SmallPlayer,BattlePlayers.ThinPlayer]
    def __init__(self, level, players,controllers):
        self.done = False
        self.level = level
        self.exitcode="NORMAL"
        self.e = []
        self.ps=[]
        savfile = open(Img.np("lvls//battle//"+level), "r")
        self.t = []
        self.o = []
        self.fx = []
        self.bfx = []
        pn=0
        savr = savfile.readlines()
        for row in savr[:20]:
            self.t.append([int(s) for s in row.split()])
        for x, row in enumerate(savr[20:]):
            self.o.append([None] * 20)
            crow = [int(s) for s in row.split()]
            for y, n in enumerate(crow):
                if n:
                    eo = self.eoconvert(n)
                    if eo[1] == "obj":
                        self.o[x][y] = eo[0](x, y)
                    elif eo[1] == "ent":
                        self.e.append(eo[0](x, y))
                    elif eo[1] == "spawn":
                        self.ps.append(self.pconv[players[pn]](x, y, controllers[pn]))
                        self.e.append(self.ps[-1])
                        pn+=1
        savfile.close()
    def update(self, ev):
        for e in self.e[:]:
            if e.moving:
                e.mupdate(self)
            if e.invtime:
                e.invtime-=1
            e.update(self, ev)
        for e in self.e:
            e.rerect()
        dangers = [d.rect for d in self.e if d.denemy]
        for e in [e for e in self.e if not e.denemy and e.enemy and not e.invtime]:
            if e.rect.collidelist(dangers) != -1:
                if e.hp:
                    e.hp-=1
                    e.invtime=20
                else:
                    self.e.remove(e)
        for p in self.ps[:]:
            if p.rect.collidelist([e.rect for e in self.e if e.enemy]) != -1:
                self.ps.remove(p)
                self.e.remove(p)
        for row in self.o:
            for o in row:
                if o:
                    o.update(self)
        for fx in self.fx[:]:
            fx.update(self)
            if fx.dead:
                self.fx.remove(fx)
        for fx in self.bfx[:]:
            fx.update(self)
            if fx.dead:
                self.bfx.remove(fx)
        for x, r in enumerate(self.t):
            for y, t in enumerate(r):
                if t:
                    Tiles.tiles[t-1].update(self,x,y)
    def render(self, s):
        for fx in self.bfx:
            s.blit(fx.img, (fx.x, fx.y))
        for x, r in enumerate(self.t):
            for y, t in enumerate(r):
                if t:
                    s.blit(Tiles.tiles[t - 1].img, (x * 32, y * 32))
        for e in self.e:
            s.blit(e.get_img(), (e.x * 32 + e.xoff, e.y * 32 + e.yoff))
        for x, r in enumerate(self.o):
            for y, o in enumerate(r):
                if o:
                    s.blit(o.get_img(), (x * 32, y * 32 - 8 * o.is3d))
        for fx in self.fx:
            s.blit(fx.img, (fx.x, fx.y))

    def inworld(self, x, y):
        return 0 <= x < 20 and 0 <= y < 20

    def is_clear(self, x, y, ent=None):
        if not self.inworld(x,y):
            return False
        for e in self.e:
            if e.x == x and e.y == y:
                if ent and ((ent in self.ps and (e.enemy or e.powerup)) or (ent.enemy and e in self.ps)):
                    if e.powerup:
                        self.e.remove(e)
                        e.collect(ent)
                        powerup.play()
                    pass
                else:
                    return False
        if self.o[x][y]:
            return False
        return self.t[x][y]

    def get_tile(self, x, y):
        return Tiles.tiles[self.t[x][y] - 1]

    def get_t(self, x, y):
        return self.t[x][y]

    def get_ent(self, x, y):
        for e in self.e:
            if (e.x, e.y) == (x, y):
                return e

    def eoconvert(self, eo):
        if eo == 1:
            return Object.Block, "obj"
        elif eo in Tiles.eents.keys():
            return Tiles.eents[eo], "ent"
        elif eo == 3:
            return BattlePlayers.Player, "spawn"
        elif eo == 6:
            return Object.Indest, "obj"
        elif eo == 9:
            return Object.SokoLock, "obj"
        elif eo == 10:
            return Object.ExplosiveBlock, "obj"
        elif eo == 13:
            return Object.GhostSpawner,"obj"
        elif eo == 15:
            return Object.CannonBlock,"obj"
        elif eo == 16:
            return BattlePlayers.SmallPlayer, "spawn"
        elif eo == 17:
            return BattlePlayers.FatPlayer, "spawn"
        elif eo == 18:
            return BattlePlayers.ThinPlayer, "spawn"

    def create_exp(self, fx, fy, r, p=False):
        exp.play()
        self.explode(fx, fy,p)
        for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
            x, y = fx + dx, fy + dy
            for n in range(r):
                if self.explode(x, y, p):
                    break
                x += dx
                y += dy

    def explode(self, x, y, p):
        if self.inworld(x, y):
            if self.o[x][y]:
                if self.o[x][y].destructible:
                    self.o[x][y] = None
                    self.e.append(Entities.Explosion(x, y, p))
                else:
                    self.o[x][y].explode(self)
                    return True
                if not p:
                    return True
            else:
                self.e.append(Entities.Explosion(x, y, p))
                gent=self.get_ent(x,y)
                if gent and gent.name=="Bomb":
                    gent.timer=1
        else:
            return True

    def get_p(self,x,y):
        if len(self.ps)==1:
            return self.ps[0]
        scores=[]
        for p in self.ps:
            scores.append((p, abs(p.x-x)+abs(p.y-y)))
        minscore=min([x[1] for x in scores])
        for p, s in scores:
            if s == minscore:
                return p
        return self.ps[0]
    def get_activeplayer(self):
        return [p for p in self.ps if p.akey==self.akey][0]
