__author__ = 'NoNotCar'
from Img import img2, img32, imgstrip, imgstrip2
from random import choice, randint, shuffle
import pygame, math

pi=math.pi
tau=2*pi
right=pi/2

def iround(fl):
    return int(round(fl))


class Path(object):
    def __init__(self, path):
        self.path = path

    def get_score(self, end):
        return len(self.path) + abs(self.path[-1][0] - end[0]) + abs(self.path[-1][1] - end[1])

    def extend(self, paths, world):
        for dire in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            tx, ty = self.path[-1][0] + dire[0], self.path[-1][1] + dire[1]
            gpaths = []
            for path in paths:
                gpaths.extend(path.path)
            if world.is_clear(tx, ty) and (tx, ty) not in gpaths:
                paths.append(Path(self.path + [(tx, ty)]))
        paths.remove(self)

    def next(self):
        dx, dy = self.path[1][0] - self.path[0][0], self.path[1][1] - self.path[0][1]
        self.path.pop(0)
        return dx, dy


class Entity(object):
    # Anything that can move
    solid = True
    name = "Entity"
    hidden = False
    xoff = 0
    yoff = 0
    speed = 0
    moving = False
    pathfollowing = False
    path = None
    img = None
    enemy = True
    orect = pygame.Rect(0, 0, 32, 32)
    denemy = False
    powerup = False
    pushable = False
    dx = 0
    dy = 0
    ignore = False
    sticky = False
    darkresist = False
    hp = 0
    invtime = 0
    invoverride=20

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_img(self):
        return self.img

    def update(self, world, events):
        pass

    def mupdate(self, world):
        if self.xoff > 0:
            self.xoff -= self.speed
        elif self.xoff < 0:
            self.xoff += self.speed
        if self.yoff > 0:
            self.yoff -= self.speed
        elif self.yoff < 0:
            self.yoff += self.speed
        if abs(self.xoff) < self.speed and abs(self.yoff) < self.speed and self.moving:
            self.xoff = 0
            self.yoff = 0
            self.moving = False
            if not (self.ignore or self.sticky) and world.get_tile(self.x, self.y).slippery:
                self.move(self.dx, self.dy, self.speed, world)
                self.pathfollowing = False
            if self.pathfollowing:
                if len(self.path.path) > 1:
                    dx, dy = self.path.next()
                    if not self.move(dx, dy, self.speed, world):
                        self.pathfollowing = False
                        self.path = None
                else:
                    self.pathfollowing = False
                    self.path = None

    def rerect(self):
        self.rect = pygame.Rect(self.x * 32 + self.xoff + self.orect.left, self.y * 32 + self.yoff + self.orect.top,
                                self.orect.width, self.orect.height)

    def pathfind(self, end, world):
        if end == (self.x, self.y):
            return True
        else:
            paths = [Path([(self.x, self.y)])]
            while not len([p for p in paths if p.path[-1] == end]):
                if len(paths) == 0:
                    return False
                bpaths = []
                bscore = None
                for path in paths:
                    if bscore is None:
                        bscore = path.get_score(end)
                        bpaths.append(path)
                    elif bscore > path.get_score(end):
                        bscore = path.get_score(end)
                        bpaths = [path]
                    elif bscore == path.get_score(end):
                        bpaths.append(path)
                if len(bpaths) != 1:
                    blen = max([len(b.path) for b in bpaths])
                    bpath = choice([bp for bp in bpaths if len(bp.path) == blen])
                else:
                    bpath = bpaths[0]
                bpath.extend(paths, world)
            self.pathfollowing = True
            self.path = [p for p in paths if p.path[-1] == end][0]
            dx, dy = self.path.next()
            self.move(dx, dy, self.speed, world, True, False)

    def move(self, dx, dy, s, world, ignoreobs=False):
        self.ignore = ignoreobs
        if not self.moving:
            tx = self.x + dx
            ty = self.y + dy
            if ignoreobs or world.is_clear(tx, ty, self):
                self.x = tx
                self.y = ty
                self.moving = True
                self.speed = s
                self.xoff = -dx * 32
                self.yoff = -dy * 32
                self.dx = dx
                self.dy = dy
                return True
            elif self in world.ps:
                pent = world.get_ent(tx, ty)
                if pent and pent.pushable and pent.move(dx, dy, s, world):
                    self.x = tx
                    self.y = ty
                    self.moving = True
                    self.speed = s
                    self.xoff = -dx * 32
                    self.yoff = -dy * 32
                    self.dx = dx
                    self.dy = dy
                    return True

    def place(self, x, y):
        self.x = x
        self.y = y
        self.xoff=0
        self.yoff=0
        self.moving=False

    def aplace(self, ax, ay):
        self.x = int(ax // 32)
        self.y = int(ay // 32)
        self.xoff = int(round(ax % 32))
        self.yoff = int(round(ay % 32))
        if self.xoff >= 16:
            self.xoff-=32
            self.x += 1
        if self.yoff >= 16:
            self.yoff-=32
            self.y += 1


class Player(Entity):
    orect = pygame.Rect(10, 2, 12, 28)
    kconv = {pygame.K_w: (0, -1), pygame.K_s: (0, 1), pygame.K_a: (-1, 0), pygame.K_d: (1, 0)}
    enemy = False
    bombs = 1
    rng = 2
    pen = False
    dy = 1
    iconv = {(0, -1): img2("Men/Man2u"), (0, 1): img2("Men/Man2"), (1, 0): img2("Men/Man2r"),
             (-1, 0): img2("Men/Man2l")}
    ms = 2
    akey = pygame.K_UP
    rd = False
    detonate = False

    def update(self, world, events):
        if self.detonate:
            self.detonate = False
        if world.akey == self.akey:
            keys = pygame.key.get_pressed()
            for k, v in self.kconv.iteritems():
                if keys[k] and self.move(v[0], v[1], self.ms, world):
                    break
            for e in events:
                if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and self.bombs:
                    for e in world.get_ents(self.x,self.y):
                        if e.name=="Bomb":
                            break
                    else:
                        world.e.append(
                            Bomb(iround((self.x * 32 + self.xoff) / 32.0), iround((self.y * 32 + self.yoff) / 32.0),
                                 self.rng,
                                 self))
                        self.bombs -= 1
                elif e.type == pygame.KEYDOWN and e.key == pygame.K_LSHIFT and self.rd:
                    self.detonate = True
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
    iconv = {(0, -1): img2("Men/SManu"), (0, 1): img2("Men/SMan"), (1, 0): img2("Men/SManr"),
             (-1, 0): img2("Men/SManl")}
    akey = pygame.K_DOWN


class FatPlayer(Player):
    orect = pygame.Rect(8, 2, 16, 28)
    rng = 2
    bombs = 2
    ms = 1.5
    pen = True
    sticky = True
    akey = pygame.K_LEFT
    iconv = {(0, -1): img2("Men/FManu"), (0, 1): img2("Men/FMan"), (1, 0): img2("Men/FManr"),
             (-1, 0): img2("Men/FManl")}


class ThinPlayer(Player):
    orect = pygame.Rect(12, 2, 8, 28)
    rng = 3
    rd = True
    akey = pygame.K_RIGHT
    iconv = {(0, -1): img2("Men/TManu"), (0, 1): img2("Men/TMan"), (1, 0): img2("Men/TManr"),
             (-1, 0): img2("Men/TManl")}


class Ghost(Entity):
    imgs = imgstrip("Ghost")
    img = imgs[0]
    anitick = 0
    orect = pygame.Rect(8, 14, 16, 12)

    def update(self, world, events):
        if self.anitick == 31:
            self.anitick = 0
            p = world.get_p(self.x, self.y)
            if p.x < self.x:
                self.move(-1, 0, 1, world)
            elif p.x > self.x:
                self.move(1, 0, 1, world)
            elif p.y > self.y:
                self.move(0, 1, 1, world)
            elif p.y < self.y:
                self.move(0, -1, 1, world)

        else:
            self.anitick += 1
        self.img = self.imgs[self.anitick // 8]


class FGhost(Entity):
    imgs = imgstrip("FGhost")
    img = imgs[0]
    anitick = 0
    orect = pygame.Rect(8, 14, 16, 12)

    def update(self, world, events):
        if self.anitick == 15:
            self.anitick = 0
            p = world.get_p(self.x, self.y)
            if p.x < self.x:
                self.move(-1, 0, 2, world)
            elif p.x > self.x:
                self.move(1, 0, 2, world)
            elif p.y > self.y:
                self.move(0, 1, 2, world)
            elif p.y < self.y:
                self.move(0, -1, 2, world)

        else:
            self.anitick += 1
        self.img = self.imgs[self.anitick // 4]


class TGhost(Ghost):
    timgs = imgstrip("TGhost")
    img = timgs[0]
    hp = 1

    def update(self, world, events):
        if self.anitick == 31:
            self.anitick = 0
            p = world.get_p(self.x, self.y)
            if p.x < self.x:
                self.move(-1, 0, 1, world)
            elif p.x > self.x:
                self.move(1, 0, 1, world)
            elif p.y > self.y:
                self.move(0, 1, 1, world)
            elif p.y < self.y:
                self.move(0, -1, 1, world)

        else:
            self.anitick += 1
        if self.hp:
            self.img = self.timgs[self.anitick // 8]
        else:
            self.img = self.imgs[self.anitick // 8]

class FireGhost(Ghost):
    imgs=imgstrip("FireGhost")
    img=imgs[0]
    fspawn=True
    def update(self, world, events):
        if self.fspawn:
            world.e.append(OrbitFireball(96,2,self))
            self.fspawn=False
        if self.anitick == 31:
            self.anitick = 0
            p = world.get_p(self.x, self.y)
            if p.x < self.x:
                self.move(-1, 0, 1, world)
            elif p.x > self.x:
                self.move(1, 0, 1, world)
            elif p.y > self.y:
                self.move(0, 1, 1, world)
            elif p.y < self.y:
                self.move(0, -1, 1, world)

        else:
            self.anitick += 1
        self.img = self.imgs[self.anitick // 8]

class Thud(Entity):
    imgs = imgstrip2("Thud")
    img = imgs[0]
    orect = pygame.Rect(8, 8, 16, 16)
    motion = [0, 0]

    def update(self, world, events):
        if self.motion != [0, 0]:
            if not self.moving and not self.move(self.motion[0], self.motion[1], 4, world):
                self.motion = [0, 0]
                self.img = self.imgs[0]
            else:
                self.img = self.imgs[1]
        else:
            p = world.get_p(self.x, self.y)
            if p.x == self.x:
                if p.y < self.y:
                    self.motion = [0, -1]
                else:
                    self.motion = [0, 1]
            elif p.y == self.y:
                if p.x < self.x:
                    self.motion = [-1, 0]
                else:
                    self.motion = [1, 0]


class Explosion(Entity):
    img = img2("Exp")
    pimg = img2("ExpPen")
    orect = pygame.Rect(6, 6, 20, 20)
    life = 20
    denemy = True
    darkresist = True

    def __init__(self, x, y, pen):
        self.place(x, y)
        self.pen = pen

    def update(self, world, events):
        self.xoff = randint(-1, 1)
        self.yoff = randint(-1, 1)
        self.life -= 1
        if self.life == 0:
            world.e.remove(self)

    def get_img(self):
        return self.pimg if self.pen else self.img


class Bomb(Entity):
    enemy = False
    timer = 120
    img = img2("Bomb")
    darkresist = True
    name = "Bomb"

    def __init__(self, x, y, r, p=False):
        self.x = x
        self.y = y
        self.p = p
        self.r = r
        self.pen = p and p.pen
        self.rd = p and p.rd

    def update(self, world, events):
        if self.rd:
            if self.p.detonate or self.timer == 1:
                world.create_exp(self.x, self.y, self.r, self.pen)
                world.e.remove(self)
                self.p.bombs += 1
        else:
            self.timer -= 1
            if self.timer == 0:
                world.create_exp(self.x, self.y, self.r, self.pen)
                world.e.remove(self)
                if self.p:
                    self.p.bombs += 1
            elif self.timer <= 30:
                self.xoff = randint(-2, 2)
                self.yoff = randint(-2, 2)


class RangeUp(Entity):
    enemy = False
    img = img32("RangeUp")
    powerup = True

    def collect(self, p):
        p.rng += 1


class Penetrating(Entity):
    enemy = False
    img = img2("Pen")
    powerup = True

    def collect(self, p):
        p.pen = True


class BombPlus(Entity):
    enemy = False
    img = img2("ExBomb")
    powerup = True

    def collect(self, p):
        p.bombs += 1


class NullPower(Entity):
    enemy = False
    img = img2("Null")
    powerup = True

    def collect(self, p):
        p.bombs = 0
        p.rng = 0
        p.pen = False


class SokoBlock(Entity):
    enemy = False
    img = img2("SokoBlok")
    pushable = True
    name = "Sokoblock"

    def update(self, world, events):
        if not self.moving:
            if world.get_t(self.x, self.y) == 4:
                world.t[self.x][self.y] = 5
                world.e.remove(self)


class SokoBlokSlippy(SokoBlock):
    img = img2("SokoBlokIce")

    def update(self, world, events):
        if not self.moving:
            if world.get_t(self.x, self.y) == 4:
                world.t[self.x][self.y] = 5
                world.e.remove(self)
            if self.dx != 0 or self.dy != 0:
                if not self.move(self.dx, self.dy, self.speed, world):
                    self.dx = 0
                    self.dy = 0


class SokoBlockGoo(SokoBlock):
    img = img2("SokoBlokGoo")
    sticky = True


class SokoBlokGrav(SokoBlock):
    imgs = imgstrip2("GraviBlok")
    aimgs = imgstrip2("GraviBlokAct")

    def __init__(self, x, y, d):
        self.place(x, y)
        self.d = d
        self.gd = [(1, 0), (0, 1), (-1, 0), (0, -1)][d]
        self.gdx = self.gd[0]
        self.gdy = self.gd[1]

    def update(self, world, events):
        if not self.moving:
            if world.get_t(self.x, self.y) == 4:
                world.t[self.x][self.y] = 5
                world.e.remove(self)
            self.move(self.gdx, self.gdy, 2, world)

    def get_img(self):
        if self.moving and self.dx == self.gdx and self.dy == self.gdy:
            return self.aimgs[self.d]
        return self.imgs[self.d]


class Slime(Entity):
    anitick = 0
    imgs = imgstrip2("Slime")
    orect = pygame.Rect(6, 10, 20, 14)

    def update(self, world, events):
        if self.anitick < 31:
            self.anitick += 1
        else:
            self.anitick = 0
        if not self.moving:
            p = world.get_p(self.x, self.y)
            if self.x == p.x:
                self.move(0, 1 if self.y < p.y else -1, 2, world)
            elif self.y == p.y:
                self.move(1 if self.x < p.x else -1, 0, 2, world)
        if not self.moving:
            dirs = [[1, 0], [0, 1], [-1, 0], [0, -1]]
            shuffle(dirs)
            for dx, dy in dirs:
                if self.move(dx, dy, 0.5, world):
                    break

    def get_img(self):
        return self.imgs[self.anitick // 8 if self.speed == 0.5 else self.anitick // 4 % 4]


class CannonBall(Entity):
    img = img2("CannonBall")
    orect = pygame.Rect(10, 10, 12, 12)

    def __init__(self, x, y, dx):
        self.dx = dx
        self.place(x, y)
        self.js = True

    def update(self, world, events):
        if not self.moving:
            if not self.js and world.inworld(self.x, self.y) and world.o[self.x][self.y]:
                world.e.remove(self)
            elif world.inworld(self.x, self.y):
                self.move(self.dx, 0, 4, world, True)
            else:
                world.e.remove(self)
            if self.js:
                self.js = False


class Fireball(Entity):
    img = img2("Fireball")
    orect = pygame.Rect(10, 10, 12, 12)
    solid = False

    def __init__(self, x, y, ang, spd):
        self.place(x, y)
        self.ang = ang
        self.ax = x * 32
        self.ay = y * 32
        self.dx = spd * math.cos(ang)
        self.dy = spd * math.sin(ang)
        self.spd=spd

    def update(self, world, events):
        self.ax += self.dx
        self.ay += self.dy
        self.aplace(self.ax, self.ay)
        if not world.inworld(self.x, self.y) or world.o[self.x][self.y]:
            world.e.remove(self)
class HomingFireball(Fireball):
    img = img2("HFireball")
    def update(self, world, events):
        self.ax += self.dx
        self.ay += self.dy
        self.aplace(self.ax, self.ay)
        if not world.inworld(self.x, self.y) or world.o[self.x][self.y]:
            world.e.remove(self)
        np=world.get_p(self.x,self.y)
        tang=math.atan2(np.y*32 + np.yoff - self.y*32 - self.yoff, np.x*32 + np.xoff - self.x*32 - self.xoff)
        tdiff=math.fmod(tang-self.ang+pi,tau)-pi
        if right>tdiff>0:
            self.ang+=0.02
        elif 0>tdiff>-right:
            self.ang-=0.02
        self.dx = self.spd * math.cos(self.ang)
        self.dy = self.spd * math.sin(self.ang)

class OrbitFireball(Fireball):
    hp = -1
    def __init__(self, r, spd, ent):
        self.ent=ent
        self.ang = math.radians(randint(0,359))
        self.spd = math.radians(spd)
        self.r=r
        self.recalc()

    def update(self, world, events):
        if self.ent not in world.e:
            world.e.remove(self)
        else:
            self.recalc()
    def recalc(self):
        offx=self.ent.x*32+self.ent.xoff
        offy=self.ent.y*32+self.ent.yoff
        self.ang+=self.spd
        self.ang=self.ang%(2*pi)
        self.ax=self.r*math.cos(self.ang)+offx
        self.ay=self.r*math.sin(self.ang)+offy
        self.aplace(self.ax,self.ay)


class FireballLauncher(Entity):
    img = img2("FireballL1")
    aimg = img2("FireballL2")
    enemy = False
    fireballclass=Fireball
    speed = 3
    def __init__(self,x,y):
        self.place(x,y)
        self.tonext = randint(120, 240)

    def update(self, world, events):
        if self.tonext:
            self.tonext -= 1
        else:
            self.tonext = randint(120, 240)
            np = world.get_p(self.x, self.y)
            ang = math.atan2(np.y*32 + np.yoff - self.y*32 - self.yoff, np.x*32 + np.xoff - self.x*32 - self.xoff)
            world.e.append(self.fireballclass(self.x, self.y, ang, self.speed))

    def get_img(self):
        return self.img if self.tonext > 30 else self.aimg

class HFireballLauncher(FireballLauncher):
    fireballclass = HomingFireball
    aimg = img2("FireballL3")
