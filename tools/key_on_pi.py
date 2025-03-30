from evdev import InputDevice, categorize, ecodes

# Replace with your keyboard's device path
device = InputDevice('/dev/input/event4')
print(f"Listening on {device.path} - {device.name}")

desired_key = 'KEY_SPACE'

def scanKeys(desired_key):
    for event in device.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            if key_event.keystate == key_event.key_down:
                # Sometimes key_event.keycode might be a list; handle both cases.

                key = key_event.keycode

                return key
                break

key = ""            
while key != "KEY_Q":
    key = scanKeys(desired_key)
    print(key)

print("quittin")
