__author__ = 'NoNotCar'
import pygame, sys, Img
import World
from Worlds import worlds, castle
import Tiles,Object

pygame.init()
pygame.font.init()
pdf = pygame.font.get_default_font()
tfont=pygame.font.Font(pdf,60)
sfont=pygame.font.Font(pdf,20)
screen = pygame.display.set_mode((640, 640))
clock = pygame.time.Clock()
breaking = False
level=[1,1]
success=Img.sndget("Level")
while not breaking:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            breaking = True
    screen.fill((255, 0, 0))
    Img.bcentre(tfont,"BOMB ADVENTURES",screen)
    pygame.display.flip()
    clock.tick(60)
while True:
    try:
        w = World.World(False,level)
    except IOError:
        screen.fill((255,255,0))
        Img.bcentre(tfont,"YOU WIN",screen)
        pygame.display.flip()
        pygame.time.wait(2000)
        break
    world=worlds[level[0]-1] if level[1]!=8 else castle
    Img.musplay(world.music+".ogg")
    screen.fill(world.loadcolour)
    Img.bcentre(tfont,"WORLD %s-%s"%tuple(level),screen)
    Img.bcentre(sfont,w.fltext,screen,50)
    pygame.display.flip()
    pygame.time.wait(2000)
    tofpsprint=60
    Tiles.Grass.img=world.textures[0]
    Object.Block.img=world.textures[1]
    Object.Indest.img=world.textures[2]
    if len(world.textures)==4:
        Tiles.Ice.img=world.textures[3]
    back=world.back
    pygame.event.get()
    while not (w.playerdead or w.done):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill(back)
        w.update(events)
        w.render(screen)
        pygame.display.flip()
        clock.tick(60)
    pygame.mixer.music.stop()
    if w.done:
        success.play()
        if level[1] in [8,"A"]:
            level=[level[0]+1,1]
        elif w.exitcode=="SECRET":
            level=[level[0],"A"]
        else:
            level[1]+=1
    pygame.time.wait(1000)
