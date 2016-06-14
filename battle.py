__author__ = 'NoNotCar'
import pygame, sys, os
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((640, 704))
import BattleWorld, Img
from random import choice
import Controllers

pdf = pygame.font.get_default_font()
tfont=pygame.font.Font(pdf,60)
sfont=pygame.font.Font(pdf,20)
clock = pygame.time.Clock()
expimg=Img.img2("Exp")
pexpimg=Img.img2("ExpPen")
bombimg=Img.img2("Bomb")
tickimg=Img.img2("Tick")
crossimg=Img.img2("Null")
pimgs=[Img.img2("men/"+x) for x in ["Man2","FMan","SMan","Tman"]]#+[Img.imgstrip("men/CMan")[0]]
breaking = False
Img.musplay("OF.ogg")
while not breaking:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            breaking = True
    screen.fill((255, 0, 0))
    Img.bcentre(tfont,"BOMB BATTLES",screen)
    Img.bcentre(sfont,"Click to start",screen,50)
    pygame.display.flip()
    clock.tick(60)
breaking=False
controllers=[Controllers.Keyboard1(),Controllers.Keyboard2()]+[Controllers.UniJoyController(n) for n in range(pygame.joystick.get_count())]
activecons=[]
acps=[]
rsps=[]
rsc=[]
while not breaking:
    gevents=pygame.event.get()
    for event in gevents:
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and len(rsps)>1:
            breaking = True
    for n,c in enumerate(activecons):
        if c.get_buttons(gevents)[0]:
            if acps[n] not in rsps:
                rsps.append(acps[n])
                rsc.append(c)
    for c in controllers[:]:
        if c.get_buttons(gevents)[0]:
            activecons.append(c)
            acps.append(0)
            controllers.remove(c)
    screen.fill((0, 0, 0))
    Img.bcentrex(tfont,"PLAYER SELECT",screen,0,(255,255,255))
    n=-1
    for n,c in enumerate(activecons):
        if c not in rsc:
            cdir=c.get_dir_pressed(gevents)
            if (1,0) == cdir:
                acps[n]=(acps[n]+1)%len(pimgs)
            elif (-1,0) == cdir:
                acps[n]=(acps[n]-1)%len(pimgs)
            screen.blit(pimgs[acps[n]],(304,n*32+94))
            if acps[n] in rsps:
                screen.blit(crossimg,(336,n*32+94))
        else:
            screen.blit(pimgs[acps[n]],(304,n*32+94))
            screen.blit(tickimg,(336,n*32+94))
    Img.bcentrex(sfont,"Press <bomb> to join",screen,n*32+128,(255,255,255))
    pygame.display.flip()
    clock.tick(60)
while True:
    lvls=os.listdir(Img.np("lvls/battle/"))
    lvls=[lvl for lvl in lvls if lvl[0]==str(len(rsps))]
    w=BattleWorld.World(choice(lvls), rsps,rsc)
    Img.musplay("Cumulo.ogg")
    while len(w.ps)>=2:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        screen.fill((125, 255, 255))
        w.update(events)
        w.render(screen)
        pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,640,640,64))
        for pn,p in enumerate(w.ps):
            screen.blit(p.iconv[(0,1)],(0,640+pn*32))
            for n in range(p.rng):
                screen.blit(pexpimg if p.pen else expimg, (32+n*32,640+pn*32))
            for x in range(p.bombs):
                screen.blit(bombimg,(64+n*32+x*32,640+pn*32))
        pygame.display.flip()
        clock.tick(60)
    pygame.mixer.music.stop()
    pygame.time.wait(1000)