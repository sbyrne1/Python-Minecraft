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
iron1_loc = [0,0,0]
iron2_loc = [0,0,0]
iron3_loc = [0,0,0]

gold_found = False

#find the gold
for gx in range (px-radius,px+radius):
    for gy in range (py-radius,py+radius):
        for gz in range (pz-radius,pz+radius):
            block = mc.getBlock(gx,gy,gz) # block ID
            if block == gold:
                g_loc = [gx,gy,gz]
                mc.postToChat(str(gx) + ", " + str(gy) + ", " + str(gz))

if (g_loc[0]!=0) or (g_loc[1]!=0) or (g_loc[2]!=0):
    gold_found = True
    mc.postToChat("Gold block located.")
else:
    mc.postToChat("Gold block was NOT located.")

#find the iron
iron_found = 0
card = [0,0,0,0,0,0]
if gold_found:
    bl_a=mc.getBlock(g_loc[0]+1,g_loc[1],g_loc[2])
    bl_b=mc.getBlock(g_loc[0]-1,g_loc[1],g_loc[2])
    bl_c=mc.getBlock(g_loc[0],g_loc[1]+1,g_loc[2])
    bl_d=mc.getBlock(g_loc[0],g_loc[1]-1,g_loc[2])
    bl_e=mc.getBlock(g_loc[0],g_loc[1],g_loc[2]+1)
    bl_f=mc.getBlock(g_loc[0],g_loc[1],g_loc[2]-1)


    
    for ix in range (g_loc[0]-radius,g_loc[0]+radius):
        for iy in range (g_loc[1]-radius,g_loc[1]+radius):
            for iz in range (g_loc[2]-radius,g_loc[2]+radius):
                block=mc.getBlock(ix,iy,iz) # block ID
                if block==iron:
                    iron_found = iron_found + 1
                    if iron_found == 1:
                        iron1_loc = [ix,iy,iz]
                        mc.postToChat("iron1 " + str(ix) + ", " + str(iy) + ", " + str(iz))
                    elif iron_found == 2:
                        iron2_loc = [ix,iy,iz]
                        mc.postToChat("iron2 " + str(ix) + ", " + str(iy) + ", " + str(iz))                        
                    elif iron_found == 3:
                        iron3_loc = [ix,iy,iz]
                        mc.postToChat("iron2 " + str(ix) + ", " + str(iy) + ", " + str(iz))
                    else:
                        mc.postToChat("That is a lot of iron cubes you have got there!")
                        
                        
mc.postToChat("iron_found==" + str(iron_found))

mode = "default"

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
    mode = "cube"

blocks_x = 5
blocks_y = 4
blocks_z = 3


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


elif mode == "cube":
    for wx in range (0,blocks_x):
        for wy in range (0,blocks_y):
            for wz in range (0,blocks_z):
                place_x=g_loc[0]+wx*delta_x
                place_y=g_loc[1]+wy*delta_y
                place_z=g_loc[2]+wz*delta_z
                mc.setBlock(place_x,place_y,place_z,0)
                                      
                                    


