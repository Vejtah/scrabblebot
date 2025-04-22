import json

from constans import Constants

Cons = Constants()
json_path = Cons.System.json_path

class Data:
    def __init__(self):
        pass

    def write(self, data):
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self):
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data

    def clac_midpoint(self, data):
        """
        find the highest black val for the frames with letters and the lowest for the frames without tiles
        than find a midpoint which will be used to determine if there is a letters or not later on (using the network)

        """
        letters = sorted(data["letters"], reverse=True) # need the highest val
        nones = sorted(data["None"])
        letters_highest_val = letters[0]
        nones_smallest_val = nones[0]

        midpoint = (letters_highest_val + nones_smallest_val) / 2
        midpoint += Cons.Image.add_black_prc  # add some extra % to shift the midpoint up

        return midpoint
