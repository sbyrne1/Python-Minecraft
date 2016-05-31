from mcpi.minecraft import Minecraft

mc=Minecraft.create()

px,py,pz=mc.player.getPos()


blocks_x=5
blocks_y=5
blocks_z=5

tnt=46

mc.setBlocks(px,py-1,pz,px+1,py-1000,pz+1,tnt,1)
