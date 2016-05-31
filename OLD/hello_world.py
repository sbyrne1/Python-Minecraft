from mcpi.minecraft import Minecraft

mc=Minecraft.create()

mc.postToChat("Hello world")

x,y,z=mc.player.getPos()
mc.postToChat(z)
#teleport!
mc.player.setPos(x,y+50,z)
