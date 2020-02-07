import numpy as np
from init import WIDTH, HEIGHT, font, window_height, window_width, pygame, SQUARE_SIZE

SHAPES = [
    np.array([
        [1, 1, 0],
        [0, 1, 1]
    ]),
    np.array([
        [0, 2, 2],
        [2, 2, 0]
    ]),
    np.array([
        [3, 3],
        [3, 3]
    ]),
    np.array([
        [0, 0, 0],
        [4, 4, 4],
        [0, 4, 0]
    ]),
    np.array([
        [0, 0, 0],
        [5, 5, 5],
        [0, 0, 5]
    ]),
    np.array([
        [0, 0, 0],
        [6, 6, 6],
        [6, 0, 0]
    ]),
    np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [7, 7, 7, 7],
        [0, 0, 0, 0]
    ])
]

COLORS = [
    (0, 0, 0),
    (255, 13, 114),
    (13, 194, 255),
    (13, 255, 114),
    (245, 56, 255),
    (255, 142, 13),
    (255, 225, 56),
    (56, 119, 255),
    (0, 0, 139),
]

def createBlockdropAnimation(player):
    counter = 0
    white = False
    def inner(s):
        nonlocal counter, white
        if counter % 4 == 0:
            white = not white

        for y, l in enumerate(player["shape"]):
        
            for x, e in enumerate(l):
                if e > 0:
                    pygame.draw.rect(s, COLORS[e] if not white else (255,255,255), ((player["x"] + x + 1) * SQUARE_SIZE, (player["y"] + y) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        pygame.display.update()
        counter += 1

    return inner
        

def das(delay, speed):
    counter = delay
    charged = False
    def inner(charge=False):
        nonlocal counter, charged
        if charge:
            counter = delay
            charged = True
            return

        if counter == 16:
            counter = [0, delay-speed][charged]
            charged = True
            return True
        
        counter += 1
        return False

    return inner

def drop(delay, first=False):
    counter = 0
    if first:
        counter = -100
    def inner(increment=1):
        nonlocal counter
        if counter >= delay:
            counter = 0
            return True
        counter += increment
        return False

    return inner

def pause(delay):
    counter = 0
    def inner():
        nonlocal counter
        if counter >= delay:
            return True

        counter += 1
        return False

    return inner
        
def clearLines(b):
    lineCount = 0
    for y, l in enumerate(b):
        if l.min() != 0:
            lineCount += 1
            y_up = y
            while y_up > 0:
                b[y_up, :] = b[y_up - 1].copy()
                y_up -= 1
            b[0, :] = [0] * WIDTH

    return lineCount

def displayText(s, string_text, pos, color=(255,255,255), center=False):
    lines = string_text.split("\n")
    x_center, y_center = pos
    lineHeight = font.size(string_text)[1]
    y_current = y_center - len(lines) * lineHeight / 2
    for line in string_text.split("\n"):
        text = font.render(line, True, color)
        
        s.blit(text, (x_center - center * text.get_width() / 2, y_current))
        y_current += lineHeight

def drawBoard(s, b, player=None):
    # draw the current playing-field
    print_b = b.copy() # b is het bord zonder de huidige blok
    if player:
        player.burn(print_b) # we zetten de huidige blok in print_b, zonder het huidige veld aan te passen

    pygame.draw.rect(s, COLORS[0], (0, 0, window_width, window_height))
    for y, l in enumerate(print_b):
        pygame.draw.rect(s, COLORS[8], (0, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for x, e in enumerate(l):
            if e > 0:
                pygame.draw.rect(s, COLORS[e], ((x + 1) * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        pygame.draw.rect(s, COLORS[8], ((WIDTH + 1) * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    pygame.draw.rect(s, COLORS[8], (0, window_height - SQUARE_SIZE, (WIDTH + 2) * SQUARE_SIZE, SQUARE_SIZE))


    # draw the next piece
    if not player:
        return

    
    displayText(s, f"Score:\n{player.score:09}\nLines:\n{player.lines:03}\nLevel:\n{player.level:02}", (WIDTH * SQUARE_SIZE +  3.5 * SQUARE_SIZE, 3 * window_height / 4))

    min_y, min_x = 2 * SQUARE_SIZE, (WIDTH + 3) * SQUARE_SIZE
    pygame.draw.rect(s, COLORS[8], (min_x, min_y, 7 * SQUARE_SIZE, SQUARE_SIZE))
    pygame.draw.rect(s, COLORS[8], (min_x, min_y, SQUARE_SIZE, 7 * SQUARE_SIZE))
    pygame.draw.rect(s, COLORS[8], (min_x + 6 * SQUARE_SIZE, min_y, SQUARE_SIZE, 7 * SQUARE_SIZE))
    pygame.draw.rect(s, COLORS[8], (min_x, min_y + 6 * SQUARE_SIZE, 7 * SQUARE_SIZE, SQUARE_SIZE))
    for y, l in enumerate(player.nextShape):
        for x, e in enumerate(l):
            if e > 0:
                pygame.draw.rect(s, COLORS[e], (min_x + (x + 2) * SQUARE_SIZE, min_y + (y + 2) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
    pygame.display.update()


def displayButton(s, text, rect, bc, fc, action=None):
    center_x, center_y, width, height = rect
    pygame.draw.rect(s, bc, (center_x - width / 2, center_y - height / 2, width, height))
    displayText(s, text, (center_x, center_y), color=fc, center=True)

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if center_x + width / 2 > mouse[0] > center_x - width / 2 and center_y + height / 2 > mouse[1] > center_y - height / 2:
        if click[0] == 1 and action != None:
            action()
         

def drawMenu(s, prev_score, play_button_action=None):
    """ Fuck off """
    pygame.draw.rect(s, COLORS[0], (0, 0, window_width, window_height))
    displayText(s, "Tetris", (window_width / 2, window_height / 10), center=True)

    if prev_score:
        displayText(s, prev_score, (window_width / 2, window_height / 2), center=True)

    displayButton(s, "PLAY!", (window_width / 2, window_height * 0.80, 120, 50), (255,255,255), (0, 0, 0), play_button_action)

    pygame.display.update()