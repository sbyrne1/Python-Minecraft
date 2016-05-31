from mcpi.minecraft import Minecraft

mc=Minecraft.create()

mc.postToChat("Hello world")

px,py,pz=mc.player.getPos()

color=0
wool=35
blocks_x=5
blocks_y=10
blocks_z=15

for bx in range (0,blocks_x):
    for by in range (0,blocks_y):
        for bz in range (0,blocks_z):
            mc.setBlock(px+bx+1,py+by,pz+bz,1) 
            #mc.setBlock(x+1,y+num,z+i,wool,color)
            #color=color+1
