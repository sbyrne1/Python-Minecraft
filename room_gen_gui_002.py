from tkinter import *
import Builder

class App:
    def __init__(self,master):
        print ("room_gen_gui_002.py")
        print ("\nGUI FUNCTION: __init__")
        self.builder = Builder()
        frame=Frame(master)
        frame.pack()

        Label(frame,text='MINECRAFT ROOM GENERATOR').grid(row=0,columnspan=3)

        Button(frame,text='SET CORNER',command=self.btn_findgold).grid(row=1,column=1)
        Label(frame,text='Blocks x').grid(row=2,column=0)
        self.x_var = IntVar()
        Entry(frame, textvariable=self.x_var).grid(row=2,column=1)
        Label(frame,text='Blocks y').grid(row=3,column=0)
        self.y_var = IntVar()
        Entry(frame, textvariable=self.y_var).grid(row=3,column=1)
        Label(frame,text='Blocks z').grid(row=4,column=0)
        self.z_var = IntVar()
        Entry(frame, textvariable=self.z_var).grid(row=4,column=1)

        Button(frame,text='LIST',command=self.btn_list).grid(row=5,column=0)

        Button(frame,text='BUILD',command=self.btn_build).grid(row=5,column=1)

        Button(frame,text='QUIT',command=exit).grid(row=5,column=2)

        self.reset_interface()

    def btn_list(self):
        print ("\nGUI FUNCTION: btn_list")
        self.builder.print_corners()

    def reset_interface(self):
        print ("\nGUI FUNCTION: reset_interface")
        self.x_var.set(1)
        self.y_var.set(1)
        self.z_var.set(1)

    def btn_build(self):
        print ("\nGUI FUNCTION: btn_build")
        #TODO is 'index' a member of room_gen_gui_002???
        index = 0 #TODO 'index' doesn't seem to be a variable, does the user interact with it?
        self.builder.set_build_mode(index)
        mode = self.builder.get_mode(index) #NOTE may not need to pass index to get_mode.
        if (mode != "default"):
            self.builder.set_dims(self.x_var.get(),self.y_var.get(),self.z_var.get())
            self.builder.set_materials(57,35,20,5,45,246)
            #TODO put a list of constant variables with the names of the materials at the top.
            # NOTE: THE FOLLOWING HARDCODES THE BUILD TO HAPPEN AT THE FIRST
            # DEFINED CORNER
            self.builder.builder(index)

    def btn_findgold(self):
        print ("\nGUI FUNCTION: btn_findgold")
        self.builder.find_gold()

root=Tk()
root.wm_title('RoomCraft')
app=App(root)
root.mainloop()
