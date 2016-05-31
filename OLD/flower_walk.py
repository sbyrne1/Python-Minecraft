from mcpi.minecraft import Minecraft
from time import sleep

mc=Minecraft.create()

flower=38
cactus=81

while True:
    px,py,pz=mc.player.getPos()
    mc.setBlock(px,py,pz,cactus)
    sleep(0.5)
