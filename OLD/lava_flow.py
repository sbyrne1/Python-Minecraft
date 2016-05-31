from mcpi.minecraft import Minecraft

mc=Minecraft.create()

px,py,pz=mc.player.getPos()

lava=10

mc.setBlock(px+3,py+3,pz,lava)
