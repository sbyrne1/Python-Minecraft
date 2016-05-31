from tkinter import *
from MinecraftGenerator import *

class App:
    def __init__(self,master):
        self.mine = MinecraftBuilder()
        frame=Frame(master)
        frame.pack()

        Label(frame,text='MINECRAFT ROOM GENERATOR').grid(row=0,columnspan=3)
        Button(frame,text='FIND GOLD',command=self.btn_findgold).grid(row=1,column=1)
        Label(frame,text='Blocks x').grid(row=2,column=0)
        self.x_var = IntVar()
        Entry(frame, textvariable=self.x_var).grid(row=2,column=1)
        Label(frame,text='Blocks y').grid(row=3,column=0)
        self.y_var = IntVar()
        Entry(frame, textvariable=self.y_var).grid(row=3,column=1)
        Label(frame,text='Blocks z').grid(row=4,column=0)
        self.z_var = IntVar()
        Entry(frame, textvariable=self.z_var).grid(row=4,column=1)
        Button(frame,text='RESET',command=self.btn_reset).grid(row=5,column=0)
        Button(frame,text='BUILD',command=self.btn_build).grid(row=5,column=1)
        Button(frame,text='QUIT',command=exit).grid(row=5,column=2)

        self.btn_reset()

    def btn_reset(self):
        self.reset_interface()
        self.mine.reset()

    def reset_interface(self):
        self.x_var.set(1)
        self.y_var.set(1)
        self.z_var.set(1)

    def btn_build(self):
        if (self.mine.mode != "default"):
            self.mine.set_dims(self.x_var.get(),self.y_var.get(),self.z_var.get())
            self.mine.set_materials(57,35,20,5,45,246)
            self.mine.builder()

    def btn_findgold(self):
        self.mine.find_gold()
        self.mine.set_build_mode()



root=Tk()
root.wm_title('RoomCraft')
app=App(root)
root.mainloop()



