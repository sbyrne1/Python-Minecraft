from sense_hat import SenseHat
from time import sleep

sense = SenseHat()
sense.clear()
sense.low_light = True
board =[
  [1,1,1,1,1,1,1,1],
  [1,0,0,0,0,0,0,1],
  [1,0,0,1,0,0,0,1],
  [1,0,0,1,0,0,0,2],
  [1,0,0,1,0,0,0,1],
  [1,0,0,1,0,0,0,1],
  [1,0,0,0,0,0,0,1],
  [1,1,1,1,1,1,1,1]]

a_col = [0,0,0]
b_col = [0,255,0]
c_col = [255,0,0]
ball_col = [255,255,0]

ball = {'x': 1, 'y': 1}

class Pt:
    x = 0
    y = 0

    def __init__(self,_x,_y):
        self.x = _x
        self.y = _y

pt_current = Pt(1,1)
pt_past = Pt(1,1)

print(pt_past.x + " , " + pt_past.y)

# setup the board
for i in range(8):
    for j in range(8):
        b = board[i][j]
        if (b == 0):
            sense.set_pixel(i,j,a_col)
        elif (b == 1):
            sense.set_pixel(i,j,b_col)
        elif (b == 2):
            sense.set_pixel(i,j,c_col)
# initial player position
sense.set_pixel(ball['x'],ball['y'],ball_col)

def check_loc(pt):
    b = board[pt.x][pt.y]
    bx = ball['x']
    by = ball['y']
    if (b == 0):
        # 1 -- reset old location
        sense.set_pixel(ball['x'],ball['y'],a_col)
        # 2 -- move the ball
        ball['x'] = x
        ball['y'] = y
        print("move the ball!")
        return 0
    elif (b == 1):
        print("do not move the ball!")
        return 1
    elif (b == 2):
        print("you win!")
        return 2

def get_direction():
    if (event.action == 'pressed'):
        dire = event.direction
        bx = ball['x']
        by = ball['y']
        if (dire == "left"):
            bx-=1
        elif (dire == "right"):
            bx+=1
        elif (dire == "down"):
            by+=1
        elif (dire == "up"):
            by-=1
    return p = Pt(bx,by)
    

while True:   
    event = sense.stick.wait_for_event()
    get_direction()
    
    if (check_loc(bx,by)==2):
        break
    sleep(0.2)

sense.show_message("You Win!", scroll_speed=0.05, text_colour=[255,255,0], back_colour=[0,0,0])

