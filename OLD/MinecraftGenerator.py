# Author: Stephen Byrne
# Date: 5-29-2016
from mcpi.minecraft import Minecraft

class MinecraftGenerator:

    def __init__(self):
        # create minecraft object
        self.mc=Minecraft.create()

    def update_position(self):
        # resets values of variables representing player position
        self.px,self.py,self.pz = self.mc.player.getPos()
        # float value is converted to integer 
        self.px=int(self.px)
        self.py=int(self.py)
        self.pz=int(self.pz)

    def get_position(self):
        # returns [x,y,z] location player is in
        return [self.px,self.py,self.pz]

class GoldBlockFinder(MinecraftGenerator):

    def __init__(self):
        MinecraftGenerator.__init__(self)
        self.reset()

    def reset(self):
        # resets/sets variables used by GoldBlockFinder
        # this is perhaps a clumsy way to do this
        # ie it is not 100% successful
        self.g_loc = []
        self.set_radius(2)
        self.gold=41
        self.iron=42
        self.gold_found=False
        self.g_scan_keys=[]
        self.g_scan_blocks=[]

        self.delta_x = 0
        self.delta_y = 0
        self.delta_z = 0
        self.mode = "default"

    def set_radius(self, value):
        # defines scan radius relative to player position
        self.radius = int(value)

    
    def scan_in_player_radius(self,rad,target):
        # scan for target brick type within radius of player
        found = []
        self.update_position()
        for x in range (self.px-rad,self.px+rad):
            for y in range (self.py-rad,self.py+rad):
                for z in range (self.pz-rad,self.pz+rad):
                    self.block = self.mc.getBlock(x,y,z) # get block ID
                    if self.block == target:
                        # compiles a list of block coordinates matching target
                        # brick type
                        found.append([x,y,z])
        return found

    def find_gold(self):
        gold_bricks = self.scan_in_player_radius(self.radius,self.gold)
        if len(gold_bricks)==1:
            self.gold_found=True
            self.g_loc=gold_bricks[0]
            self.analyze_gold()
        # ERROR CHECK NEEDED: what if there are more than 1 gold blocks?

    def analyze_gold(self):
        # make a list of lists of x,y,z locations around the gold cube
        for iy in range (-1,2):
            for ix in range (-1,2):
                for iz in range (-1,2):
                    self.g_scan_keys.append([self.g_loc[0] + ix, self.g_loc[1] + iy, self.g_loc[2] + iz])

        # make a corresponding list of block types
        for ai in range (0,27):
            jx = self.g_scan_keys[ai][0]
            jy = self.g_scan_keys[ai][1]
            jz = self.g_scan_keys[ai][2]
            block_id = self.mc.getBlock(jx,jy,jz) # block ID
            self.g_scan_blocks.append(block_id)

    def find_blocks(self,block_type):
        found = []
        if self.gold_found:
            for i in range (0,27):
                if (self.g_scan_blocks[i] == block_type):
                    found.append(self.g_scan_keys[i])
        else:
            print("No gold block found.")
        return found

    def calc_deltas(self,a_loc = [],b_loc = []):
        if (len(a_loc)==3) and (len(b_loc)==3):
            d_x = b_loc[0]-a_loc[0]
            d_y = b_loc[1]-a_loc[1]
            d_z = b_loc[2]-a_loc[2]
            return [d_x,d_y,d_z]
        else:
            return 0

    def set_build_mode(self):
        # is this the right place for this?
        iron_blocks = self.find_blocks(self.iron)
        iron_found = len(iron_blocks)
        print("set_build_mode")
        print("iron_blocks=="+str(iron_blocks))
        print("iron_found=="+str(iron_found))
        self.delta_x = 0
        self.delta_y = 0
        self.delta_z = 0
        if iron_found > 0:
            for i in range(0,iron_found):
                deltas = self.calc_deltas(self.g_loc,iron_blocks[i])
                self.delta_x = deltas[0] + self.delta_x
                self.delta_y = deltas[1] + self.delta_y
                self.delta_z = deltas[2] + self.delta_z
        # Should the following functionality be in MinecraftBuilder?
        if iron_found==1:
            self.mode="line"
        elif iron_found==2:
            self.mode="plane"
        elif iron_found==3:
            self.mode="hollow_cube"
        print("mode=="+self.mode)
        print("delta_x=="+str(self.delta_x))
        print("delta_y=="+str(self.delta_y))
        print("delta_z=="+str(self.delta_z))

class MapBuilder(GoldBlockFinder):
    def __init__(self):
        GoldBlockFinder.__init__(self)
        self.plane=[]
        self.plane.append([1,2,1,2,1])
        self.plane.append([2,1,2,1,2])
        self.plane.append([1,2,1,2,1])
        self.plane.append([2,1,2,1,2])
        self.plane.append([1,2,1,2,1])

        self.cube=[]
        self.cube.append([])
        self.cube.append([])
        self.cube.append([])
        self.cube.append([])
        self.cube.append([])
        self.cube.append([])
        self.cube.append([])
        self.cube[0].append([1,2,1,2,1])
        self.cube[0].append([2,1,2,1,2])
        self.cube[0].append([1,2,1,2,1])
        self.cube[0].append([2,1,2,1,2])
        self.cube[0].append([1,2,1,2,1])
        self.cube[1].append([1,2,1,2,1])
        self.cube[1].append([2,0,0,0,2])
        self.cube[1].append([1,0,0,0,1])
        self.cube[1].append([2,0,0,0,0])
        self.cube[1].append([1,2,1,2,1])
        self.cube[2].append([2,1,2,1,0])
        self.cube[2].append([1,0,0,0,1])
        self.cube[2].append([2,0,0,0,0])
        self.cube[2].append([1,0,0,0,0])
        self.cube[2].append([2,1,2,1,2])
        self.cube[3].append([2,1,2,1,2])
        self.cube[3].append([1,0,0,0,1])
        self.cube[3].append([2,0,0,0,0])
        self.cube[3].append([1,0,0,0,0])
        self.cube[3].append([2,1,2,1,2])
        self.cube[4].append([2,1,2,1,2])
        self.cube[4].append([1,0,0,0,1])
        self.cube[4].append([2,0,0,0,0])
        self.cube[4].append([1,0,0,0,0])
        self.cube[4].append([2,1,2,1,2])
        self.cube[5].append([2,1,2,1,2])
        self.cube[5].append([1,0,0,0,1])
        self.cube[5].append([2,0,0,0,2])
        self.cube[5].append([1,0,0,0,1])
        self.cube[5].append([2,0,0,0,2])
        self.cube[6].append([1,2,1,2,1])
        self.cube[6].append([2,1,2,1,2])
        self.cube[6].append([1,2,1,2,1])
        self.cube[6].append([2,1,2,1,2])
        self.cube[6].append([1,2,1,2,1])

    def build_plane(self):
        if (self.delta_x!=0) and (self.delta_y!=0):
            for x in range(0,len(self.plane)-1):
                for y in range(0,len(self.plane[x])-1):
                    print(str(x) + "x," + str(y) + "y," + str(self.plane[x][y]))
                    block_x=self.g_loc[0]+self.delta_x*x
                    block_y=self.g_loc[1]+self.delta_y*y
                    block_z=self.g_loc[2]
                    self.mc.setBlock(block_x,block_y,block_z,self.plane[x][y])
        elif (self.delta_x!=0) and (self.delta_z!=0):
            for x in range(0,len(self.plane)-1):
                for z in range(0,len(self.plane[x])-1):
                    block_x=self.g_loc[0]+self.delta_x*x
                    block_y=self.g_loc[1]
                    block_z=self.g_loc[2]+self.delta_z*z
                    self.mc.setBlock(block_x,block_y,block_z,self.plane[x][z])
        elif (self.delta_y!=0) and (self.delta_z!=0):
            for y in range(0,len(self.plane)-1):
                for z in range(0,len(self.plane[y])-1):
                    block_x=self.g_loc[0]
                    block_y=self.g_loc[1]+self.delta_y*y
                    block_z=self.g_loc[2]+self.delta_z*z
                    self.mc.setBlock(block_x,block_y,block_z,self.plane[y][z])
    def build_cube(self):
        #self.to_x = self.g_loc[0]+self.delta_x*self.blocks_x
        #self.to_y = self.g_loc[1]+self.delta_y*self.blocks_y
        #self.to_z = self.g_loc[2]+self.delta_z*self.blocks_z
        for x in range(0,len(self.cube)):
            for y in range(0,len(self.cube[x])):
                for z in range(0,len(self.cube[x][y])):
                    print(str(x)+"x,"+str(y)+"y,"+str(z)+"z")
                    block_x=self.g_loc[0]+self.delta_x*x
                    block_y=self.g_loc[1]+self.delta_y*y
                    block_z=self.g_loc[2]+self.delta_z*z
                    self.mc.setBlock(block_x,block_y,block_z,self.cube[x][y][z])


class MinecraftBuilder(GoldBlockFinder):
    def __init__(self):
        GoldBlockFinder.__init__(self)
        self.blocks_x = 1
        self.blocks_y = 1
        self.blocks_z = 1

    def set_materials(self,a=1,b=1,c=1,d=1,e=1,f=1):
        self.material_1 = int(a)
        self.material_2 = int(b)
        self.material_3 = int(c)
        self.material_4 = int(d)
        self.material_5 = int(e)
        self.material_6 = int(f)

    def set_dims(self,x,y,z):
        self.blocks_x = int(x)
        self.blocks_y = int(y)
        self.blocks_z = int(z)
        print("dimensions set")

    def builder(self):
        # set default values
        self.to_x = self.g_loc[0]
        self.to_y = self.g_loc[1]
        self.to_z = self.g_loc[2]

        if self.mode=="line":
            self.build_line()
        elif self.mode=="plane":
            self.build_plane()
        elif self.mode=="hollow_cube":
            self.build_hollow_cube()

    def build_line(self):
        if (self.delta_x!=0):
            self.to_x = self.g_loc[0]+self.delta_x*self.blocks_x
        elif (self.delta_y!=0):
            self.to_y = self.g_loc[1]+self.delta_y*self.blocks_y
        elif (self.delta_z!=0):
            self.to_z = self.g_loc[2]+self.delta_z*self.blocks_z
        self.mc.setBlocks(self.g_loc[0],self.g_loc[1],self.g_loc[2],self.to_x,self.to_y,self.to_z,self.material_1)

    def build_plane(self):
        if (self.delta_x!=0) and (self.delta_y!=0):
            self.to_x = self.g_loc[0]+self.delta_x*self.blocks_x
            self.to_y = self.g_loc[1]+self.delta_y*self.blocks_y
        elif (self.delta_x!=0) and (self.delta_z!=0):
            self.to_x = self.g_loc[0]+self.delta_x*self.blocks_x
            self.to_z = self.g_loc[2]+self.delta_z*self.blocks_z
        elif (delta_y!=0) and (delta_z!=0):
            self.to_y = self.g_loc[1]+self.delta_y*self.blocks_y
            self.to_z = self.g_loc[2]+self.delta_z*self.blocks_z
        self.mc.setBlocks(self.g_loc[0],self.g_loc[1],self.g_loc[2],self.to_x,self.to_y,self.to_z,self.material_1)

    def build_hollow_cube(self):
        self.to_x = self.g_loc[0]+self.delta_x*self.blocks_x
        self.to_y = self.g_loc[1]+self.delta_y*self.blocks_y
        self.to_z = self.g_loc[2]+self.delta_z*self.blocks_z
        # replace cube space with air (just in case we are building into a hill)
        self.mc.setBlocks(self.g_loc[0],self.g_loc[1],self.g_loc[2],self.to_x,self.to_y,self.to_z,0)
        # make the floor
        self.mc.setBlocks(self.g_loc[0],self.g_loc[1],self.g_loc[2],self.to_x,self.g_loc[1],self.to_z,self.material_1)
        # make 4 walls
        self.mc.setBlocks(self.g_loc[0],self.g_loc[1]+1*self.delta_y,self.g_loc[2],self.to_x,self.to_y,self.g_loc[2],self.material_2) # A to D
        self.mc.setBlocks(self.to_x,self.g_loc[1]+1*self.delta_y,self.g_loc[2],self.to_x,self.to_y,self.to_z,self.material_3) # D to C
        self.mc.setBlocks(self.to_x,self.g_loc[1]+1*self.delta_y,self.to_z,self.g_loc[0],self.to_y,self.to_z,self.material_4) # B to C
        self.mc.setBlocks(self.g_loc[0],self.g_loc[1]+1*self.delta_y,self.to_z,self.g_loc[0],self.to_y,self.g_loc[2],self.material_5) # B to A
        # make a ceiling
        self.mc.setBlocks(self.g_loc[0],self.to_y,self.g_loc[2],self.to_x,self.to_y,self.to_z,self.material_6)

#mine = MinecraftBuilder()
#mine.update_position()
#mine.find_gold()
#mine.set_build_mode()
#mine.set_dims(10,2,12)
#mine.set_materials(57,35,20,5,45,246)
#mine.builder()

#mine = MapBuilder()
#mine.update_position()
#mine.find_gold()
#mine.set_build_mode()
#mine.build_cube()
#
