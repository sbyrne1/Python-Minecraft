# Author: Stephen Byrne
# Date: 5-29-2016
from mcpi.minecraft import Minecraft
#TODO figure out what class needs this import. -Bill





"""
    The MinecraftGenerator:
        Generates structures in Minecraft.

        MinecraftGenerator is a parent class:
            BlockFinder child of MinecraftGenerator.
            Builder child of BlockFinder.
"""
class MinecraftGenerator:
    """
    Attributes:
        mc: the instantance of Minecraft the MinecraftGenerator is associated with.

    """
    def __init__(self): #??? Uses mc instance.
        # create minecraft object
        print ("\nFUNCTION: MinecraftGenerator __init__")
        print ("Open connection to Minecraft Pi")
        self.mc=Minecraft.create()

        #TODO indentify class attributes, and initialize them in the constructor. -Bill


    def update_position(self):
        print ("\nFUNCTION: update_position")

        # resets values of variables representing player position
        self.px,self.py,self.pz = self.mc.player.getPos()

        # float value is converted to integer
        self.px=int(self.px)
        self.py=int(self.py)
        self.pz=int(self.pz)

    def get_position(self):
        print ("\nFUNCTION: get_position")

        # returns players [x,y,z] coordinates
        return [self.px,self.py,self.pz]

    def reset(self):
        #TODO reset required members for new building.
        print ("\nFUNCTION: reset")

#End of MinecraftGenerator Class.

#mine = Builder()
# find_gold defines most corner variables
# this
# find_gold() defines a corner
#mine.find_gold()
# builder(0) constructs a structure at first defined corner
#mine.builder(0)
# find blocks with block_id 3 (dirt) in first corner (0 index)
#dirt_blocks = mine.find_blocks(0,3) # search the first corner blocks for dirt
#print ("dirtblocks " + str(len(dirt_blocks)))
