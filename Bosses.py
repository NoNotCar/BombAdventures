from Entities import *
import FX
import Img
import Object
missile=Img.sndget("Expmiss")
laugh=Img.sndget("bosslaugh")
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

class BlockBot(Object.Object):
    tick=0
    hp=5
    inv=0
    img=img2("BossBlock")
    imga=img2("BossBlockWhite")
    dx=-1
    dy=0
    destructible=False
    missilecooldown=0
    stuck=False
    def update(self,world):
        if self.tick>=self.hp*5+10:
            self.tick=0
            if randint(0,4) and self.clear(self.dx+self.x,self.dy+self.y,world):
                self.move(self.dx,self.dy,world)
            else:
                dirs=[[0,1],[1,0],[0,-1],[-1,0]]
                shuffle(dirs)
                for dx,dy in dirs:
                    if self.clear(self.x+dx,self.y+dy,world):
                        self.move(dx,dy,world)
                        break
                else:
                    self.stuck=True
        else:
            self.tick+=1
        if self.inv:
            self.inv-=1
        if self.stuck:
            if self.missilecooldown==0:
                missileattack(world,9)
                self.missilecooldown=120 if self.hp else 60
        if self.missilecooldown:
            self.missilecooldown-=1
    def get_img(self):
        if self.stuck or not self.hp:
            return self.img if (self.tick//2)%2 else self.imga
        return self.img
    def move(self,dx,dy,world):
        self.stuck=False
        tx=self.x+dx
        ty=self.y+dy
        if world.get_ent(tx,ty) in world.ps:
            world.e.remove(world.get_ent(tx,ty))
            world.playerdead=True
        world.o[tx][ty]=self
        world.o[self.x][self.y]=(Object.Block if randint(self.hp,20)>5 else Object.ExplosiveBlock)(self.x,self.y)
        self.x=tx
        self.y=ty
    def clear(self,tx,ty,world):
        if world.inworld(tx,ty) and world.get_t(tx,ty) and not world.o[tx][ty]:
            gent=world.get_ent(tx,ty)
            if gent is None or gent in world.ps:
                return True
    def explode(self,world):
        if not self.inv:
            self.hp-=1
            if self.hp==-1:
                world.o[self.x][self.y]=None
            else:
                self.inv=30
class DarkMonster(DarkCoreX):
    hp = 4
    imgs=imgstrip2("DarkMonster")
    aimgs = imgstrip2("DarkMonsterAng")
    initing=True
    darkresist = True
    invoverride = 20
    def update(self, world, events):
        if self.initing:
            self.initing=False
            for x in range(3):
                for y in range(3):
                    if (x,y)!=(0,0):
                        world.e.append(Multi(self.x+x,self.y+y,self))
        if self.anitick == 31:
            self.anitick = 0
        else:
            self.anitick += 1
        if self.invtime==1:
            self.invtime=2
            if not self.attacking:
                self.attacking=True
                self.attacks=["f","r","g","f"] if self.hp>=2 else ["fh","b","g","r","g","b","f"]
                self.aleft={"r":2,"g":1,"b":randint(10,20),"f":randint(180,360),"fh":randint(20,30)}[self.attacks[0]]
            a=self.attacks[0]
            if self.aleft==0 and not any([m in world.e for m in self.minions]):
                del self.attacks[0]
                if not self.attacks:
                    self.invtime=0
                    self.attacking=False
                else:
                    a=self.attacks[0]
                    self.aleft={"r":2,"g":1,"b":randint(10,20),"f":randint(180,360),"fh":randint(20,30)}[a]
            elif self.atime==0 and not any([m in world.e for m in self.minions]):
                self.aleft-=1
                if a=="r":
                    missileattack(world,8)
                    self.atime=120
                elif a=="f":
                    world.e.append(Fireball(10,10,math.radians(self.aleft*4),4))
                elif a=="fh":
                    world.e.append(HomingFireball(10,10,self.aleft,3))
                    self.atime=30
                elif a=="g":
                    for dx, dy in [[0, -1],[1,-1],[2,-1], [3, 0],[3,1],[3,2], [0, 3],[1,3],[2,3], [-1, 0],[-1,1],[-1,2]]:
                        tx,ty=self.x+dx,self.y+dy
                        if world.is_clear(tx,ty):
                            ghost=FGhost(self.x+1,self.y+1)
                            world.e.append(ghost)
                            ghost.move(dx-1,dy-1,2,world,True)
                            self.minions.append(ghost)
                elif a=="b":
                    bombattack(world,8)
                    self.atime=20
            elif self.atime:
                self.atime-=1
        if self.invtime:
            self.img = self.aimgs[self.anitick // 2 % 8]
        else:
            self.img = self.imgs[self.anitick // 4]
class DarkPlayer(Player):
    hidden = True
    solid=False
    enemy = False
    bombs = 1
    rng = 2
    pen = True
    dy = 1
    hp=5
    iconv = {(0, -1): img2("Men/ManBu"), (0, 1): img2("Men/ManB"), (1, 0): img2("Men/ManBr"),
             (-1, 0): img2("Men/ManBl")}
    ms = 2
    rd = False
    detonate = False
    activate=False

    def update(self, world, events):
        if self.activate:
            self.activate=False
        if self.hidden:
            if (world.ps[0].x,world.ps[0].y)==(self.x,self.y) and not world.ps[0].moving:
                world.done=False
                world.e.remove(world.ps[0])
                del world.ps[0]
                np=Player(9,2)
                np.hidden=True
                world.ps.append(np)
                world.e.append(np)
                self.hidden=False
                self.solid=True
                world.t[self.x][self.y]=1
                self.enemy=True
                self.activate=True
                laugh.play()
        else:
            if not randint(0,1000):
                laugh.play()
            if not self.moving:
                if world.indanger(self.x,self.y):
                    dirs=[[0,1],[1,0],[0,-1],[-1,0]]
                    shuffle(dirs)
                    for dx,dy in dirs:
                        if self.move(dx,dy,2,world):
                            break
                elif self.bombs:
                    if randint(0,2):
                        dirs=[[0,1],[1,0],[0,-1],[-1,0]]
                        shuffle(dirs)
                        for dx,dy in dirs:
                            if not world.indanger(self.x+dx,self.y+dy) and self.move(dx,dy,2,world):
                                break
                    else:
                        world.e.append(Bomb(self.x,self.y,6-self.hp,self))
                        self.bombs-=1


    def get_img(self):
        return self.iconv[(self.dx, self.dy)]
class Multi(Entity):
    hidden = True
    darkresist = True
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
        if self.invtime<self.p.invtime:
            self.invtime=self.p.invtime
bosses=[BGhost,FBGhost,DarkCore,BigSlime,DarkCoreX,BlockBot,DarkMonster,DarkPlayer]