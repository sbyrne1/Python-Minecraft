from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()
sense.low_light = True

# Pt is used where x,y coordinates are defined
class Pt:
    x = 0
    y = 0

    def set_pt(self,_x,_y):
        self.x = _x
        self.y = _y

    def add_pts(self,_pt1,_pt2):
        self.set_pt(_pt1.x+_pt2.x,_pt1.y+_pt2.y)

    def sub_pts(self,_pt1,_pt2):
        self.set_pt(_pt1.x-_pt2.x,_pt1.y-_pt2.y)
    
    def __init__(self,_x,_y):
        self.set_pt(_x,_y)

class Board:
    # colors correspond to play[][] values
    colors = [[0,0,0],[127,0,0],[0,127,0],[127,127,0]]
    
    level = 0 

    mini = Pt(0,0) # minimum values
    maxi = Pt(7,7) # maximum values

    # 0 -> clear space
    # 1 -> wall
    # 2 -> goal
    # 3 -> players current position
    # 4 -> player spawn
    
    # play[][] is used for display purposes
    play = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]]

    # players position on play[][]
    play_pos = Pt(3,3)
    # players postion on plan[][][]
    plan_pos = Pt(0,0)

    # plan[level][][] stores level maps
    plan =[[
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,4,1,1,1,1,0,1,1,1,1,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,0,0,1,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],[
        [1,1,1,1,1,1,0,2],
        [1,1,1,1,1,1,0,1],
        [1,1,1,1,1,1,0,1],
        [0,0,0,0,0,1,0,1],
        [1,1,1,1,0,1,0,1],
        [0,0,0,1,0,1,0,1],
        [1,1,0,1,0,1,0,1],
        [1,1,0,1,0,1,0,1],
        [1,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,0],
        [1,4,1,0,0,0,1,0],
        [1,0,1,0,1,0,1,0],
        [1,0,0,0,1,0,0,0],
        [1,1,1,1,1,1,1,1]
        ]]

    def test_bounds(self,max_x,max_y,_x,_y):
        if ( (_x >= 0) and (_y >= 0) and (_x < max_x) and (_y < max_y) ):
            #print("test_bounds: True")
            return True
        else:
            #print("test_bounds: False")
            return False      

    def print_plan(self):
        test = "Level " + str(self.level)
        print(test)
        test = "plan[" + str(self.level) + "][" + str(len(self.plan[self.level])) + "][" + str(len(self.plan[self.level][0])) + "]"
        print(test)
        for i in range(len(self.plan[self.level])):
            print(self.plan[self.level][i])
        print("")
            
    def print_play(self):
        # print_play() is for testing purposes
        test = "play_pos==" + str(self.play_pos.x) + ", " + str(self.play_pos.y)
        print(test)
        test = "plan_pos==" + str(self.plan_pos.x) + ", " + str(self.plan_pos.y)
        print(test)
        print("play[" + str(len(self.play)) + "][" + str(len(self.play[0])) + "]")
        for i in range(8):
            print(self.play[i])
        
    
    # populates play. this is used whenever the board moves
    def pop_play(self):
        print("pop_play()")
        offset = Pt(0,0)
        offset.sub_pts(self.plan_pos,self.play_pos)
        test = "offset==" + str(offset.x) + ", " + str(offset.y)
        print(test)
        x_len = len(self.plan[self.level])   # get dimension of plan[level] (x)
        y_len = len(self.plan[self.level][0])  # get dimension of plan[level][] (y)
        for x in range(len(self.play)):
            for y in range(len(self.play[0])):
                plan_x = offset.x + x 
                plan_y = offset.y + y
                if (self.test_bounds(x_len,y_len,plan_x,plan_y)):
                    if (self.plan[self.level][plan_x][plan_y] == 4):
                        self.play[x][y]=0
                    else:
                        self.play[x][y] = self.plan[self.level][plan_x][plan_y]
                else:
                    self.play[x][y] = 1 # interpret display space as a wall if out of bounds
        self.play[self.play_pos.x][self.play_pos.y]=3 # place the player in play[][]
        self.print_play() # print debug information to console
        self.draw()

    def find_spawn(self):
        print("find_spawn()")
        for x in range(len(self.plan[self.level])):
            for y in range(len(self.plan[self.level][0])):
                if (self.plan[self.level][x][y] == 4):
                    self.plan_pos.set_pt(x,y)
                    self.plan[self.level][x][y] == 0 # space is treated as a blank 
                    break
                            
    def level_up(self):
        print("level_up()")
        self.level += 1
        # test for end of array
        if (self.level > len(self.plan) - 1):
            self.level = 0
        self.find_self()
        self.print_plan()

    def set_led(self, _pt, _color):
        if ((_color < 0) or (_color >= len(self.colors))):
            # if no color in array
            _color = 0 # make pixel blank
        sense.set_pixel(_pt.x, _pt.y, self.colors[_color])
        self.play[_pt.x][_pt.y] = _color        
    
    def draw(self):
        print("draw()")
        for x in range(8):
            for y in range(8):
                pixel = self.play[x][y]
                self.set_led(Pt(x,y), pixel)

    def find_self(self):
        print("find_self()")
        self.play_pos.set_pt(3,3)       # reset play_pos
        self.find_spawn()            # sets plan_pos

    
    def __init__(self):
        print("Board.__init__()")
        self.find_self()
        self.print_plan()
        self.pop_play()

class Control():
    boa = Board()
    step = 0
    def __init__(self):
        print("Control.__init__()")
        self.loop()

    def move_delta(self,_dir):
        delta = Pt(0,0)
        print("")
        print("move_delta(" + _dir + ")")
        print("step " + str(self.step))
        self.step += 1
        if (_dir == "left"):
            delta.x -= 1
        elif (_dir == "right"):
            delta.x += 1
        elif (_dir == "down"):
            delta.y += 1
        elif (_dir == "up"):
            delta.y -= 1
        elif (_dir == "middle"):
            print("button click")
        return delta

    def loop(self):
        print("loop()")
        win = False
        
        while (not win):
            event = sense.stick.wait_for_event()
            if (event.action == 'pressed'):
                old_pos = Pt(self.boa.play_pos.x,self.boa.play_pos.y)
                delta = self.move_delta(event.direction)
                new_pos = Pt(0,0)
                new_pos.add_pts(old_pos, delta)
                new_plan = Pt(0,0)
                new_plan.add_pts(self.boa.plan_pos, delta)
                # new_square is the value of the square the player wishes to walk into
                new_square = self.boa.play[new_pos.x][new_pos.y]
                if(new_square == 0):
                    if( ((new_pos.x == 3) or (new_pos.x == 4)) and ((new_pos.y == 3) or (new_pos.y == 4)) ):
                        #player is within the four center squares
                        print("MOVE PLAYER")
                        self.boa.set_led(old_pos, 0)    # overwrite old position with color 0
                        self.boa.set_led(new_pos, 3)    # overwite new position with color 3
                        # move player to new location in play 
                        self.boa.play_pos = new_pos     # change player position
                        self.boa.plan_pos = new_plan    # change plan position
                        self.boa.play[new_pos.x][new_pos.y] == 3
                        self.boa.print_play()
                    else:
                        print("MOVE BOARD")
                        # change plan_pos instead of play_pos
                        new_plan = Pt(0,0)
                        new_plan.add_pts(self.boa.plan_pos, delta)
                        print("delta == " + str(delta.x) + ", " + str(delta.y))
                        test = "new_plan==" + str(new_plan.x) + ", " + str(new_plan.y)
                        print(test)
                        self.boa.plan_pos = new_plan
                        # regenerate play from plan
                        self.boa.pop_play()
                        # self.boa.play_pos = old_pos   
                elif(new_square == 1):
                    print("YOU HIT A WALL,!")
                elif(new_square == 2):
                    print("LEVEL EXIT")
                    sense.clear()
                    self.boa.level_up()
                    if (self.boa.level != 0):
                        message = "Level " + str(self.boa.level+1)
                    else:
                        message = "You win!"
                    sense.show_message(message, scroll_speed=0.05, text_colour=[255,255,0], back_colour=[0,0,0])
                    sleep(1.5)
                    self.boa.pop_play()
                    
                    
cont = Control()

