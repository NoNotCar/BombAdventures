__author__ = 'NoNotCar'
import pygame, sys
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 672))
import World, Img
from Worlds import worlds, castle
import Tiles,Object,Save

pdf = pygame.font.get_default_font()
tfont=pygame.font.Font(pdf,60)
sfont=pygame.font.Font(pdf,20)
clock = pygame.time.Clock()
breaking = False
man=Img.img2("Men/Man2r")
wnum=1
expimg=Img.img2("Exp")
pexpimg=Img.img2("ExpPen")
bombimg=Img.img2("Bomb")
Img.musplay("OF.ogg")
try:
    savefile=open("SAVE.sav","r")
    save=savefile.readline()
    if Save.load(save):
        wnum=Save.load(save)
    savefile.close()
except IOError:
    pass
success=Img.sndget("Level")
while not breaking:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            breaking = True
    screen.fill((255, 0, 0))
    Img.bcentre(tfont,"BOMB ADVENTURES",screen)
    Img.bcentre(sfont,"Click to start",screen,50)
    pygame.display.flip()
    clock.tick(60)
breaking=False
wselnum=0
mx=0
while not breaking:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            my=pygame.mouse.get_pos()[1]
            sel=(my-70)//64
            if 0<=sel<wnum and sel<len(worlds):
                wselnum=sel+1
                breaking=True
    screen.fill((0, 0, 0))
    Img.bcentrex(tfont,"SELECT WORLD",screen,2,(255,255,255))
    for n,w in enumerate(worlds[:wnum]):
        pygame.draw.rect(screen,w.loadcolour,pygame.Rect(0,n*64+66,640,64))
        Img.bcentrex(tfont,"WORLD %s" % str(n+1),screen,n*64+70)
    screen.blit(man,(mx-32,646))
    mx=(mx+2)%672
    pygame.display.flip()
    clock.tick(60)
level=[wselnum,1]
success.play()
pygame.mixer.music.stop()
pygame.time.wait(1000)
while True:
    try:
        w = World.World(False,level)
    except IOError:
        screen.fill((255,255,0))
        Img.bcentre(tfont,"YOU WIN",screen)
        Img.bcentre(sfont,"(Hooray)",screen,50)
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
    warplevel=1
    while True:
        while not (w.playerdead or w.done):
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    sys.exit()
            screen.fill(back)
            w.update(events)
            w.render(screen)
            pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,640,640,32))
            ap=w.get_activeplayer()
            screen.blit(ap.iconv[(0,1)],(0,640))
            for n in range(ap.rng):
                screen.blit(pexpimg if ap.pen else expimg, (32+n*32,640))
            for x in range(ap.bombs):
                screen.blit(bombimg,(64+n*32+x*32,640))
            pygame.display.flip()
            clock.tick(60)
        if w.exitcode!="WARP":
            break
        else:
            success.play()
            w=World.World(False,level+[warplevel])
            warplevel+=1
            pygame.time.wait(1000)
            pygame.event.get()
    pygame.mixer.music.stop()
    if w.done:
        success.play()
        if level[1] in [8,"A"]:
            level=[level[0]+1,1]
            if level[0]>wnum:
                savefile=open("SAVE.sav","w")
                savefile.write(Save.save(level[0]))
                savefile.close()
        elif w.exitcode=="SECRET":
            level=[level[0],"A"]
        else:
            level[1]+=1
    pygame.time.wait(1000)
