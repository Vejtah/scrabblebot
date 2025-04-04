
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
YELLOW = (255, 255, 0)

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

played_moves = []

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

    if False:  # def remove impossible
        possiles = {(8, 9): None, (9, 9): None, (10, 9): None, (11, 9): None, (12, 9): None, (13, 9): None, (14, 9): 'E', (14, 3): None, (14, 4): None, (14, 5): None, (14, 6): None, (14, 7): None, (14, 8): None}
        for (x, y), item in possiles.items():

            c_x = x * t_with
            c_y = y * t_height
            pygame.draw.rect(
                screen, YELLOW, (c_x, c_y, t_with - 1, t_height - 1)
            )
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
        direction = (0, 1)
    elif action == 1:
        selected = (selected[0], selected[1] + 1)
        direction = (0, 1)
    elif action == 2:
        selected = (selected[0] + 1, selected[1])
        direction = (1, 0)
    else:
        selected = (selected[0] - 1, selected[1])
        direction = (1, 0)

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



def find_click(float: x, float: y) -> int | int:
    current_x = 0
    current_y = 0

    while True:
        if (current_x * t_with) <= x <= ((current_x + 1) * t_with):
            break
        else:current_x+=1

    while True:
        if (current_y * t_height) <= y <= ((current_y + 1) * t_height):
            break
        else:current_y+=1

    return current_x, current_y


def plot_word(move_tupple: tuple) -> None:
    
    letters_dict = move_tupple[3]
    
    for (x, y), letter in letters_dict.items():
        letters[(x, y)] = letter.upper() # add the letter to the main dict 

def choose_rand_letters(l=7):
    
    # Scrabble letter frequencies for English (without blanks)
    weights = [9, 2, 2, 4, 12, 2, 3, 2, 9, 1, 1, 4, 2, 6, 8, 2, 1, 6, 4, 6, 4, 2, 2, 1, 2, 1]
    return random.choices(possible, weights=weights, k=l)


def find_move():
    global letters, played_moves
    print("best word...")
    choose = choose_rand_letters()
    print(choose)
    best_move, _ = s.eval_moves(s.all_possible_moves(letters, choose, played_moves))

    print(f"best word: {best_move[0]}")

    plot_word(best_move)
    

    played_moves.append(best_move[0])  # save word so wont get played again
    print(f"played moves: {played_moves}")



clock = pygame.time.Clock()
running = True
selected = (cols // 2, rows // 2)
direction = (1, 0)  # auto move selected on letter press
while running:
    x, y  = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            key = pygame.key.name(event.key)
            if key in MOVE:  # move selected tile
                move(key)
            elif key.upper() in possible:
                add(key)
            elif key == "backspace":
                remove(selected)
            elif key == "return":
                find_move()
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = find_click(x, y)
            selected = (click_x, click_y)
                
    # Update the displaybr
    screen.fill(BLACK)
    draw_back()
    selected_tile(selected)
    back_num()
    write_existing()

    pygame.display.flip()

    # Cap the frame rate
    clock.tick(10)
exit()
