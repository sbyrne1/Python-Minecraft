from mcpi.minecraft import Minecraft

mc=Minecraft.create()

px,py,pz=mc.player.getPos()
px=int(px)
py=int(py)
pz=int(pz)

iron=42
gold=41

radius=2

g_loc = [0,0,0]
g_scan_keys = []
g_scan_blocks = []
iron1_loc = [0,0,0]
iron2_loc = [0,0,0]
iron3_loc = [0,0,0]

gold_found = False
mode = "default"
#find the gold
for gx in range (px-radius,px+radius):
    for gy in range (py-radius,py+radius):
        for gz in range (pz-radius,pz+radius):
            block = mc.getBlock(gx,gy,gz) # block ID
            if block == gold:
                g_loc = [gx,gy,gz]
                gold_found = True
                mc.postToChat(str(gx) + ", " + str(gy) + ", " + str(gz))

if gold_found:
    mc.postToChat("Gold block located.")
else:
    mc.postToChat("Gold block was NOT located.")

#scan the blocks surrounding the gold cube
iron_found = 0
if gold_found:
    # make a list of lists of x,y,z locations around the gold cube
    for iy in range (-1,2):
        for ix in range (-1,2):
            for iz in range (-1,2):
                g_scan_keys.append([g_loc[0] + ix, g_loc[1] + iy, g_loc[2] + iz])    
    # make a corresponding list of block types
    for ai in range (0,27):
        jx = g_scan_keys[ai][0]
        jy = g_scan_keys[ai][1]
        jz = g_scan_keys[ai][2]
        block_id = mc.getBlock(jx,jy,jz) # block ID
        g_scan_blocks.append(block_id)
    # find iron bricks
    for bi in range (0,27):
        if g_scan_blocks[bi] == iron:
            iron_found = iron_found+1
            if iron_found == 1:
                iron1_loc = g_scan_keys[bi]
            elif iron_found == 2:
                iron2_loc = g_scan_keys[bi]                       
            elif iron_found == 3:
                iron3_loc = g_scan_keys[bi]
            else:
                mc.postToChat("That is a lot of iron cubes you have got there!")

if iron_found == 1:
    #calculate delta x, y and z
    delta_x = iron1_loc[0] - g_loc[0] 
    delta_y = iron1_loc[1] - g_loc[1]
    delta_z = iron1_loc[2] - g_loc[2]
    mc.postToChat("delta_x==" + str(delta_x) + "delta_y==" + str(delta_y) + "delta_z==" + str(delta_z))
    mode = "line"
elif iron_found == 2:
    #build a plane/wall
    #ADD ERROR CHECKING HERE!
    delta_x1 = iron1_loc[0] - g_loc[0] 
    delta_y1 = iron1_loc[1] - g_loc[1]
    delta_z1 = iron1_loc[2] - g_loc[2] 
    delta_x2 = iron2_loc[0] - g_loc[0]
    delta_y2 = iron2_loc[1] - g_loc[1] 
    delta_z2 = iron2_loc[2] - g_loc[2] 
    delta_x = delta_x1+delta_x2
    delta_y = delta_y1+delta_y2
    delta_z = delta_z1+delta_z2
    mc.postToChat("delta_x==" + str(delta_x) + "delta_y==" + str(delta_y) + "delta_z==" + str(delta_z))
    mode = "plane"
elif iron_found == 3:
    delta_x1 = iron1_loc[0] - g_loc[0] 
    delta_y1 = iron1_loc[1] - g_loc[1]
    delta_z1 = iron1_loc[2] - g_loc[2] 
    delta_x2 = iron2_loc[0] - g_loc[0]
    delta_y2 = iron2_loc[1] - g_loc[1] 
    delta_z2 = iron2_loc[2] - g_loc[2]
    delta_x3 = iron3_loc[0] - g_loc[0]
    delta_y3 = iron3_loc[1] - g_loc[1] 
    delta_z3 = iron3_loc[2] - g_loc[2]
    delta_x = delta_x1+delta_x2+delta_x3
    delta_y = delta_y1+delta_y2+delta_y3
    delta_z = delta_z1+delta_z2+delta_z3                                      
    mode = "hollow_cube"

blocks_x = 20
blocks_y = 15
blocks_z = 30


if mode == "line":
    # set defaults
    to_x = g_loc[0]
    to_y = g_loc[1]
    to_z = g_loc[2]  
    if (delta_x!=0):
        to_x = g_loc[0]+delta_x*blocks_x
    elif (delta_z!=0):
        to_z = g_loc[2]+delta_z*blocks_z
    elif (delta_y!=0):
        to_y = g_loc[1]+delta_y*blocks_y
    mc.setBlocks(g_loc[0],g_loc[1],g_loc[2],to_x,to_y,to_z,1) 
    

elif mode == "plane":
    # set defaults
    to_x = g_loc[0]
    to_y = g_loc[1]
    to_z = g_loc[2]  
    if (delta_x!=0) and (delta_y!=0):
        to_x = g_loc[0]+delta_x*blocks_x
        to_y = g_loc[1]+delta_y*blocks_y           
    elif (delta_x!=0) and (delta_z!=0):
        to_x = g_loc[0]+delta_x*blocks_x 
        to_z = g_loc[2]+delta_z*blocks_z
    elif (delta_y!=0) and (delta_z!=0):
        to_y = g_loc[1]+delta_y*blocks_y
        to_z = g_loc[2]+delta_z*blocks_z
    mc.setBlocks(g_loc[0],g_loc[1],g_loc[2],to_x,to_y,to_z,1)        


elif mode == "hollow_cube":
    to_x = g_loc[0]+delta_x*blocks_x
    to_y = g_loc[1]+delta_y*blocks_y
    to_z = g_loc[2]+delta_z*blocks_z
    # replace cube space with air (just in case we are building into a hill)
    mc.setBlocks(g_loc[0],g_loc[1],g_loc[2],to_x,to_y,to_z,0)
    # make the floor
    mc.setBlocks(g_loc[0],g_loc[1],g_loc[2],to_x,g_loc[1],to_z,5)
    # make 4 walls
    mc.setBlocks(g_loc[0],g_loc[1]+1*delta_y,g_loc[2],to_x,to_y,g_loc[2],20) # A to D
    mc.setBlocks(to_x,g_loc[1]+1*delta_y,g_loc[2],to_x,to_y,to_z,45) # D to C
    mc.setBlocks(to_x,g_loc[1]+1*delta_y,to_z,g_loc[0],to_y,to_z,1) # B to C
    mc.setBlocks(g_loc[0],g_loc[1]+1*delta_y,to_z,g_loc[0],to_y,g_loc[2],20) # B to A
    # make a ceiling
    mc.setBlocks(g_loc[0],to_y,g_loc[2],to_x,to_y,to_z,1)
  
