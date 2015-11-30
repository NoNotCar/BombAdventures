import Img

class World(object):
    def __init__(self,txt,mus,back,load):
        self.textures=txt
        self.music=mus
        self.back=back
        self.loadcolour=load
worlds=[World([Img.img2("Grass"),Img.img2("Block"),Img.img2("Grass2")],"Cumulo",(125, 255, 255),(125, 225, 0)),
        World([Img.img2("Snow"),Img.img2("CastleBlock"),Img.img2("FrozenIn")],"Chr",(240, 255, 255),(255, 255, 255))]
castle=World([Img.img2("CastleFloor"),Img.img2("CastleBlock"),Img.img2("CastleIn")],"Flags",(125, 125, 125),(200, 200, 200))