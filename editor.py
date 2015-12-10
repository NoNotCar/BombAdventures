__author__ = 'NoNotCar'
import pygame, sys
pygame.init()
screen = pygame.display.set_mode((640, 704))
import World
import Tiles
import Img

clock = pygame.time.Clock()
selmenu=0
selobjs=[0 for _ in Tiles.tilemenus+Tiles.objmenus]
w=World.World(True)
expimg=Img.img2("Exp")
pexpimg=Img.img2("ExpPen")
bombimg=Img.img2("Bomb")
while True:
    kmods=pygame.key.get_mods()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_s and kmods&pygame.KMOD_LCTRL:
            w.save()
            print "SAVED"
        elif event.type==pygame.KEYDOWN:
            menus=Tiles.tilemenus+Tiles.objmenus
            menu=menus[selmenu]
            if event.key==pygame.K_w:
                selobjs[selmenu]=(selobjs[selmenu]-1)%len(menu)
            elif event.key==pygame.K_s:
                selobjs[selmenu]=(selobjs[selmenu]+1)%len(menu)
            elif event.key==pygame.K_a:
                selmenu=(selmenu-1)%len(menus)
            elif event.key==pygame.K_d:
                selmenu=(selmenu+1)%len(menus)
            elif event.key==pygame.K_t:
                screen = pygame.display.set_mode((640, 672))
                w.save()
                wo=World.World(False,"sav")
                Img.musplay("Cumulo.ogg")
                while not (wo.playerdead or wo.done):
                    events = pygame.event.get()
                    for event in events:
                        if event.type == pygame.QUIT:
                            sys.exit()
                    screen.fill((125, 255, 255))
                    wo.update(events)
                    wo.render(screen)
                    pygame.draw.rect(screen,(200,200,200),pygame.Rect(0,640,640,32))
                    ap=wo.get_activeplayer()
                    screen.blit(ap.iconv[(0,1)],(0,640))
                    for n in range(ap.rng):
                        screen.blit(pexpimg if ap.pen else expimg, (32+n*32,640))
                    for x in range(ap.bombs):
                        screen.blit(bombimg,(64+n*32+x*32,640))
                    pygame.display.flip()
                    clock.tick(60)
                screen = pygame.display.set_mode((640, 704))
                pygame.mixer.music.stop()
    seltype=selmenu<len(Tiles.tilemenus)
    if pygame.mouse.get_pressed()[0]:
        mpos=pygame.mouse.get_pos()
        if mpos[0]<640 and mpos[1]<640:
            if seltype:
                w.t[mpos[0]//32][mpos[1]//32]=0 if kmods&pygame.KMOD_LSHIFT else Tiles.tilemenus[selmenu][selobjs[selmenu]]+1
            else:
                w.o[mpos[0]//32][mpos[1]//32]=0 if kmods&pygame.KMOD_LSHIFT else Tiles.objmenus[selmenu-len(Tiles.tilemenus)][selobjs[selmenu]]+1
    screen.fill((125, 255, 255))
    w.render(screen)
    for n in range(19):
        pygame.draw.line(screen,(125,125,125),(n*32+32,0),(n*32+32,640),2)
        pygame.draw.line(screen,(125,125,125),(0,n*32+32),(640,n*32+32),2)
    for n,tm in enumerate(Tiles.tilemenus):
        screen.blit(Tiles.tiles[tm[selobjs[n]]].img,(n*32,656))
    for on,om in enumerate(Tiles.objmenus):
        screen.blit(Tiles.eobjs[om[selobjs[n+on+1]]][0],(n*32+64+on*32,656))
    off=selmenu*32+(0 if selmenu<len(Tiles.tilemenus) else 32)
    pygame.draw.polygon(screen,(0,0,0),[(off+16,688),(off,704),(off+32,704)])
    pygame.display.flip()
    clock.tick(60)