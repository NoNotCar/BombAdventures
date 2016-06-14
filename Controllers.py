import pygame
import UniJoy
class Controller(object):
    def get_buttons(self,events):
        return 0,0
    def get_dirs(self):
        return [(0,0)]

class Keyboard1(Controller):
    kconv = {pygame.K_w: (0, -1), pygame.K_s: (0, 1), pygame.K_a: (-1, 0), pygame.K_d: (1, 0)}
    def get_buttons(self,events):
        bomb=False
        act=False
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    bomb=True
                elif e.key==pygame.K_LSHIFT:
                    act=True
        return bomb,act
    def get_dirs(self):
        keys = pygame.key.get_pressed()
        kpr=[]
        for k, v in self.kconv.iteritems():
            if keys[k]:
                kpr.append(v)
        return kpr
    def get_dir_pressed(self,events):
        for e in events:
            if e.type==pygame.KEYDOWN and e.key in self.kconv.keys():
                return self.kconv[e.key]
class Keyboard2(Keyboard1):
    kconv={pygame.K_UP: (0, -1), pygame.K_DOWN: (0, 1), pygame.K_LEFT: (-1, 0), pygame.K_RIGHT: (1, 0)}
    def get_buttons(self,events):
        bomb=False
        act=False
        for e in events:
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_RETURN:
                    bomb=True
                elif e.key==pygame.K_RCTRL:
                    act=True
        return bomb,act
class UniJoyController(Controller):
    cooldown=0
    def __init__(self,n):
        self.uj=UniJoy.Unijoy(n)
    def get_buttons(self,events):
        bomb=False
        act=False
        for e in events:
            if e.type==pygame.JOYBUTTONDOWN and e.joy==self.uj.jnum:
                if self.uj.get_b("A"):
                    bomb=True
                if self.uj.get_b("B"):
                    act=True
                break
        return bomb,act
    def get_dirs(self):
        return [self.uj.getdirstick(1)]
    def get_dir_pressed(self,events):
        ds=self.uj.getdirstick(1)
        if self.cooldown:
            self.cooldown-=1
            return 0,0
        else:
            if ds!=(0,0):
                self.cooldown=30
            return ds