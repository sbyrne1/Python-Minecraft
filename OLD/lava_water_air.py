from mcpi.minecraft import Minecraft
from time import sleep

mc=Minecraft.create()

px,py,pz=mc.player.getPos()

lava=10
water=8
air=0

mc.setBlock(px+3,py+3,pz,lava)
sleep(20)
mc.setBlock(px+3,py+5,pz,water)
sleep(4)
mc.setBlock(px+3,py+5,pz,air)
