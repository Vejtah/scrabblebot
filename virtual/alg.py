import enchant
import itertools
from tqdm import tqdm
import time
d = enchant.Dict("en_US")  # select language


def all_pos_local(letters: list[str], num_slots: int) -> list:
    # itertools.product returns an iterator over tuples
    return ["".join(combo) for combo in itertools.permutations(letters, num_slots)]


def check_word(word: str) -> list:
    if len(word) >= 2 and d.check(word):
        return True
    else: 
        return False

def score_word(word: str) -> int:
    
    score = {
        'A': 1,
        'B': 3,
        'C': 3,
        'D': 2,
        'E': 1,
        'F': 4,
        'G': 2,
        'H': 4,
        'I': 1,
        'J': 8,
        'K': 5,
        'L': 1,
        'M': 3,
        'N': 1,
        'O': 1,
        'P': 3,
        'Q': 10,
        'R': 1,
        'S': 1,
        'T': 1,
        'U': 1,
        'V': 4,
        'W': 4,
        'X': 8,
        'Y': 4,
        'Z': 10
    }
    total_s = 0
    for letter in list(word):
        total_s += score[letter.upper()]

    return total_s 


def insert_substring(original: str, index: int, substring: str) -> str:
    return original[:index] + substring + original[index:]


class Scrabble:
    def __init__(self):
        self.rows, self.cols = 10, 15
        self.tiles = self.rows * self.cols

    # brute all words :D
    def all_pos(self, board: dict[(int, int): str], letters: list[str]) -> list[tuple[str, bool, tuple[int, int]]]:
        #  -> list[tuple(word, x_true, tuple(x, y))
        all_possibles = []
        total_words = 0
        find_words_graph = tqdm(total=self.tiles, desc="finding all possible moves")  # plot the porgress
        start_time = time.perf_counter()
        for y in range(self.rows):
            for x in range(self.cols):  # go through all tiles

                add_existing_letters = {}
                
                for letter_position in range(1, len(letters) + 1):  # go through words in the next 7 slots
                    x_current = x + letter_position - 1
                    # check if still playing on the board (-1 because of interation)
                    if x_current <= self.cols - 1:
                        if board[(x_current, y)] is not None:  # there is already a letter at current spot

                            add_existing_letters[letter_position] = board[(x_current, y)]  # save to add it latter
                        else:
                            # get all the possibilities of the space between current and the starting point,
                            # excluding existing

                            # check if the possible word is touching something on either start or end    
                            if len(add_existing_letters) >= 1:
                                for possibility in all_pos_local(letters, letter_position): # add all possibles to list:

                                    # if the word has n existing letter from the board than include it for the word eval
                                    
                                    for letter_index, letter_insert in add_existing_letters.items():
                                        #print(f"{possibility}:{letter_index}:{letter_insert}")
                                        possibility = insert_substring(possibility.lower(), letter_index , letter_insert.lower())
#                                        print(possibility)
#                                        total_words += 1
                                        if check_word(possibility): # confirmed word time to save it 

                                            word = (possibility, True, (x, y)) # tupple for save

                                            all_possibles.append(word)  # add local valid to all valid
            
                """ check vertical"""
                add_existing_letters = {}
                
                for letter_position in range(1, len(letters) + 1):  # go through words in the next 7 slots
                    y_current = y + letter_position - 1
                    # check if still playing on the board (-1 because of interation)
                    if y_current <= self.rows - 1:
                        if board[(x, y_current)] is not None:  # there is already a letter at current spot

                            add_existing_letters[letter_position] = board[(x, y_current)]  # save to add it latter
                        else:
                            # get all the possibilities of the space between current and the starting point,
                            # excluding existing

                            # check if the possible word is touching something on either start or end
                            if len(add_existing_letters) >= 1: # the word has to include some letters from the board
                                for possibility in all_pos_local(letters, letter_position): # add all possibles to list:

                                    # if the word has n existing letter from the board than include it for the word eval
                                    for letter_index, letter_insert in add_existing_letters.items():
                                        #print(f"{possibility}:{letter_index}:{letter_insert}")
                                        possibility = insert_substring(possibility.lower(), letter_index, letter_insert.lower())
#                                        total_words += 1
#                                        print(possibility)
                                        if check_word(possibility): # confirmed word time to save it 

                                            word = (possibility, False, (x, y)) # tupple for save false because y direction 

                                            all_possibles.append(word)  # add local valid to all valid
                
                
#                find_words_graph.update(1) # plot
        print(f"total legal letter combinations: {total_words}")
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Elapsed time: {elapsed_time:.6f} seconds")

        return all_possibles
    def eval_words(self, words: list[type], board: dict[(int, int): str]) -> tuple[str, dict[str: tuple[int, int]]] | dict[str: tuple[int, int]]:
        # -> (word, {letter:(x, y)})  letter: lay_x, lay_y  # exclude letters alreday on the board
          # specified [0]
        word_eval = {}

        for word in words: # score words

            lit_word = word[0] # get string word             
            word_eval[score_word(lit_word)] = lit_word

        scores = {}
        higthst_score = 0
        for score, word in word_eval.items(): # find the higest score
            print(score,word)
            scores[word] = score

            if score >= higthst_score:
                higthst_score = score

        # plot
 

        
        word = ("", True, (0, 0))
        i = 0
        while word_eval[higthst_score] != word[0]:  # iterate back to best word
            word = words[i]
            i += 1
        
        print(word)
        
        lit_word = word[0]

        sorted_scores = dict(sorted(scores.items(), reverse=True))
        lengh = 10
        item = "="
        print(sorted_scores)
        proc = lengh / sorted_scores[lit_word]

        for word_l, score in sorted_scores.items():
            line_l = ""

            for _ in range(round(proc * score)):
                line_l += item

            line = f"{word_l:<10} | {score:<3} | {line_l}"
            print(line)
       

        letter_pos = {}
        move_dict = {}

        start_x, start_y = word[2]
        for i, letter in enumerate(list(lit_word)):
            
            if word[1]:  # direction x
                x, y = start_x + i - 1, start_y
            
            else: # direction y
                x, y = start_x, start_y + i - 1 
            
            letter_pos[letter] = (x, y)
            
            if board[(x, y)] is None:
                move_dict[letter] = (x, y)                

        word_tuple = (lit_word, letter_pos)

        return word_tuple, move_dict