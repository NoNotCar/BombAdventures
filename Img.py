__author__ = 'NoNotCar'
import pygame
import os

np = os.path.normpath
loc = os.getcwd() + "/Assets/"
pygame.mixer.init()


def img2(fil):
    return pygame.transform.scale2x(pygame.image.load(np(loc + fil + ".png")))


def img32(fil):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), (32, 32))


def imgsz(fil, sz):
    return pygame.transform.scale(pygame.image.load(np(loc + fil + ".png")), sz)


def imgstrip2(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    for n in range(img.get_width() // 16):
        imgs.append(pygame.transform.scale2x(img.subsurface(pygame.Rect(n * 16, 0, 16, 16))))
    return imgs


def imgstrip(fil):
    img = pygame.image.load(np(loc + fil + ".png"))
    imgs = []
    for n in range(img.get_width() // 16):
        imgs.append(pygame.transform.scale(img.subsurface(pygame.Rect(n * 16, 0, 16, 16)), (32, 32)))
    return imgs


def musplay(fil):
    pygame.mixer.music.load(np(loc + fil))
    pygame.mixer.music.play(-1)


def bcentre(font, text, surface, offset=0, col=(0, 0, 0), xoffset=0):
    render = font.render(str(text), True, col)
    textrect = render.get_rect()
    textrect.centerx = surface.get_rect().centerx + xoffset
    textrect.centery = surface.get_rect().centery + offset
    return surface.blit(render, textrect)

def sndget(fil):
    return pygame.mixer.Sound(np(loc+fil+".wav"))
