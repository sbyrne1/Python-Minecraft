from mcpi.minecraft import Minecraft

mc=Minecraft.create()

px,py,pz=mc.player.getPos()
pdir=mc.player.getDirection()

print(pdir)
