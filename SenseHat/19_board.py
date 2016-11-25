from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()
sense.low_light = True

# Pt is used where x,y coordinates are defined
class Pt:
    x = 0
    y = 0
    
    def __init__(self,_x,_y):
        self.x = _x
        self.y = _y

class Board:
    # index of board_colors[][] correspond to board[][] values
    colors = [
        [0,0,0],
        [127,0,0],
        [0,127,0]]

    level = 0
    play_start = Pt(0,0)
    
    # 0 -> clear space
    # 1 -> wall
    # 2 -> goal
    # 3 -> player start
    plan =[[
        [1,0,0,0,0,0,0,1],
        [1,0,1,1,1,1,0,1],
        [1,0,0,0,0,1,0,1],
        [1,1,1,1,0,1,0,1],
        [1,2,1,1,3,1,0,1],
        [1,0,1,1,1,1,0,1],
        [1,0,0,0,0,0,0,1],
        [1,1,1,1,1,1,1,1],
        ],[
        [1,0,0,0,1,1,1,1],
        [1,3,1,0,1,0,0,2],
        [1,1,1,0,1,0,1,1],
        [0,0,0,0,1,0,0,1],
        [0,1,1,1,1,1,0,1],
        [0,1,0,0,0,1,0,1],
        [0,1,0,1,0,1,0,1],
        [0,0,0,1,0,0,0,1]
        ],[
        [0,0,0,1,1,1,1,1],
        [0,1,0,1,1,0,0,2],
        [0,1,0,1,1,0,1,1],
        [0,1,0,3,1,0,0,1],
        [0,1,1,1,1,1,0,1],
        [0,1,0,0,0,1,0,1],
        [0,1,0,1,0,1,0,1],
        [0,0,0,1,0,0,0,1]
        ],[
        [0,1,0,0,1,1,1,1],
        [0,1,0,1,1,0,0,0],
        [0,0,0,1,1,0,1,1],
        [0,1,0,3,1,2,0,1],
        [0,1,1,1,1,1,0,0],
        [0,1,0,0,0,1,0,1],
        [0,1,0,1,0,1,0,1],
        [0,0,0,1,0,0,0,1]
        ]]

    def level_up(self):
        self.level += 1


        # test for end of array
        if (self.level > len(self.plan) - 1):
            self.level = 0

    def draw(self):
        for i in range(8):
            for j in range(8):
                pixel = self.plan[self.level][i][j]
                if (pixel != 3):
                    sense.set_pixel(i,j,self.colors[pixel])
                else:
                    self.play_start = Pt(i,j)
                    print("play_start!")

    def __init__(self):
        print(len(self.plan))
        self.draw()

    max_x = 7
    min_x = 0
    max_y = 7
    min_y = 0
    
    def get_pt(self,_pt):
        if ((_pt.x > self.max_x) or (_pt.x < self.min_x) or (_pt.y > self.max_y) or (_pt.y < self.min_y)):
            return 1 # if out of bounds, treat as a 
        else:
            return self.plan[self.level][_pt.x][_pt.y]

class Player(Pt):
    color = [255,255,0]
    blank = [0,0,0]

    def draw(self):
        sense.set_pixel(self.x,self.y,self.color)

    def clear(self):
        sense.set_pixel(self.x,self.y,self.blank)

    def set_pos(self,_pt):
        self.x = _pt.x
        self.y = _pt.y
        self.draw()

    def move(self,_pt):
        self.clear()
        self.set_pos(_pt)
        
    def __init__(self,_pt):
        Pt.__init__(self,_pt.x,_pt.y)
        self.draw()
        
#play = Player(1,1)
#print(str(play.x) + " , " + str(play.y))

class Control():
    sense.show_message("Level 1", scroll_speed=0.05, text_colour=[255,255,0], back_colour=[0,0,0])
    sleep(1.5)
    boa = Board()
    play = Player(boa.play_start)
    def __init__(self):
        print("control")
        self.loop()

    def get_next(self,_pt,_direction): # _pt is a Pt object
        a = _pt # new point
        if (_direction == "left"):
            a.x -= 1
        elif (_direction == "right"):
            a.x += 1
        elif (_direction == "down"):
            a.y += 1
        elif (_direction == "up"):
            a.y -= 1
        return a # return new point
    
    def loop(self):
        win = False
        
        while (not win):
            event = sense.stick.wait_for_event()
            if (event.action == 'pressed'):
                b = self.get_next(Pt(self.play.x,self.play.y),event.direction)
                print(str(b.x) + " , " + str(b.y))
                test = self.boa.get_pt(b)
                print(test)
                if (test == 0):  # clear space, move player
                    print('clear space, move player')
                    self.play.move(b)
                if (test == 1):  # wall space, don't move player
                    print('wall space, do not move player')
                    self.play.clear()
                    self.play.move(self.boa.play_start)
                if (test == 2):  # win state
                    print('win state')
                    sense.clear()
                    self.boa.level_up()
                    level = self.boa.level + 1
                    if (level != 1):
                        message = "Level " + str(level)
                    else:
                        message = "You win!"
                    sense.show_message(message, scroll_speed=0.05, text_colour=[255,255,0], back_colour=[0,0,0])
                    sleep(1.5)            # show message for 3 seconds
                    self.boa.draw()     # draw board
                    self.play.set_pos(self.boa.play_start) # reset player position

cont = Control()

