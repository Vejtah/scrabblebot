import pygame
from tqdm import tqdm as tq
from alg import Scrabble
import time
import random
pygame.init()
s = Scrabble()
# Set up display
window_size = 1200
rows, cols = 10, 15

WHITE = (255, 255, 255)
GREY = (225, 225, 225)
D1_GREY = (190, 190, 190)
DARK_GREY = (80, 80, 80)
BLACK = (0, 0, 0)

text_size = 55

MOVE = ["up", "down", "right", "left"]
possible = [
    'Q', 'W', 'E', 'R', 'T', 'Z', 'U', 'I', 'O', 'P', 'A', 'S', 'D',
    'F', 'G', 'H', 'J', 'K', 'L', 'Y', 'X', 'C', 'V', 'B', 'N', 'M']

screen = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("")
text_size_mult = window_size / 1200  # calc the text size based on the win size (for 1200 optimal = 60)


t_height = window_size / rows
t_with = window_size / cols

c_x, c_y = 0, 0
mid_pos = {}
letters = {}

# populate letters with None bacauce of the look up from find move

for y in range(rows):
    for x in range(cols):
        letters[(x, y)] = None


for y in range(rows): # create the middle pos dict x, y
    for x in range(cols):

        center_x = c_x + (t_with / 2)
        center_y = c_y + (t_height / 2)

        mid_pos[(x, y)] = (center_x, center_y)

        c_x += t_with

    c_y += t_height
    c_x = 0


def text(txt: str, pos: tuple[float, float], col: tuple[int, int, int], size=74):

    font = pygame.font.Font(None, size)

    key_text = font.render(txt, True, col)

    # Get the rect of the text
    text_rect = key_text.get_rect(center=pos)

    screen.blit(key_text, text_rect)


def draw_back() -> None:

    c_x, c_y = 0, 0

    for y in range(rows):
        for x in range(cols):

            pygame.draw.rect(
                screen, WHITE, (c_x, c_y, t_with - 1, t_height - 1)
            )


            c_x += t_with

        c_y += t_height
        c_x = 0

def back_num():

    for y in range(rows):
        for x in range(cols):

            text(f"{x}|{y}", mid_pos[(x, y)], GREY, size=round(text_size_mult * text_size))


def selected_tile(selected: tuple[int, int]):
    x, y = mid_pos[selected]
    x = x - (t_with / 2)
    y = y - (t_height / 2)

    pygame.draw.rect(
        screen, D1_GREY, (x, y, t_with - 1, t_height - 1)
    )


def move(key: str):
    global selected, direction
    old = selected

    action = MOVE.index(key)  # modfy the selected tile based on the pressed arrow
    if action == 0:
        selected = (selected[0], selected[1] - 1)
        direction = (0, -1)
    elif action == 1:
        selected = (selected[0], selected[1] + 1)
        direction = (0, 1)
    elif action == 2:
        selected = (selected[0] + 1, selected[1])
        direction = (1, 0)
    else:
        selected = (selected[0] - 1, selected[1])
        direction = (-1, 0)

    if 0 <= selected[0] <= cols - 1 and 0 <= selected[1] <= rows -1: # check if selected is on the board
        pass
    else:
        selected = old


def add(key: str) -> None:
    global selected, direction

    letters[selected] = key.upper()
    old = selected

    selected = (selected[0] + direction[0], selected[1] + direction[1])  # select next based on direction

    if 0 <= selected[0] <= cols - 1 and 0 <= selected[1] <= rows -1: # check if selected is on the board
        pass
    else:
        selected = old

def write_existing() -> None:
    for pos, letter in letters.items():

        pos = mid_pos[pos]
        text(letter, pos, DARK_GREY)


def remove(pos) -> None:
    letters[pos] = None

def plot_word(move_dict: dict[str: tuple[int, int]]) -> None:
    for letter, (x, y) in move_dict.items():
        letters[(x, y)] = letter.upper() # add the letter to the main dict 

def choose_rand_letters(l=7):
    choose = []
    for letter in range(l):
        choose.append(random.choice(possible).lower())
    return ["a", "b", "c", "d", "e", "n", "t"]


def find_move():
    global letters
    print("best word...")
    choose = choose_rand_letters()
    print(choose)
    word_tuple, move_dict = s.eval_words(s.all_pos(letters, choose), letters)

    print(f"best word: {word_tuple[0]}")

    plot_word(move_dict)


clock = pygame.time.Clock()
running = True
selected = (cols // 2, rows // 2)
direction = (1, 0)  # auto move selected on letter press
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            print(key)
            if key in MOVE:  # move selected tile
                move(key)
            elif key.upper() in possible:
                add(key)
            elif key == "backspace":
                remove(selected)
            elif key == "return":
                find_move()
                
    # Update the displaybr
    screen.fill(BLACK)
    draw_back()
    selected_tile(selected)
    back_num()
    write_existing()

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

exit()