from evdev import InputDevice, categorize, ecodes

from configs.config import Constants


class Keys: # class for all controls
    def __init__(self):
        for n in range(Constants.System.rasp_pi_ports):
            try:
                device = InputDevice(f'/dev/input/event{n}')
                print(f"Listening on event {n} - {device.path} - {device.name}")
                if device.name == Constants.System.keyboardName:

                    print(f"Listening on {device.path} - {device.name} : OK")
                    break

            except FileNotFoundError as _:
                #print(e)
                pass

        self.device = device

    class AllKeys:    
        KEY_PLAY = "KEY_SPACE"
        KEY_QUIT = "KEY_Q"
        KEY_CONFIRM = "KEY_ENTER"
        KEY_MOVE_Xp = "KEY_RIGHT" # x to right 
        KEY_MOVE_Xn = "KEY_LEFT" # x to left
        KEY_MOVE_Yp = "KEY_UP" # y up
        KEY_MOVE_Yn = "KEY_DOWN" # y down
        KEY_HELP = "KEY_H"
        KEY_NUMPAD = "KEY_N"
        KEY_MANUAL = "KEY_M"

    MANUAL_MOVEMENT = [AllKeys.KEY_MOVE_Xp, AllKeys.KEY_MOVE_Xn, AllKeys.KEY_MOVE_Yp, AllKeys.KEY_MOVE_Yn]


    numPad = {
        "KEY_KP0": 0,
        "KEY_KP1": 1,
        "KEY_KP2": 2,
        "KEY_KP3": 3,
        "KEY_KP4": 4,
        "KEY_KP5": 5,
        "KEY_KP6": 6,
        "KEY_KP7": 7,
        "KEY_KP8": 8,
        "KEY_KP9": 9
    }

    def scan_keys(self):
        for event in self.device.read_loop():
            if event.type == ecodes.EV_KEY:
                key_event = categorize(event)
                if key_event.keystate == key_event.key_down:
                    # Sometimes key_event.keycode might be a list; handle both cases.

                    key = key_event.keycode

                    return key
    
    def numpad(self):
        print("entering numpad...")
        num = ""
        key = ""
        while key != self.AllKeys.KEY_CONFIRM:
            key = self.scan_keys()
            if key in self.numPad:
                num += str(self.numPad[key])
                print(num)
            
        return int(num)

    
    def help(self):


        print("help:")
        for attr, value in self.AllKeys.__dict__.items():  # cycle though all items in AllKeys
            if not attr.startswith('__'):
                print(f"{attr} = {value}")
        print("")




    
