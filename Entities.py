__author__ = 'NoNotCar'
from Img import img2, img32, imgstrip, imgstrip2, loc, np
from random import choice, randint, shuffle
import pygame


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
    solid = False
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
    ignore=False

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
            if not self.ignore and world.get_tile(self.x, self.y).slippery:
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
        self.ignore=ignoreobs
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
            elif self is world.p:
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


class Player(Entity):
    orect = pygame.Rect(10, 2, 12, 28)
    kconv = {pygame.K_w: (0, -1), pygame.K_s: (0, 1), pygame.K_a: (-1, 0), pygame.K_d: (1, 0)}
    enemy = False
    bombs = 1
    rng = 2
    pen = False
    dy = 1
    iconv = {(0, -1): img2("Man2u"), (0, 1): img2("Man2"), (1, 0): img2("Man2r"), (-1, 0): img2("Man2l")}

    def update(self, world, events):
        keys = pygame.key.get_pressed()
        for k, v in self.kconv.iteritems():
            if keys[k] and self.move(v[0], v[1], 2, world):
                break
        for e in events:
            if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE and self.bombs:
                world.e.append(
                    Bomb(iround((self.x * 32 + self.xoff) / 32.0), iround((self.y * 32 + self.yoff) / 32.0), self.rng,
                         self))
                self.bombs -= 1
        if not self.moving:
            if world.t[self.x][self.y] == 2:
                world.done = True

    def get_img(self):
        return self.iconv[(self.dx, self.dy)]


class Ghost(Entity):
    imgs = imgstrip("Ghost")
    img = imgs[0]
    anitick = 0
    orect = pygame.Rect(8, 14, 16, 12)

    def update(self, world, events):
        if self.anitick == 31:
            self.anitick = 0
            if world.p.x < self.x:
                self.move(-1, 0, 1, world)
            elif world.p.x > self.x:
                self.move(1, 0, 1, world)
            elif world.p.y > self.y:
                self.move(0, 1, 1, world)
            elif world.p.y < self.y:
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
            if world.p.x < self.x:
                self.move(-1, 0, 2, world)
            elif world.p.x > self.x:
                self.move(1, 0, 2, world)
            elif world.p.y > self.y:
                self.move(0, 1, 2, world)
            elif world.p.y < self.y:
                self.move(0, -1, 2, world)

        else:
            self.anitick += 1
        self.img = self.imgs[self.anitick // 4]


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
            if world.p.x == self.x:
                if world.p.y < self.y:
                    self.motion = [0, -1]
                else:
                    self.motion = [0, 1]
            elif world.p.y == self.y:
                if world.p.x < self.x:
                    self.motion = [-1, 0]
                else:
                    self.motion = [1, 0]


class Explosion(Entity):
    img = img2("Exp")
    pimg=img2("ExpPen")
    orect = pygame.Rect(6, 6, 20, 20)
    life = 20
    denemy = True

    def __init__(self,x,y,pen):
        self.place(x,y)
        self.pen=pen
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

    def __init__(self, x, y, r, p=False):
        self.x = x
        self.y = y
        self.p = p
        self.r = r
        self.pen=p and p.pen

    def update(self, world, events):
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
        p.bombs+=1


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

class Slime(Entity):
    anitick=0
    imgs=imgstrip2("Slime")
    orect = pygame.Rect(6,10,20,14)
    def update(self, world, events):
        if self.anitick<31:
            self.anitick+=1
        else:
            self.anitick=0
        if not self.moving:
            if self.x==world.p.x:
                self.move(0,1 if self.y<world.p.y else -1, 2,world)
            elif self.y==world.p.y:
                self.move(1 if self.x<world.p.x else -1,0, 2,world)
        if not self.moving:
            dirs=[[1,0],[0,1],[-1,0],[0,-1]]
            shuffle(dirs)
            for dx,dy in dirs:
                if self.move(dx,dy,0.5,world):
                    break

    def get_img(self):
        return self.imgs[self.anitick//8 if self.speed==0.5 else self.anitick//4%4]

class CannonBall(Entity):
    img=img2("CannonBall")
    orect = pygame.Rect(10,10,12,12)
    def __init__(self,x,y,dx):
        self.dx=dx
        self.place(x,y)
    def update(self, world, events):
        if not self.moving:
            if world.inworld(self.x,self.y):
                self.move(self.dx,0,4,world,True)
            else:
                world.e.remove(self)

