import BlockFinder

LINE_SETTING = 1
PLANE_SETTING = 2
HOLLOW_CUBE_SETTING = 3

"""
    Builder:
        Derived from BlockFinder.

"""
class Builder(BlockFinder):
    """
    Attributes:

    """
    def __init__(self):
        print ("\nFUNCTION: Builder __init__")
        #instantiate parent.
        BlockFinder.__init__(self)
        self.set_materials()
        self.set_dims(10,30,10)
        #TODO indentify class attributes.

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
        if iron_found==LINE_SETTING:
            mode="line"
        elif iron_found==PLANE_SETTING:
            mode="plane"
        elif iron_found==HOLLOW_CUBE_SETTING:
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

    def build_line(self, index):#??? Uses mc instance.
        #TODO indentify why 'index' is an argument, it is unused.
        print ("\nFUNCTION: build_line")
        if (self.delta_x!=0):
            self.to_x = self.g_loc[0]+self.delta_x*self.blocks_x
        elif (self.delta_y!=0):
            self.to_y = self.g_loc[1]+self.delta_y*self.blocks_y
        elif (self.delta_z!=0):
            self.to_z = self.g_loc[2]+self.delta_z*self.blocks_z
        self.mc.setBlocks(self.g_loc[0],self.g_loc[1],self.g_loc[2],self.to_x,self.to_y,self.to_z,self.material_1)

    def build_plane(self, index): #??? Uses mc instance.
        #TODO indentify why 'index' is an argument, it is unused.
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

    def build_hollow_cube(self, index): #??? Uses mc instance.
        #TODO indentify why 'index' is an argument, it is unused.
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
        #TODO indentify why 'index' is an argument, it is unused.
        print ("\nFUNCTION: define_demo_map3d")
        self.map3d=[]

        #comment out the for-loop if it doesn't work.
        for x in range(7):
            self.map3d.append([])

        """#uncomment block comment if the for-loop doesn't work.
        self.map3d.append([])
        self.map3d.append([])
        self.map3d.append([])
        self.map3d.append([])
        self.map3d.append([])
        self.map3d.append([])
        self.map3d.append([])
        """

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
        #TODO indentify why 'index' is an argument, it is unused.
        print ("\nFUNCTION: define_demo_map2d")
        self.map2d=[]
        self.map2d.append([1,2,1,2,1])
        self.map2d.append([2,1,2,1,2])
        self.map2d.append([1,2,1,2,1])
        self.map2d.append([2,1,2,1,2])
        self.map2d.append([1,2,1,2,1])

    def define_demo_map1d(self, index):
        #TODO indentify why 'index' is an argument, it is unused.
        print ("\nFUNCTION: define_demo_map1d")
        # WORKING
        self.map1d=[]
        self.map1d.append([1,2,3,4,5,4,3,2,1])

    def build_map1d(self, index):
        #TODO indentify why 'index' is an argument, it is unused.
        print ("\nFUNCTION: build_map1d")
        # WORKING

    def build_map2d(self, index): #??? Uses mc instance.
        #TODO indentify why 'index' is an argument, it is unused.
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

    def build_map3d(self,index): #??? Uses mc instance.
        #TODO indentify why 'index' is an argument, it is unused.
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

    def reset (self, BlockFinder):
        #TODO reset members for new build.
#End of builder class.
