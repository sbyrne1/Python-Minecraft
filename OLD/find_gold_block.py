from mcpi.minecraft import Minecraft

mc=Minecraft.create()

px,py,pz=mc.player.getPos()
px=int(px)
py=int(py)
pz=int(pz)

iron=42
gold=41

radius=2

gold_loc = [0,0,0]
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
                gold_loc = [gx,gy,gz]
                mc.postToChat(str(gx) + ", " + str(gy) + ", " + str(gz))

if (gold_loc[0]!=0) or (gold_loc[1]!=0) or (gold_loc[2]!=0):
    gold_found = True
    mc.postToChat("Gold block located.")
else:
    mc.postToChat("Gold block was NOT located.")

#find the iron
iron_found = 0
if gold_found:
    for ix in range (gold_loc[0]-radius,gold_loc[0]+radius):
        for iy in range (gold_loc[1]-radius,gold_loc[1]+radius):
            for iz in range (gold_loc[2]-radius,gold_loc[2]+radius):
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
    delta_x1 = gold_loc[0] - iron1_loc[0]
    delta_y1 = gold_loc[0] - iron1_loc[1]
    delta_z1 = gold_loc[0] - iron1_loc[2]
    mc.postToChat("delta_x1==" + str(delta_x1) + "delta_y1==" + str(delta_y1) + "delta_z1==" + str(delta_z1))
    mode = "single_line"
elif iron_found == 2:
    #build a plane/wall
    #ADD ERROR CHECKING HERE!
    delta_x1 = iron1_loc[0] - gold_loc[0] 
    delta_y1 = iron1_loc[1] - gold_loc[1]
    delta_z1 = iron1_loc[2] - gold_loc[2] 
    delta_x2 = iron2_loc[0] - gold_loc[0]
    delta_y2 = iron2_loc[1] - gold_loc[1] 
    delta_z2 = iron2_loc[2] - gold_loc[2] 
    delta_x = delta_x1+delta_x2
    delta_y = delta_y1+delta_y2
    delta_z = delta_z1+delta_z2
    mc.postToChat("delta_x==" + str(delta_x) + "delta_y==" + str(delta_y) + "delta_z==" + str(delta_z))
    mode = "plane"
elif iron_found == 3:
    delta_x1 = iron1_loc[0] - gold_loc[0] 
    delta_y1 = iron1_loc[1] - gold_loc[1]
    delta_z1 = iron1_loc[2] - gold_loc[2] 
    delta_x2 = iron2_loc[0] - gold_loc[0]
    delta_y2 = iron2_loc[1] - gold_loc[1] 
    delta_z2 = iron2_loc[2] - gold_loc[2]
    delta_x3 = iron3_loc[0] - gold_loc[0]
    delta_y3 = iron3_loc[1] - gold_loc[1] 
    delta_z3 = iron3_loc[2] - gold_loc[2]
    delta_x = delta_x1+delta_x2+delta_x3
    delta_y = delta_y1+delta_y2+delta_y3
    delta_z = delta_z1+delta_z2+delta_z3                                      
    mode = "cube"

blocks_x = 5
blocks_y = 50
blocks_z = 50

if mode == "plane":
    if (delta_x!=0) and (delta_y!=0):
        for wx in range (0,blocks_x):
            for wy in range (0,blocks_y):
                place_x=gold_loc[0]+wx*delta_x
                place_y=gold_loc[1]+wy*delta_y
                place_z=gold_loc[2]
                mc.setBlock(place_x,place_y,place_z,1)
    elif (delta_x!=0) and (delta_z!=0):
        for wx in range (0,blocks_x):
            for wz in range (0,blocks_z):
                place_x=gold_loc[0]+wx*delta_x
                place_y=gold_loc[1]
                place_z=gold_loc[2]+wz*delta_z
                mc.setBlock(place_x,place_y,place_z,1)
    elif (delta_y!=0) and (delta_z!=0):
        for wy in range (0,blocks_y):
            for wz in range (0,blocks_z):
                place_x=gold_loc[0]
                place_y=gold_loc[1]+wy*delta_y
                place_z=gold_loc[2]+wz*delta_z
                mc.setBlock(place_x,place_y,place_z,1)

elif mode == "cube":
    for wx in range (0,blocks_x):
        for wy in range (0,blocks_y):
            for wz in range (0,blocks_z):
                place_x=gold_loc[0]+wx*delta_x
                place_y=gold_loc[1]+wy*delta_y
                place_z=gold_loc[2]+wz*delta_z
                mc.setBlock(place_x,place_y,place_z,0)
                                      
                                    


