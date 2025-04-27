import time
from tqdm import tqdm


try:
    from config import Constants
except ModuleNotFoundError:
    from functions.config import Constants

from functions.keys import Keys

if Constants.System.running_on_raspberry:
    import board # type: ignore
    from adafruit_motor import stepper # type: ignore
    from adafruit_motorkit import MotorKit # type: ignore
    import busio # type: ignore
    from adafruit_pca9685 import PCA9685 # type: ignore
    from adafruit_motor import servo # type: ignore



Key_c = Keys()


class Movement:
    def __init__(self):
        """
        crate an object self.Constants to save stepper positions
        """

        self.Cons = Constants()
        if Constants.System.running_on_raspberry:
            self.kit = MotorKit(i2c=board.I2C())

            self.s_x = self.kit.stepper1
            self.s_y = self.kit.stepper2
            self.sleep = .04

            self.i2c = busio.I2C(board.SCL, board.SDA)
            self.pca = PCA9685(self.i2c)
            self.pca.frequency = 40

            self.hand = servo.Servo(self.pca.channels[0])

    def open(self):
        self.hand.angle = 30
    def close(self):
        self.hand.angle = 0

    def release(self) -> None:
        self.s_x.release() # release to prevent overheat
        self.s_y.release()

    def move(self, x_move_by: int, y_move_by: int, poss_check=True):

        if poss_check:
            if 0 <= (self.Cons.Pos.s_x + x_move_by) <= self.Cons.Pos.s_x_max:
                print("move X pos: OK")
            else:
                print("move X unable: ERROR")
                return


            if 0 <= (self.Cons.Pos.s_y + y_move_by) <= self.Cons.Pos.s_y_max:
                print("move Y pos: OK")
            else:
                print("move Y unable: ERROR")
                return


        # have to move right (x>0) , move x stepper BACKWARD

        if x_move_by >= 0:
            x_dir = stepper.BACKWARD
            x_dir_i = 1

        else:
            x_dir = stepper.FORWARD
            x_move_by *= -1
            x_dir_i = -1


        if y_move_by >= 0:
            y_dir = stepper.BACKWARD
            y_dir_i = 1

        else:
            y_dir = stepper.FORWARD
            y_move_by *= -1
            y_dir_i = -1

        x_progress = tqdm(total=x_move_by, desc="X move Progress")
        y_progress = tqdm(total=y_move_by, desc="Y move Progress")

        # combine x and y movement:
        while x_move_by >= 1 and y_move_by >= 1:

            self.s_x.onestep(direction=x_dir)
            time.sleep(self.sleep / 2) # wait 1/2 of waiting cycle

            self.s_y.onestep(direction=y_dir)

            x_progress.update(1)
            y_progress.update(1)

            x_move_by -= 1
            y_move_by -= 1

            self.Cons.Pos.s_x += x_dir_i # update location +1 if pos else -1
            self.Cons.Pos.s_y += y_dir_i

            time.sleep(self.sleep / 2)  # finsh the waiting cycle

        #  move the rest
        if x_move_by >= y_move_by:
            x_left = x_move_by - y_move_by

            for _ in range(x_left):
                self.s_x.onestep(direction=x_dir)

                x_progress.update(1)

                self.Cons.Pos.s_x += x_dir_i

                time.sleep(self.sleep)

        else:
            y_left = y_move_by - x_move_by

            for _ in range(y_left):
                self.s_y.onestep(direction=y_dir)

                y_progress.update(1)

                self.Cons.Pos.s_y += y_dir_i

                time.sleep(self.sleep)




    def move_to(self, target_x: int, target_y: int) -> {int | float, int | float}:
        x_move_by = target_x - self.Cons.Pos.s_x
        y_move_by = target_y - self.Cons.Pos.s_y

        # check if move possible

        x_next = self.Cons.Pos.s_x + x_move_by  # maybe -?? but i dont think so
        y_next = self.Cons.Pos.s_y + y_move_by

        if 0 <= x_next <= self.Cons.Pos.s_x_max and 0 <= y_next <= self.Cons.Pos.s_y_max:
            print("move possible, proceeding...")
        else:
            print("next move called in minus: ERROR")
            print("aborting...")
            return  # exit move function

        self.move(x_move_by, y_move_by)


    def move_to_piece(self, x: float, y: float):
        #x
        move_range_x = self.Cons.Pos.s_x_max - self.Cons.Pos.x_start_offset - self.Cons.Pos.x_end_offset
        piece_x = move_range_x / self.Cons.cols #cols = 15  - calculate the steps rq for one tile

        move_range_y = self.Cons.Pos.s_y_max - self.Cons.Pos.y_start_offset - self.Cons.Pos.y_end_offset
        piece_y = move_range_y / self.Cons.rows #rows = 12 ( 10 + 2)

        # add starting offset


        piece_x_pos = (piece_x * x) + self.Cons.Pos.x_start_offset

        piece_x_pos += piece_x / 2  # add 1/2 of the tile to be in the middle

        piece_y_pos = (piece_y * y) + self.Cons.Pos.y_start_offset

        piece_y_pos += piece_y / 2 # add 1/2 of the tile to be in the middle

        self.move_to(round(piece_x_pos), round(piece_y_pos))

    def ret(self) -> None:

        # check if the hand is already in the top right corner
        if (self.Cons.Pos.s_x > Constants.Pos.s_x_max - Constants.Pos.x_start_offset and
            self.Cons.Pos.s_y > Constants.Pos.s_y_max - Constants.Pos.y_start_offset):
            pass

        else:
            self.move_to_piece(14, 10)
            time.sleep(self.sleep)

        self.move_to(Constants.Pos.s_x_max, Constants.Pos.s_y_max) #  move to right top corner
        self.move(10, 10, poss_check=False)  # disable check if possible move
        self.Cons.s_x, self.Cons.s_y = Constants.Pos.s_x_max, Constants.Pos.s_y_max  # reset the x and y var
        self.open() # open the hand

    def manual_movement(self, key: int, amt=5):

        action = Key_c.MANUAL_MOVEMENT.index(key)
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
        print(f"{self.Cons.Pos.s_x} | {self.Cons.Pos.s_y}")


    def manual(self):
        print("entering manual movement...")
        print("")
        print("select step: (int)")
        step = Key_c.numpad()

        print(f"step: {step}")
        print("move with keys...")

        key =""
        while key != Key_c.AllKeys.KEY_QUIT:
            key = Key_c.scan_keys()
            if key in Key_c.MANUAL_MOVEMENT:

                self.manual_movement(key, amt=step)
        print("exiting manual...")
