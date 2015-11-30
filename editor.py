import Tiles

__author__ = 'NoNotCar'
import pygame, sys
import World
import Tiles

pygame.init()
screen = pygame.display.set_mode((640, 704))
clock = pygame.time.Clock()
seltile=0
selobj=0
w=World.World(True)
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN and event.key==pygame.K_s:
            w.save()
            print "SAVED"
        elif event.type==pygame.KEYDOWN:
            if event.key==pygame.K_UP:
                seltile=(seltile-1)%len(Tiles.tiles)
            elif event.key==pygame.K_DOWN:
                seltile=(seltile+1)%len(Tiles.tiles)
            elif event.key==pygame.K_LEFT:
                selobj=(selobj-1)%len(Tiles.eobjs)
            elif event.key==pygame.K_RIGHT:
                selobj=(selobj+1)%len(Tiles.eobjs)
    kmods=pygame.key.get_mods()
    if pygame.mouse.get_pressed()[0]:
        mpos=pygame.mouse.get_pos()
        if mpos[0]<640 and mpos[1]<640:
            w.t[mpos[0]//32][mpos[1]//32]=0 if kmods&pygame.KMOD_LSHIFT else seltile+1
    elif pygame.mouse.get_pressed()[2]:
        mpos=pygame.mouse.get_pos()
        if mpos[0]<640 and mpos[1]<640:
            w.o[mpos[0]//32][mpos[1]//32]=0 if kmods&pygame.KMOD_LSHIFT else selobj+1
    screen.fill((125, 255, 255))
    w.render(screen)
    for n in range(19):
        pygame.draw.line(screen,(125,125,125),(n*32+32,0),(n*32+32,640),2)
        pygame.draw.line(screen,(125,125,125),(0,n*32+32),(640,n*32+32),2)
    screen.blit(Tiles.tiles[seltile].img,(0,656))
    screen.blit(Tiles.eobjs[selobj][0],(608,656))
    pygame.display.flip()
    clock.tick(60)