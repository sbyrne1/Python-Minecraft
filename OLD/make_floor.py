from mcpi.minecraft import Minecraft

mc=Minecraft.create()

px,py,pz=mc.player.getPos()

blocks_x=5
blocks_z=15

by=py-1
bx=px
bz=pz
trigger=True

while trigger:
    bx=bx+1
    bz=pz
    mc.setBlock(bx,by,bz,57)
    


