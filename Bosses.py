from Entities import *
import FX
import Img
missile=Img.sndget("Expmiss")
def bombattack(world,ssize):
    while True:
        tx=randint(9-ssize,9+ssize)
        ty=randint(9-ssize,9+ssize)
        if world.is_clear(tx,ty):
            bomb=Bomb(tx,ty,2)
            bomb.timer=60
            world.e.append(bomb)
            break
def missileattack(world,ssize):
    while True:
        tx=randint(9-ssize,9+ssize)
        ty=randint(9-ssize,9+ssize)
        if world.is_clear(tx,ty):
            m=FX.Missile(tx*32,-48-(19-ty)*32,ty*32)
            world.fx.append(m)
            world.fx.append(FX.MissileTarget(tx*32,ty*32,m))
            missile.play()
            break
class BGhost(Ghost):
    imgs = imgstrip("BossGhost1")
    aimgs = imgstrip("BossGhost2")
    img = imgs[0]
    hp = 5
    invoverride = 320
    def update(self, world, events):
        if self.anitick == 31:
            self.anitick = 0
            if not self.invtime:
                p = world.get_p(self.x, self.y)
                if p.x < self.x:
                    self.move(-1, 0, 1, world)
                elif p.x > self.x:
                    self.move(1, 0, 1, world)
                elif p.y > self.y:
                    self.move(0, 1, 1, world)
                elif p.y < self.y:
                    self.move(0, -1, 1, world)
            elif self.invtime>=60:
                self.invoverride=320+(5-self.hp)*120
                for x in range((self.hp==0)+1):
                    bombattack(world,5)
                    if randint(0,1):
                        break

        else:
            self.anitick += 1
        if self.invtime:
            self.img = self.aimgs[(self.anitick // 4) % 4]
        else:
            self.img = self.imgs[self.anitick // 8]
class FBGhost(Ghost):
    imgs = imgstrip("FastBossGhost")
    aimgs=imgstrip("FastBossGhostAngry")
    img = imgs[0]
    anitick = 0
    orect = pygame.Rect(8, 14, 16, 12)
    hp=5

    def update(self, world, events):
        if self.anitick >= (11 if self.hp>0 else 7):
            self.anitick = 0
            s=3 if self.hp>0 else 4
            p = world.get_p(self.x, self.y)
            if p.x < self.x:
                self.move(-1, 0, s, world)
            elif p.x > self.x:
                self.move(1, 0, s, world)
            elif p.y > self.y:
                self.move(0, 1, s, world)
            elif p.y < self.y:
                self.move(0, -1, s, world)

        else:
            self.anitick += 1
        if self.hp>0:
            self.img = self.imgs[self.anitick // 3]
        else:
            self.img = self.aimgs[self.anitick // 2]
class DarkCore(Entity):
    imgs = imgstrip("DarkCore1")
    aimgs= imgstrip("DarkCore2")
    img = imgs[0]
    anitick = 0
    orect = pygame.Rect(2, 2, 28, 28)
    hp = 5
    invoverride = 31
    minions=[]
    def update(self, world, events):
        if self.anitick == 31:
            self.anitick = 0
        else:
            self.anitick += 1
        if self.invtime==10:
            self.invtime=2
            for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                tx,ty=self.x+dx,self.y+dy
                if world.is_clear(tx,ty):
                    ghost=FGhost(self.x,self.y)
                    world.e.append(ghost)
                    ghost.move(dx,dy,2,world,True)
                    self.minions.append(ghost)
        elif self.invtime==1:
            if any([m in world.e for m in self.minions]):
                self.invtime=2
                if self.hp==0 and self.anitick==0:
                    bombattack(world,5)
            else:
                self.minions=[]
        if self.invtime:
            self.img = self.aimgs[self.anitick // 4]
        else:
            self.img = self.imgs[self.anitick // 4]
class DarkCoreX(DarkCore):
    hp = 5
    invoverride = 2
    attacking=False
    attacks=[]
    aleft=0
    atime=0
    minions=[]
    def update(self, world, events):
        if self.anitick == 31:
            self.anitick = 0
        else:
            self.anitick += 1
        if self.invtime==1:
            self.invtime=2
            if not self.attacking:
                self.attacking=True
                self.attacks=["r","g","r"] if self.hp>=2 else ["b","g","r","g","b"]
                self.aleft={"r":2,"g":1,"b":randint(10,20)}[self.attacks[0]]
            a=self.attacks[0]
            if self.aleft==0 and not any([m in world.e for m in self.minions]):
                del self.attacks[0]
                if not self.attacks:
                    self.invtime=0
                    self.attacking=False
                else:
                    a=self.attacks[0]
                    self.aleft={"r":2,"g":1,"b":randint(10,20)}[a]
            elif self.atime==0 and not any([m in world.e for m in self.minions]):
                self.aleft-=1
                if a=="r":
                    missileattack(world,8)
                    self.atime=120
                elif a=="g":
                    for dx, dy in [[0, 1], [1, 0], [0, -1], [-1, 0]]:
                        tx,ty=self.x+dx,self.y+dy
                        if world.is_clear(tx,ty):
                            ghost=FGhost(self.x,self.y)
                            world.e.append(ghost)
                            ghost.move(dx,dy,2,world,True)
                            self.minions.append(ghost)
                elif a=="b":
                    bombattack(world,8)
                    self.atime=20
            elif self.atime:
                self.atime-=1
        if self.invtime:
            self.img = self.aimgs[self.anitick // 4]
        else:
            self.img = self.imgs[self.anitick // 4]
class BigSlime(Entity):
    anitick = 0
    imgs = imgstrip2("BigSlime")
    orect = pygame.Rect(12, 20, 40, 28)
    hp=3
    initing=True
    tplocs=[(1,19),(16,2),(17,19)]
    def update(self, world, events):
        if self.initing:
            self.initing=False
            world.e.append(Multi(self.x+1,self.y,self))
            world.e.append(Multi(self.x+1,self.y+1,self))
            world.e.append(Multi(self.x,self.y+1,self))
        if self.anitick < 31:
            self.anitick += 1
        else:
            self.anitick = 0
        if self.invtime==19:
            world.fx.append(FX.TPFX(world.ps[0].x*32,world.ps[0].y*32))
            world.ps[0].place(*self.tplocs[2-self.hp])
    def get_img(self):
        return self.imgs[self.anitick // 8]
class NomSnakeHead(Entity):
    imgs = imgstrip2("NomStrip")
    img = imgs[0]
    anitick=0
    hp = 10
    dx=-1
    dy=0
    init=True
    def update(self, world, events):
        if self.init:
            for x in range(10):
                seg=NomSnakeSeg(self.x+x,self.y,self)
                world.e.append(seg)
                if x==0:
                    self.fseg=seg
                seg.move(self.dx,self.dy,2,world,True)
            self.move(self.dx,self.dy,2,world,True)
            self.init=False
        if self.anitick == 15:
            self.anitick = 0
            if not self.move(self.dx,self.dy,2,world):
                pass
            elif self.invtime>=60:
                self.invoverride=320+(5-self.hp)*120
                for x in range((self.hp==0)+1):
                    missileattack(world,5)
                    if randint(0,1):
                        break

        else:
            self.anitick += 1
        if self.invtime:
            self.img = self.aimgs[(self.anitick // 4) % 4]
        else:
            self.img = self.imgs[self.anitick // 8]
class Multi(Entity):
    hidden = True
    def __init__(self, x, y, p):
        self.x = x
        self.y = y
        self.p = p
        self.hp=p.hp
    def update(self,world,events):
        if self.hp>self.p.hp:
            self.hp=self.p.hp
            self.invtime=self.p.invtime
        elif self.hp<self.p.hp:
            self.p.hp=self.hp
            self.p.invtime=self.p.invoverride
            self.invtime=self.p.invoverride
class NomSnakeSeg(Multi):
    hidden = False
    img=img2("NomSeg")
bosses=[BGhost,FBGhost,DarkCore,BigSlime,DarkCoreX]