from evdev import InputDevice, categorize, ecodes

for n in range(10):
    try:
        device = InputDevice(f'/dev/input/event{n}')
        print(f"Listening on event {n} - {device.path} - {device.name} : OK")
    except FileNotFoundError as e:
        print(e)
