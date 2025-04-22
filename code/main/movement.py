import time
import board # type: ignore
from adafruit_motor import stepper # type: ignore
from adafruit_motorkit import MotorKit # type: ignore
from tqdm import tqdm
import busio # type: ignore
from adafruit_pca9685 import PCA9685 # type: ignore
from adafruit_motor import servo # type: ignore

from constans import Constants
from keys import Keys

Cons = Constants()
Key_c = Keys()


class Movement():
    def __init__(self):
        
        self.kit = MotorKit(i2c=board.I2C())

        self.s_x = self.kit.stepper1
        self.s_y = self.kit.stepper2
        self.sleep = .03

        self.i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(self.i2c)
        self.pca.frequency = 40

        self.hand = servo.Servo(self.pca.channels[0])


    
    def open(self):
        self.hand.angle = 30
    def colse(self):
        self.hand.angle = 0
    
    def release(self) -> None:
        self.s_x.release() # release to prevent overheat
        self.s_y.release()
    
    def move(self, x_moveby: int, y_moveby: int):

        if 0 <= (Cons.Pos.s_x + x_moveby) <= Cons.Pos.s_x_max:
            print("move X pos: OK")
        else:
            print("move X unable: ERROR")
            return


        if 0 <= (Cons.Pos.s_y + y_moveby) <= Cons.Pos.s_y_max:
            print("move Y pos: OK")
        else:
            print("move Y unable: ERROR")
            return


        if x_moveby >= 0:
            x_dir = stepper.FORWARD
            x_dir_i = 1

        else:
            x_dir = stepper.BACKWARD
            x_moveby *= -1
            x_dir_i = -1


        if y_moveby >= 0:
            y_dir = stepper.FORWARD
            y_dir_i = 1

        else:
            y_dir = stepper.BACKWARD
            y_moveby *= -1
            y_dir_i = -1

        x_progress = tqdm(total=x_moveby, desc="X move Progress")
        y_progress = tqdm(total=y_moveby, desc="Y move Progress")

        # combine x and y movement:
        while x_moveby >= 1 and y_moveby >= 1:
            
            self.s_x.onestep(direction=x_dir)
            time.sleep(self.sleep / 2) # wait 1/2 of waiting cycle

            self.s_y.onestep(direction=y_dir)

            x_progress.update(1)
            y_progress.update(1)

            x_moveby -= 1
            y_moveby -= 1

            Cons.Pos.s_x += x_dir_i # update location +1 if pos else -1
            Cons.Pos.s_y += y_dir_i

            time.sleep(self.sleep / 2)  # finsh the waiting cycle
        
        #  move the rest 
        if x_moveby >= y_moveby:
            x_left = x_moveby - y_moveby

            for _ in range(x_left):
                self.s_x.onestep(direction=x_dir)

                x_progress.update(1)

                Cons.Pos.s_x += x_dir_i

                time.sleep(self.sleep)

        else:
            y_left = y_moveby - x_moveby

            for _ in range(y_left):
                self.s_y.onestep(direction=y_dir)

                y_progress.update(1)

                Cons.Pos.s_y += y_dir_i

                time.sleep(self.sleep)
        

                

    def move_to(self, target_x: int, target_y: int):
        x_moveby = target_x - Cons.Pos.s_x
        y_moveby = target_y - Cons.Pos.s_y

        # check if move possible

        x_next = Cons.Pos.s_x + x_moveby  # maybe -?? but i dont think so
        y_next = Cons.Pos.s_y + y_moveby

        if 0 <= x_next <= Cons.Pos.s_x_max and 0 <= y_next <= Cons.Pos.s_y_max:
            print("move possible, proceeding...")
        else:
            print("next move calced in minus: ERROR")
            print("aborting...")
            return  # exit move funtion
        
        return x_moveby, y_moveby
        


    def move_to_piece(self, x: int, y: int):
        #x
        move_range_x = Cons.Pos.s_x_max - Cons.Pos.x_start_offset - Cons.Pos.x_end_offset
        piece_x = move_range_x / Cons.cols #cols = 15  - calculate the steps rq for one tile

        move_range_y = Cons.Pos.s_y_max - Cons.Pos.y_start_offset - Cons.Pos.y_end_offset
        piece_y = move_range_y / Cons.rows #rows = 12 ( 10 + 2)

        # add starting offset

        # reverse the x and y 

        

        piece_x_pos = ((piece_x) * (Cons.cols - x)) + Cons.Pos.x_start_offset

        piece_x_pos += piece_x / 2  # add 1/2 of the tile to be in the middle

        piece_y_pos = round((piece_y * (Cons.rows - y)) + Cons.Pos.y_start_offset)
        
        piece_y_pos += piece_y / 2 # add 1/2 of the tile to be in the middle

        return round(piece_x_pos), round(piece_y_pos)


    def MaualMovement(self, key: int, amt=5):

        action = Key_c.MANUAL_MOVMENT.index(key)
        """
        0 = x+
        1 = x-
        2 = Y+
        3 = Y-
        """

        if action == 0:
            self.move(amt, 0)
            print("moving x+")
        elif action == 1:
            self.move(-1 * amt, 0)
            print("moving x-")
        elif action == 2:
            self.move(0, amt)
            print("moving y+")
        elif action == 3: 
            self.move(0, amt * -1)
            print("moving y-")

        print("current X Y pos:")
        print(f"{Cons.Pos.s_x} | {Cons.Pos.s_y}")


    def manual(self):
        print("entering maual movement...")
        print("")
        print("select step: (int)")
        step = Key_c.numpad()
        
        print(f"step: {step}")
        print("move with keys...")

        key =""
        while key != Key_c.AllKeys.KEY_QUIT:
            key = Key_c.scanKeys()
            if key in Key_c.MANUAL_MOVMENT:
                
                self.MaualMovement(key, amt=step)
        print("exiting manual...")
        
    
    
        
        
        

    

    
