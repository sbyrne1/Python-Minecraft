from mcpi.minecraft import Minecraft
from Blocks_List import *
"""
mc=Minecraft.create()

px,py,pz=mc.player.getPos()


blocks_x=5
blocks_y=5
blocks_z=5

tnt=46

mc.setBlocks(px,py-1,pz,px+1,py-1000,pz+1,tnt,1)
"""

#step 1, get player pos
#step 2, find gold corner
#step 3, replace gold with tnt

class make_cube_of_tnt:
    def __init__(self):
        px,py,pz=mx.player.getPos()
        tnt_block_pos = {0,0,0} #x,y,z of brick;

    def find_gold_corner(self):

        return x, y, z

    def replace_Gold_with_TNT(self):
        #if tnt_block_pos != 0,0,0 replace.
        #otherwise display message, "corner not found!"
