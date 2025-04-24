import json
from datetime import datetime
from constants import Constants

def write(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data
def reset_grids():
    write(  # reset
        {
        "grid": [],
        "choose": []
        },
        Constants.Image.compare_grids_json
    )

def add_grid(grid, choose):
    data = load(Constants.Image.compare_grids_json)
    grid_copy = {}
    for key, item in grid.items():  # json doesn't accept tuples as keys in dict
        grid_copy[str(key)] = item
    
    data["grid"].append(grid_copy)
    data["choose"].append(choose)
    write(data, Constants.Image.compare_grids_json)

def add_black_letter_val(val:float)->None:
    data = load(Constants.System.json_path_black_vals)
    data["letters"].append(val)
    
    write(data, Constants.System.json_path_black_vals)

def log(*msg, t=0)->None:

    if msg is None:
        return

    types = {
        0: "INFO",
        1: "WARNING",
        2: "ERROR"
    }

    now = datetime.now()
    time = now.strftime(Constants.System.log_time_format)
    time_skip = " " * len(time)
    log_msg = f"{time}|{types[t]}: {str(msg[0])}\n"

    for i, m in enumerate(msg):
        if i == 0:
            continue  # skip the first message
        else:
            log_msg += f"{time_skip}|{types[t]}: {str(m)}\n"


    with open(Constants.System.log_path, "a") as l:
        l.write(
            log_msg
        )
    l.close()

def clac_midpoint(data):
    """
    find the highest black val for the frames with letters and the lowest for the frames without tiles
    than find a midpoint which will be used to determine if there is a letters or not later on (using the network)

    """
    letters = sorted(data["letters"], reverse=True) # need the highest val
    nones = sorted(data["None"])
    letters_highest_val = letters[0]
    nones_smallest_val = nones[0]

    midpoint = (letters_highest_val + nones_smallest_val) / 2
    midpoint += Constants.Image.add_black_prc  # add some extra % to shift the midpoint up
    
    return midpoint

def compare_grids() -> {int, int}:
    data = load(Constants.Image.compare_grids_json)
    grids = data["grid"]
    chooses = data["choose"]

    len_dicts = len(grids)
    error_d = 0

    for i in range(len_dicts):
        for key, item in grids[i].items():
            for n in range(len_dicts):
                if grids[i][key] == grids[n][key]:
                    pass
                else:
                    log(f"k: {key}, grids {i}, {n}: {grids[i][key]}, {grids[n][key]}", t=1)
                    error_d += 1

    error_ch = 0

    for i, choose in enumerate(chooses):
        for x in chooses:
            for n, letter in enumerate(choose):
                if letter == x[n]:
                    pass
                else:
                    error_ch += 1
                    log(f"letter: {letter}, {x[n]}", t=1)


    return error_d, error_ch

if __name__ == "__main__":

    log("test", "test", t=0)
