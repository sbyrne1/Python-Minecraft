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

    play = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,3,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]]

    # players position on play[][]
    play_pos = Pt(3,3)
    # players postion on plan[][][]
    plan_pos = Pt(5,5)

    def set_offset(self, _pt1, _pt2):
        x_offset = _pt2.x - _pt1.x
        y_offset = _pt2.y - _pt1.y
        offset_pt = Pt(x_offset, y_offset) 
        return offset_pt

    plan =[[
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,1,1,1,0,1,1,1,1,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,2],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        ],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,1,1,1,1,0,1,1,1,1,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,1,1,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,1,1,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,0,0,0,0,0,0,0,0,1,0,0,1],
        [1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

    def pop_play(self):
        print("pop_play")
        offset = self.set_offset(self.play_pos, self.plan_pos)
        for x in range(8):
            for y in range(8):
                plan_x = offset.x + x
                plan_y = offset.y + y
                plan_addy = Pt(offset.x + x, offset.y + y)
                x_size = len(self.plan[self.level])
                y_size = len(self.plan[self.level][0])
                if ( ((plan_x >= 0) and (plan_y >= 0)) and ((plan_x < x_size) and (plan_y < y_size)) ):
                    self.play[x][y] = self.plan[self.level][plan_x][plan_y]
                else:
                    self.play[x][y] = 1
        play_x = self.play_pos.x
        play_y = self.play_pos.y
        self.play[play_x][play_y]=3
        self.draw()

    def find_spawn(self):
        x_len = len(self.plan[self.level])
        y_len = len(self.plan[self.level][0])
        for x in range(x_len):
            for y in range(y_len):
                if (self.plan[self.level][x][y] == 4):
                    self.play_pos.set_pt(x,y)
                    break
                            
    def level_up(self):
        self.level += 1
        # test for end of array
        if (self.level > len(self.plan) - 1):
            self.level = 0

    def set_led(self, _pt, _color):
        sense.set_pixel(_pt.x, _pt.y, self.colors[_color])
        self.play[_pt.x][_pt.y] = _color        
    
    def draw(self):
        for x in range(8):
            for y in range(8):
                pixel = self.play[x][y]
                self.set_led(Pt(x,y), pixel)

    def __init__(self):
        self.pop_play()
        self.draw()

class Control():
    boa = Board()

    def __init__(self):
        print("control")
        self.loop()

    '''def get_next(self,_pt,_direction): # _pt is a Pt object
        a = _pt # new point
        
        return a # return new point'''

    def pt_delta(self,_direction):
        change = Pt(0,0)
        if (_direction == "left"):
            change.x -= 1
        elif (_direction == "right"):
            change.x += 1
        elif (_direction == "down"):
            change.y += 1
        elif (_direction == "up"):
            change.y -= 1
        return change

    def add_pts(self,_pt1,_pt2):
        new_pt = Pt(_pt1.x+_pt2.x,_pt1.y+_pt2.y)
        return new_pt

    def loop(self):
        win = False
        
        while (not win):
            event = sense.stick.wait_for_event()
            if (event.action == 'pressed'):
                x = self.boa.play_pos.x
                y = self.boa.play_pos.y
                old_pos = Pt(x,y)
                delta = self.pt_delta(event.direction)
                new_pos = self.add_pts(old_pos, delta)
                new_square = self.boa.play[new_pos.x][new_pos.y]
                if(new_square == 0):
                    print(0)
                    if( ((new_pos.x == 3) or (new_pos.x == 4)) and ((new_pos.y == 3) or (new_pos.y == 4)) ):
                        print("MOVE PLAYER")
                        # overwrite old position with color 0
                        self.boa.set_led(old_pos, 0)
                        # overwite new position with color 3
                        self.boa.set_led(new_pos, 3)
                        # move player to new location
                        self.boa.play_pos = new_pos
                        self.boa.play[new_pos.x][new_pos.y] == 3
                    else:
                        print("MOVE BOARD")
                        # change plan_pos instead of play_pos
                        self.boa.plan_pos = self.add_pts(self.boa.plan_pos, delta)
                        test = "---" + str(self.boa.plan_pos.x) + ", " + str(self.boa.plan_pos.y)
                        print (test)
                        # regenerate play from plan
                        self.boa.pop_play()
                        # self.boa.play_pos = old_pos   
                elif(new_square == 1):
                    print("YOU HIT A WALL, RETURN TO BEGINNING!")
                elif(new_square == 2):
                    print("LEVEL EXIT")
                    
cont = Control()

