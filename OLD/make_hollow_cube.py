from mcpi.minecraft import Minecraft

mc=Minecraft.create()

px,py,pz=mc.player.getPos()

blocks_x=4
blocks_y=6
blocks_z=4

mat_a=57 # diamond block
mat_b=4 # cobblestone
mat_c=20 # glass
mat_d=17 # wood
mat_e=98 # stone brick
mat_floor=17 # wood

# make a floor
for bx in range (0,blocks_x):
    for bz in range (0,blocks_z):
        mc.setBlock(px+bx+1,py,pz+bz,mat_floor)

# make the walls
for by in range (0,blocks_y):
    for bx in range (0,blocks_x):
        mc.setBlock(px+bx+1,py+by,pz,mat_a)
        mc.setBlock(px+bx+1,py+by,pz+blocks_z-1,mat_b)
    for bz in range (0,blocks_z):
        mc.setBlock(px+blocks_x+1,py+by,pz+bz,mat_c)
        mc.setBlock(px+1,py+by,pz+bz,mat_d)

# make a roof
for bx in range (0,blocks_x):
    for bz in range (0,blocks_z):
        mc.setBlock(px+bx+1,py+blocks_y,pz+bz,mat_e)
    

