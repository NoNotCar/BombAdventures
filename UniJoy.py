'''
Created on 25 Jul 2015
@author: Thomas
'''
from pygame import joystick

joystick.init()
buconv = {"XBOX": {"A": 0, "B": 1, "X": 2, "Y": 3, "L1": 4, "R1": 5, "SELECT": 6, "START": 7},
          "PS2": {"A": 2, "B": 3, "L1": 6},
          "CHEAP": {"A": 2, "B": 3, "L1": 4}}


class Unijoy:
    def __init__(self, jnum):
        self.jnum = jnum
        self.j = joystick.Joystick(jnum)
        self.j.init()
        if self.j.get_numaxes() == 5:
            self.type = "XBOX"
        elif self.j.get_numaxes() == 4:
            self.type = "PS2"
        else:
            self.type = "CHEAP"

    def get_b(self, b):
        if b == "L2" and self.type == "XBOX":
            return self.j.get_axis(2) > 0.5
        elif b == "R2" and self.type == "XBOX":
            return self.j.get_axis(2) < -0.5
        return self.j.get_button(buconv[self.type][b])
    def getstick(self, stick):
        s = 2 * stick - 2
        if stick == 2 and self.type == "XBOX":
            return self.j.get_axis(4), self.j.get_axis(3)
        else:
            return self.j.get_axis(s), self.j.get_axis(s + 1)

    def getdirstick(self, stick):
        sx, sy = self.getstick(stick)
        if abs(sx) > 0.5 or abs(sy) > 0.5:
            if abs(sx) > abs(sy):
                return int(round(sx)), 0
            else:
                return 0, int(round(sy))
        return (0,0)


# Testing
"""import pygame
pygame.init()
teststick=Unijoy(0)
while True:
    pygame.event.pump()
    if teststick.get_b("R2"):
        print "UGO JAV"
        break"""
