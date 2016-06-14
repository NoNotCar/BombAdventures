__author__ = 'NoNotCar'
import Img, Entities, Tiles, Object, FX, pygame, Bosses
from random import randint

powerup = Img.sndget("powerup")
exp = Img.sndget("explode")


class World(object):
    rumbling=0
    rtime=0
    boss=None
    def __init__(self, edit, level=None):
        self.edit = edit
        self.playerdead = False
        self.done = False
        self.level = level
        self.exitcode="NORMAL"
        if edit:
            self.t = []
            self.o = []
            for _ in range(20):
                self.t.append([0] * 20)
                self.o.append([0] * 20)
            self.e = []
        else:
            self.e = []
            self.ps=[]
            if level=="sav":
                savfile = open(Img.np("lvls//save.sav"), "r")
            elif len(level)==2:
                savfile = open(Img.np("lvls//%s-%s.sav" % tuple(level)), "r")
            else:
                savfile = open(Img.np("lvls//%s-%s-%s.sav" % tuple(level)), "r")
            self.t = []
            self.o = []
            self.fx = []
            self.bfx = []
            if level[0]==3 and level[1]!=8:
                for _ in range(randint(50,60)):
                    self.bfx.append(FX.Star(randint(0,638),randint(0,638)))
            savr = savfile.readlines()
            self.fltext = savr[0][:-1]
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
                            self.o[x][y] = eo[0](x, y)
                        elif eo[1] == "ent":
                            self.e.append(eo[0](x, y))
                        elif eo[1] == "spawn":
                            self.ps.append(eo[0](x, y))
                            self.e.append(self.ps[-1])
                            self.akey=self.ps[-1].akey
                        elif eo[1] == "gravblock":
                            self.e.append(Entities.SokoBlokGrav(x,y,eo[0]))
            if level[1]==8:
                try:
                    self.boss=Bosses.bosses[level[0]-1](9,9)
                    self.e.append(self.boss)
                except IndexError:
                    pass
            savfile.close()
    def update(self, ev):
        for e in ev:
            if e.type==pygame.KEYDOWN:
                if e.key in [pygame.K_UP, pygame.K_DOWN,pygame.K_LEFT,pygame.K_RIGHT]:
                    if e.key in [p.akey for p in self.ps]:
                        self.akey=e.key
        if self.level[0] in [2,6] and not randint(0, 3):
            self.fx.append(FX.Snow(randint(0, 628), -12))
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
                    e.invtime=e.invoverride
                else:
                    self.e.remove(e)
                    if e is self.boss:
                        self.done=60
        for p in self.ps:
            if p.rect.collidelist([e.rect for e in self.e if e.enemy]) != -1:
                self.playerdead = True
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
        if self.rtime>0:
            self.rtime-=1
            if self.rtime==0 and self.rumbling>0:
                self.rumbling-=1
                if self.rumbling>0:
                    self.rtime=10
    def render(self, s):
        rx=randint(-self.rumbling,self.rumbling)
        ry=randint(-self.rumbling,self.rumbling)
        if self.rumbling==10 and not randint(0,5):
            s.fill((255,255,255))
        else:
            if not self.edit:
                for fx in self.bfx:
                    s.blit(fx.img, (fx.x+rx, fx.y+ry))
            for x, r in enumerate(self.t):
                for y, t in enumerate(r):
                    if t:
                        s.blit(Tiles.tiles[t - 1].img, (x * 32+rx, y * 32+ry))
            for e in self.e:
                if not e.hidden:
                    s.blit(e.get_img(), (e.x * 32 + e.xoff+ rx, e.y * 32 + e.yoff+ry))
            if self.edit:
                for x, r in enumerate(self.o):
                    for y, o in enumerate(r):
                        if o:
                            s.blit(Tiles.eobjs[o - 1][0], (x * 32+rx, y * 32 - Tiles.eobjs[o - 1][1] * 8+ry))
            else:
                for x, r in enumerate(self.o):
                    for y, o in enumerate(r):
                        if o:
                            s.blit(o.get_img(), (x * 32+rx, y * 32 - 8 * o.is3d+ry))
                for fx in self.fx:
                    s.blit(fx.img, (fx.x+rx, fx.y+ry))

    def save(self):
        savfile = open("lvls//save.sav", "w")
        savfile.write("\n")
        for row in self.t:
            savfile.write(" ".join([str(t) for t in row]) + "\n")
        for row in self.o:
            savfile.write(" ".join([str(t) for t in row]) + "\n")
        savfile.close()

    def inworld(self, x, y):
        return 0 <= x < 20 and 0 <= y < 20

    def is_clear(self, x, y, ent=None):
        if not self.inworld(x,y):
            return False
        for e in self.e:
            if e.solid and e.x == x and e.y == y:
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
    def get_ents(self,x,y):
        ents=[]
        for e in self.e:
            if (e.x, e.y) == (x, y):
                ents.append(e)
        return ents
    def eoconvert(self, eo):
        if eo == 1:
            return Object.Block, "obj"
        elif eo in Tiles.eents.keys():
            return Tiles.eents[eo], "ent"
        elif eo == 3:
            return Entities.Player, "spawn"
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
            return Entities.SmallPlayer, "spawn"
        elif eo == 17:
            return Entities.FatPlayer, "spawn"
        elif eo == 18:
            return Entities.ThinPlayer, "spawn"
        elif 22<eo<=26:
            return eo-23, "gravblock"

    def create_exp(self, fx, fy, r, p=False):
        self.rtime=10
        self.rumbling+=r*(p+1)
        if self.rumbling>10:
            self.rumbling=10
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
