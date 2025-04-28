def compare(chooses):
    ret_choose = []

    for index, letter in enumerate(
            chooses[0]):  # cycle through the first list of choose letter and add missing from seconds
        if letter is None:
            for attempt, n_choose in enumerate(chooses):
                if n_choose[index] is not None:
                    ret_choose.append(n_choose[index])
                    continue

                elif attempt + 1 == len(chooses):  # detect if the all letters were tried
                    ret_choose.append(None)
        else:
            ret_choose.append(letter)

    return ret_choose

l1 = [None, "B", None, "D"]
l2 = ["A", None, "C", None]



l = [l1, l2]
print(l)
print(compare(l))