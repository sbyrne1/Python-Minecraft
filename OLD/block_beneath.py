from mcpi.minecraft import Minecraft

mc=Minecraft.create()
grass=2
diamond_block=57
while True:
    px,py,pz=mc.player.getPos()
    block_beneath=mc.getBlock(px,py-1,pz) # block ID
    #print(block_beneath)

    if block_beneath==grass:
        mc.setBlock(px,py-1,pz,diamond_block)
