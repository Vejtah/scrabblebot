
import bisect


from constans import Constants
Cons = Constants()

save_dir = Cons.System.root_dir + "save.txt"


with open(save_dir, "r") as f:
    # Read lines from the file directly
    dictionary_list = [line.strip() for line in f]
    # Make sure your file is sorted. If not certain, do:
    dictionary_list.sort()

class UsEn:
    def __init__(self):
        self.dictionary = dictionary_list
    
    def check(self, word: str) -> bool:
        """
        Return True if 'word' exists in the sorted dictionary list,
        using binary search for O(log n) membership.
        """
        idx = bisect.bisect_left(self.dictionary, word)
        return idx < len(self.dictionary) and self.dictionary[idx] == word

if __name__ == "__main__":
    d = UsEn()
    print(d.check("metronome"))
