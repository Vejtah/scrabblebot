import itertools
from tqdm import tqdm
import time

# Set up the dictionary for word validation.

from dictonray import Us_en

d = Us_en()

def check_word(word: str) -> bool:
    """Return True if word has length>=2 and is in the dictionary."""
    return len(word) >= 2 and d.check(word)

def score_word(word: str) -> int:
    """Compute a simple Scrabble score for a word (no bonus squares)."""
    scores = {
        'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4,
        'G': 2, 'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1,
        'M': 3, 'N': 1, 'O': 1, 'P': 3, 'Q': 10, 'R': 1,
        'S': 1, 'T': 1, 'U': 1, 'V': 4, 'W': 4, 'X': 8,
        'Y': 4, 'Z': 10
    }
    actual_score = sum(scores[letter.upper()] for letter in word)
    lenth_score = len(word) + 2 # make lengh a facor as well 
    return actual_score * lenth_score

def remove_impossible(board: dict) -> dict:
    """
    Filter board positions to only those adjacent to an existing letter.
    This reduces the search space by focusing on "active" areas.
    """
    rows, cols = 10, 15
    filtered = {}
    for y in range(rows):
        for x in range(cols):
            # Check the 3x3 neighborhood.
            adjacent = False
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < cols and 0 <= ny < rows:
                        if board.get((nx, ny)) is not None:
                            adjacent = True
            if adjacent:
                filtered[(x, y)] = board.get((x, y))
    return filtered

def generate_words_from_sequence(board: dict, start: tuple, direction: tuple, length: int, hand: list[str]) -> list:
    """
    For a given starting coordinate and direction, generate all valid words of
    given length by filling empty board slots with letters from hand.
    
    Parameters:
      board: dict mapping (x,y) to a letter (or None if empty)
      start: starting (x, y) coordinate
      direction: tuple (dx, dy) indicating the direction (e.g. (1,0) for horizontal)
      length: how many slots to include in this sequence
      hand: list of letters available
      
    Returns:
      A list of moves. Each move is a tuple:
        (word, direction, start, placed_positions)
      where placed_positions is a dict mapping board coordinates to the letter played.
    """
    seq = []         # will store letters or None
    empty_indices = []  # indices in the sequence that are empty (to fill from hand)
    fixed_indices = {}  # indices where board already has a letter
    # Build the sequence along the direction.
    for i in range(length):
        pos = (start[0] + i * direction[0], start[1] + i * direction[1])
        # Check board boundaries (cols: 0-14, rows: 0-9)
        if not (0 <= pos[0] < 15 and 0 <= pos[1] < 10):
            break
        letter = board.get(pos, None)
        if letter is not None:
            seq.append(letter.lower())
            fixed_indices[i] = letter.lower()
        else:
            seq.append(None)
            empty_indices.append(i)
    # Only consider sequences that include at least one board letter (an anchor)
    if not fixed_indices:
        return []
    # If no empty slots, the word is fixed. Validate it.
    if not empty_indices:
        word = "".join(seq)
        if check_word(word):
            return [(word, direction, start, {})]
        return []
    
    valid_moves = []
    # For each permutation of hand letters to fill the empty slots:
    for perm in itertools.permutations(hand, len(empty_indices)):
        candidate = list(seq)
        placed = {}  # record which positions get a letter from hand
        for idx, letter in zip(empty_indices, perm):
            candidate[idx] = letter.lower()
            placed[idx] = letter.lower()
        word = "".join(candidate)
        if check_word(word):
            # Map indices to board coordinates.
            placed_positions = {}
            for idx, letter in placed.items():
                pos = (start[0] + idx * direction[0], start[1] + idx * direction[1])
                placed_positions[pos] = letter
            valid_moves.append((word, direction, start, placed_positions))
    return valid_moves

class Scrabble:
    def __init__(self, rows: int = 10, cols: int = 15, amt_letters: int = 7):
        self.rows = rows
        self.cols = cols
        self.amt_letters = amt_letters

    def all_possible_moves(self, board: dict, hand: list[str], moves_played: list[str]) -> list:
        """
        Generate all legal moves based on the current board and the player's hand.
        This function scans over positions near existing tiles (using remove_impossible)
        and tries to form words horizontally and vertically.
        """
        moves = []
        start_time = time.perf_counter()
        # Only consider positions near an anchor.
        filtered_board = remove_impossible(board)
        # For each candidate starting position, try horizontal and vertical moves.
        for (x, y) in tqdm(filtered_board.keys(), total=len(filtered_board), desc="Generating moves"):
            for length in range(1, self.amt_letters + 1):
                # Horizontal move (left-to-right)
                moves.extend(generate_words_from_sequence(board, (x, y), (1, 0), length, hand))
                # Vertical move (top-to-bottom)
                moves.extend(generate_words_from_sequence(board, (x, y), (0, 1), length, hand))
        elapsed_time = time.perf_counter() - start_time
        print(f"Elapsed needed: {elapsed_time:.6f} seconds")

        moves_clean = []

        print(f"movves_played_func: {moves_played}")
        for move in moves:
            if move[0] not in moves_played and len(move[3]) >= 1: # check if the word was played and adds new lettrs to the board
                moves_clean.append(move)
        
        return moves_clean

        
    def eval_moves(self, moves: list) -> tuple:
        """
        Evaluate moves by their Scrabble score and print a summary.
        
        Returns a tuple of:
          (best_move, move_scores)
        where best_move is the move tuple with the highest score and move_scores is a dict mapping word to score.
        """
        best_move = None
        best_score = 0
        move_scores = {}
        for move in moves:
            word = move[0]
            score = score_word(word)
            move_scores[word] = score
            if score > best_score:
                best_score = score
                best_move = move

        # Display a simple score chart.
        print("Move Scores:")
        for word, score in sorted(move_scores.items(), key=lambda x: x[1], reverse=True):
            bar = "=" * (score // 2)  # simple bar proportional to score
            print(f"{word:<10} | {score:<3} | {bar}")
        print(best_move)
        print(move_scores)
        return best_move, move_scores
