# Author: Stephen Byrne
# Date: 5-29-2016
from mcpi.minecraft import Minecraft

class MinecraftGenerator:

    def __init__(self):
        # create minecraft object
        print ("\nFUNCTION: MinecraftGenerator __init__")
        print ("Open connection to Minecraft Pi")
        self.mc=Minecraft.create()

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

class BlockFinder(MinecraftGenerator):

    def __init__(self):
        print ("\nFUNCTION: BlockFinder __init__")
        # instantiate parent
        MinecraftGenerator.__init__(self)
        self.corners = []
        self.set_radius(2)
        self.gold=41
        self.iron=42

    def new_corner(self):
        print ("\nFUNCTION: new_corner")
        loc = [0,0,0]
        scan_coords = []
        scan_blocks = []
        iron_blocks = []
        delta_x = 0
        delta_y = 0
        delta_z = 0
        mode = "default"
        dict_corner = {'loc':loc,
                       'scan_coords':scan_coords,
                       'scan_blocks':scan_blocks,
                       'iron_blocks':iron_blocks,
                       'delta_x':delta_x,
                       'delta_y':delta_y,
                       'delta_z':delta_z
                       }
        self.corners.append(dict_corner)
        return len(self.corners)-1

    def get_mode(self,index):
        mode = self.corners[index]['mode']
        return mode
        
    def print_corners(self):
        print ("\nFUNCTION: print_corners")
        num_corners = len(self.corners)
        print ("there are " + str(num_corners) + " corners.")
        for ind in range (0,num_corners):
            print ("corner at index == " + str(ind))
            loc = self.corners[ind]['loc']
            print ("loc == " + str(loc))
            num_iron = len(self.corners[ind]['iron_blocks'])
            print (str(num_iron) + " iron blocks.")
        
    def set_radius(self, value):
        print ("\nFUNCTION: set_radius")
        # defines scan radius relative to player position
        self.radius = int(value)
        print ("radius == " + str(self.radius))
    
    def scan_in_player_radius(self,rad,target):
        print ("\nFUNCTION: scan_in_player_radius, radius == " + str(rad) + ", target == " + str(target))
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
        print ("\nFUNCTION: find_gold")
        gold_bricks = self.scan_in_player_radius(self.radius,self.gold)
        # this whole system relies on there being ONE gold brick in player radius
        if len(gold_bricks)==1:
            index=self.new_corner()
            print ("corner index == " + str(index))
            # if there are corners defined, gold was found
            self.corners[index]['loc']=gold_bricks[0]
            print ("corner location:")
            print (self.corners[index]['loc'])
            self.analyze_gold(index)
            self.analyze_iron(index)
        # ERROR CHECK NEEDED: what if there are 0 gold blocks or more than 1 gold blocks?

    def find_blocks(self, index, block_type):
        print ("\nFUNCTION: find_blocks, corner index == " + str(index))
        found = []
        for i in range (0,27):
            if (self.corners[index]['scan_blocks'][i] == block_type):
                found.append(self.corners[index]['scan_coords'][i])
        return found

    def analyze_gold(self,index):
        print ("\nFUNCTION: analyze_gold, corner index == " + str(index))
        # make a list of lists of x,y,z locations around the gold cube
        g_loc = self.corners[index]['loc']
        for iy in range (-1,2):
            for ix in range (-1,2):
                for iz in range (-1,2):
                    self.corners[index]['scan_coords'].append([g_loc[0] + ix, g_loc[1] + iy, g_loc[2] + iz])
        print ("scan_coords: these are the coordinates surrounding the gold block")
        print (self.corners[index]['scan_coords'])
        # make a corresponding list of block types
        for ai in range (0,27):
            jx = self.corners[index]['scan_coords'][ai][0]
            jy = self.corners[index]['scan_coords'][ai][1]
            jz = self.corners[index]['scan_coords'][ai][2]
            block_id = self.mc.getBlock(jx,jy,jz) # block ID
            self.corners[index]['scan_blocks'].append(block_id)
        print ("scan_blocks: these are the block types of the blocks surrounding the gold block")
        print (" the indexes of scan_coords and scan_blocks correspond")
        print (" 41==gold, 42==iron, 0==air, 1==dirt ...") 
        print (self.corners[index]['scan_blocks'])

    def calc_deltas(self,a_loc = [],b_loc = []):
        print ("\nFUNCTION: calc_deltas")
        # calculates delta values given two [x,y,z] coordinates
        if (len(a_loc)==3) and (len(b_loc)==3):
            d_x = b_loc[0]-a_loc[0]
            d_y = b_loc[1]-a_loc[1]
            d_z = b_loc[2]-a_loc[2]
            return [d_x,d_y,d_z]
        else:
            return 0

    def analyze_iron(self,index):
        print ("\nFUNCTION: analyze_iron, corner index == " + str(index))
        g_loc = self.corners[index]['loc']
        iron_blocks = self.find_blocks(index, self.iron)
        iron_found = len(iron_blocks)
        print ("iron blocks found == " + str(iron_found))
        delta_x = 0
        delta_y = 0
        delta_z = 0
        if iron_found > 0:
            for i in range(0,iron_found):
                deltas = self.calc_deltas(g_loc,iron_blocks[i])
                delta_x = deltas[0] + delta_x
                delta_y = deltas[1] + delta_y
                delta_z = deltas[2] + delta_z
        self.corners[index]['iron_blocks']=iron_blocks
        self.corners[index]['delta_x']=delta_x
        self.corners[index]['delta_y']=delta_y
        self.corners[index]['delta_z']=delta_z
        print ("delta_x == " + str(self.corners[index]['delta_x']))
        print ("delta_y == " + str(self.corners[index]['delta_y']))
        print ("delta_z == " + str(self.corners[index]['delta_z']))

class Builder(BlockFinder):
    def __init__(self):
        print ("\nFUNCTION: Builder __init__")
        BlockFinder.__init__(self)
        self.set_materials()
        self.set_dims(10,30,10)

    def set_materials(self,a=1,b=1,c=1,d=1,e=1,f=1):
        print ("\nFUNCTION: set_materials")
        self.material_1 = int(a)
        self.material_2 = int(b)
        self.material_3 = int(c)
        self.material_4 = int(d)
        self.material_5 = int(e)
        self.material_6 = int(f)

    def set_dims(self,x,y,z):
        print ("\nFUNCTION: set_dims")
        print ("basic dimensions of line, plane, or hollow_cube")
        print ("x==" + str(x) + ", y==" + str(y) + ", z==" + str(z))
        self.blocks_x = int(x)
        self.blocks_y = int(y)
        self.blocks_z = int(z)

    def set_build_mode(self,index):
        print ("\nFUNCTION: set_build_mode")
        iron_blocks = self.corners[index]['iron_blocks']
        iron_found = len(iron_blocks)
        mode = "default"
        if iron_found==1:
            mode="line"
        elif iron_found==2:
            mode="plane"
        elif iron_found==3:
            mode="hollow_cube"
        self.corners[index]['mode']=mode
        print ("mode == " + self.corners[index]['mode'])

    def builder(self,index):
        print ("\nFUNCTION: builder, index == " + str(index))
        self.g_loc = self.corners[index]['loc']
        self.delta_x = self.corners[index]['delta_x']
        self.delta_y = self.corners[index]['delta_y']
        self.delta_z = self.corners[index]['delta_z']
        mode = self.corners[index]['mode']
        self.to_x = self.g_loc[0]
        self.to_y = self.g_loc[1]
        self.to_z = self.g_loc[2]
        if mode=="line":
            self.build_line(index)
        elif mode=="plane":
            self.build_plane(index)
        elif mode=="hollow_cube":
            self.build_hollow_cube(index)

    def build_line(self, index):
        print ("\nFUNCTION: build_line")
        if (self.delta_x!=0):
            self.to_x = self.g_loc[0]+self.delta_x*self.blocks_x
        elif (self.delta_y!=0):
            self.to_y = self.g_loc[1]+self.delta_y*self.blocks_y
        elif (self.delta_z!=0):
            self.to_z = self.g_loc[2]+self.delta_z*self.blocks_z
        self.mc.setBlocks(self.g_loc[0],self.g_loc[1],self.g_loc[2],self.to_x,self.to_y,self.to_z,self.material_1)

    def build_plane(self, index):
        print ("\nFUNCTION: build_plane")
        if (self.delta_x!=0) and (self.delta_y!=0):
            self.to_x = self.g_loc[0]+self.delta_x*self.blocks_x
            self.to_y = self.g_loc[1]+self.delta_y*self.blocks_y
        elif (self.delta_x!=0) and (self.delta_z!=0):
            self.to_x = self.g_loc[0]+self.delta_x*self.blocks_x
            self.to_z = self.g_loc[2]+self.delta_z*self.blocks_z
        elif (self.delta_y!=0) and (self.delta_z!=0):
            self.to_y = self.g_loc[1]+self.delta_y*self.blocks_y
            self.to_z = self.g_loc[2]+self.delta_z*self.blocks_z
        self.mc.setBlocks(self.g_loc[0],self.g_loc[1],self.g_loc[2],self.to_x,self.to_y,self.to_z,self.material_1)

    def build_hollow_cube(self, index):
        print ("\nFUNCTION: build_hollow_cube")
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

    def define_demo_map3d(self, index):
        print ("\nFUNCTION: define_demo_map3d")
        self.map3d=[]
        self.map3d.append([])
        self.map3d.append([])
        self.map3d.append([])
        self.map3d.append([])
        self.map3d.append([])
        self.map3d.append([])
        self.map3d.append([])
        self.map3d[0].append([1,2,1,2,1])
        self.map3d[0].append([2,1,2,1,2])
        self.map3d[0].append([1,2,1,2,1])
        self.map3d[0].append([2,1,2,1,2])
        self.map3d[0].append([1,2,1,2,1])
        self.map3d[1].append([1,2,1,2,1])
        self.map3d[1].append([2,0,0,0,2])
        self.map3d[1].append([1,0,0,0,1])
        self.map3d[1].append([2,0,0,0,0])
        self.map3d[1].append([1,2,1,2,1])
        self.map3d[2].append([2,1,2,1,0])
        self.map3d[2].append([1,0,0,0,1])
        self.map3d[2].append([2,0,0,0,0])
        self.map3d[2].append([1,0,0,0,0])
        self.map3d[2].append([2,1,2,1,2])
        self.map3d[3].append([2,1,2,1,2])
        self.map3d[3].append([1,0,0,0,1])
        self.map3d[3].append([2,0,0,0,0])
        self.map3d[3].append([1,0,0,0,0])
        self.map3d[3].append([2,1,2,1,2])
        self.map3d[4].append([2,1,2,1,2])
        self.map3d[4].append([1,0,0,0,1])
        self.map3d[4].append([2,0,0,0,0])
        self.map3d[4].append([1,0,0,0,0])
        self.map3d[4].append([2,1,2,1,2])
        self.map3d[5].append([2,1,2,1,2])
        self.map3d[5].append([1,0,0,0,1])
        self.map3d[5].append([2,0,0,0,2])
        self.map3d[5].append([1,0,0,0,1])
        self.map3d[5].append([2,0,0,0,2])
        self.map3d[6].append([1,2,1,2,1])
        self.map3d[6].append([2,1,2,1,2])
        self.map3d[6].append([1,2,1,2,1])
        self.map3d[6].append([2,1,2,1,2])
        self.map3d[6].append([1,2,1,2,1])

    def define_demo_map2d(self, index):
        print ("\nFUNCTION: define_demo_map2d")
        self.map2d=[]
        self.map2d.append([1,2,1,2,1])
        self.map2d.append([2,1,2,1,2])
        self.map2d.append([1,2,1,2,1])
        self.map2d.append([2,1,2,1,2])
        self.map2d.append([1,2,1,2,1])

    def define_demo_map1d(self, index):
        print ("\nFUNCTION: define_demo_map1d")
        # WORKING
        self.map1d=[]
        self.map1d.append([1,2,3,4,5,4,3,2,1])

    def build_map1d(self, index):
        print ("\nFUNCTION: build_map1d")
        # WORKING

    def build_map2d(self, index):
        print ("\nFUNCTION: build_map2d")
        # WORKING: THIS CODE HAS NOT BEEN UPDATED!
        if (self.delta_x!=0) and (self.delta_y!=0):
            for x in range(0,len(self.map2d)-1):
                for y in range(0,len(self.map2d[x])-1):
                    print(str(x) + "x," + str(y) + "y," + str(self.map2d[x][y]))
                    block_x=self.g_loc[0]+self.delta_x*x
                    block_y=self.g_loc[1]+self.delta_y*y
                    block_z=self.g_loc[2]
                    self.mc.setBlock(block_x,block_y,block_z,self.map2d[x][y])
        elif (self.delta_x!=0) and (self.delta_z!=0):
            for x in range(0,len(self.map2d)-1):
                for z in range(0,len(self.map2d[x])-1):
                    block_x=self.g_loc[0]+self.delta_x*x
                    block_y=self.g_loc[1]
                    block_z=self.g_loc[2]+self.delta_z*z
                    self.mc.setBlock(block_x,block_y,block_z,self.map2d[x][z])
        elif (self.delta_y!=0) and (self.delta_z!=0):
            for y in range(0,len(self.map2d)-1):
                for z in range(0,len(self.map2d[y])-1):
                    block_x=self.g_loc[0]
                    block_y=self.g_loc[1]+self.delta_y*y
                    block_z=self.g_loc[2]+self.delta_z*z
                    self.mc.setBlock(block_x,block_y,block_z,self.map2d[y][z])

    def build_map3d(self,index):
        print ("\nFUNCTION: build_map3d")
        # WORKING: THIS CODE HAS NOT BEEN UPDATED
        for x in range(0,len(self.map3d)):
            for y in range(0,len(self.map3d[x])):
                for z in range(0,len(self.map3d[x][y])):
                    print(str(x)+"x,"+str(y)+"y,"+str(z)+"z")
                    block_x=self.g_loc[0]+self.delta_x*x
                    block_y=self.g_loc[1]+self.delta_y*y
                    block_z=self.g_loc[2]+self.delta_z*z
                    self.mc.setBlock(block_x,block_y,block_z,self.map3d[x][y][z])


        
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

