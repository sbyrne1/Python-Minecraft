from MinecraftGenerator import *

MINIMUM_BRICKS_TO_WORK = 1
SEARCH_RADIUS = 2

"""
    BlockFinder:
        Derived from MinecraftGenerator.
        Child is Builder.

"""
class BlockFinder(MinecraftGenerator):
    """
    Attributes:

    """

    def __init__(self):
        print ("\nFUNCTION: BlockFinder __init__")
        # instantiate parent
        MinecraftGenerator.__init__(self)

        self.corners = []
        self.set_radius(SEARCH_RADIUS)
        self.gold=41
        self.iron=42
        #TODO indentify class attributes.

    def new_corner(self):
        print ("\nFUNCTION: new_corner")
        loc = [0,0,0]
        scan_coords = []
        scan_blocks = []
        iron_blocks = []
        delta_x = 0
        delta_y = 0
        delta_z = 0
        mode = "default" # MOVE TO BUILDER
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

    #displays how many corners are available, and their location.
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
        if len(gold_bricks)==0:
            print("No gold bricks available.")
            return
        if len(gold_bricks)==MINIMUM_BRICKS_TO_WORK:
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

    def reset(self,MinecraftGenerator):
        #TODO reset members for new build.
        print ("\nFUNCTION: reset")

#End of BlockFinder class.
