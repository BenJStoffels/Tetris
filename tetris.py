import pygame
import numpy as np # for 2D fields
import random

# Al de vormen
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

# Grootte van het bord
field = HEIGHT, WIDTH = (20, 10)
# Maakt een 2d lijst gevuld met 0
board = np.zeros(field, dtype=int)

SQUARE_SIZE = 30
window_shape = window_height, window_width = ((HEIGHT + 1) * SQUARE_SIZE, (WIDTH + 2 + 9) * SQUARE_SIZE)

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()
font = pygame.font.Font("Redkost Comic.otf", 32)

# Alles wat met de bewegende blok heeft te maken
class Player:
    def __init__(self, b, level):
        self.level = level
        self.lines = 0
        self.score = 0
        self.linesUntilNextLevel = min((level + 1) * 10, max(100, level * 10 - 50))
        self.counter = -100
        self.pause_counter = 0
        self.das_counter = -1
        self.previous_direction = 0
        self.nextShape = random.choice(SHAPES).copy()
        self.reset(b)

    # Zet de huidige blok in het veld
    def burn(self, b):
        min_y, min_x, off_y, off_x = self.rect
        for y in range(min_y, min_y + off_y):
            for x in range(min_x, min_x + off_x):
                if self.shape[y - min_y, x - min_x] != 0:
                    b[y, x] = self.shape[y - min_y, x - min_x]

    def calcScore(self, lines):
        return [0, 40, 100, 300, 1200][lines] * (self.level + 1)

    # Kijkt of de huidige blok iets aanraakt
    def collides(self, b):
        min_y, min_x, off_y, off_x = self.rect

        for y in range(min_y, min_y+off_y):
            if y >= HEIGHT:
                if self.shape[y-min_y, :].max() > 0:
                    return True
                continue
            if y < 0:
                if self.shape[y-min_y, :].max() > 0:
                    return True
                continue
            
            for x in range(min_x, min_x+off_x):
                if x >= WIDTH:
                    if self.shape[:, x-min_x].max() > 0:
                        return True
                    continue
                if x < 0:
                    if self.shape[:, x-min_x].max() > 0:
                        return True
                    continue
                if b[y, x] != 0 and self.shape[y-min_y, x-min_x] != 0:
                    return True
        return False

    # Beweegt de blok omlaag en kijkt of de blok helemaal beneden is
    def drop(self, b):
        self.y += 1
        self.counter = 0
        if self.collides(b):
            self.y -= 1
            self.burn(b)
            self.pause_counter = 1
            huidige_lines = clearLines(b)
            self.lines += huidige_lines
            self.linesUntilNextLevel -= huidige_lines
            self.score += self.calcScore(huidige_lines)

            if self.linesUntilNextLevel <= 0:
                self.level += 1
                self.linesUntilNextLevel = 10
            self.reset(b)

    # voor naar links en rechts te bewegen
    def move(self, d, b):
        if self.das_counter != -1 and self.das_counter != 16:
            self.das_counter += 1
            return
        if self.das_counter == -1:
            self.das_counter = 0
            
        if self.das_counter == 16:
            self.das_counter = 10

        self.x += d
        if self.collides(b):
            self.das_counter = 16
            self.x -= d

    def next(self, b):
        self.counter += 1
        
        if self.counter == self.dropRate:
            self.drop(b)


    # Nieuwe blok en terug naar boven
    def reset(self, b):
        self.x = 4
        self.y = 0
        self.shape = self.nextShape.copy()
        self.nextShape = random.choice(SHAPES).copy()
        if self.collides(b):
            # Wanneer de nieuwe blok meteen iets raakt, is het spel gedaan,
            # raise zorgt ervoor dat er een Error komt (zie later)
            raise StopIteration

    def rotate(self, d, b):
        self.shape = np.rot90(self.shape, d % 4)
        if self.collides(b):
            self.shape = np.rot90(self.shape, (d + 2) % 4)


    # Om te zien waar de blok is een hoe breed/hoog
    @property
    def rect(self):
        y_min, x_min = self.y, self.x
        y_off, x_off = self.shape.shape
        return y_min, x_min, y_off, x_off

    # Niet belangrijk
    @rect.setter
    def set_rect(self, val):
        raise PermissionError(
            "You can't set the rect attr, you should instead change the shape or position attributes!")

    @property
    def dropRate(self):
        return [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2,2,2,2,2,2,2,1][self.level % 30]

    # Niet belangrijk
    @dropRate.setter
    def set_dropRate(self, val):
        raise PermissionError(
            "You can't set the dropRate attr, you should change the level instead!")

    @property
    def pause(self):
        if not self.pause_counter == 0:
            self.pause_counter += 1
            if self.pause_counter >= 10:
                self.pause_counter = 0
            return True

        return False

    @pause.setter
    def set_pause(self, val):
        raise PermissionError(
            "You can't set the pause attr, you should change the pause_counter instead!")
        


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

def displayText(s, string_text, pos, lineHeight):
    lines = string_text.split("\n")
    x_pos, y_center = pos
    y_current = y_center - len(lines) * lineHeight / 2
    for line in string_text.split("\n"):
        text = font.render(line, True, (255,255,255))
        
        s.blit(text, (x_pos, y_current))
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

    
    displayText(s, f"Score:\n{player.score:09}\nLines:\n{player.lines:03}\nLevel:\n{player.level:02}", (WIDTH * SQUARE_SIZE +  3.5 * SQUARE_SIZE, 3 * window_height / 4), 34)

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
            


def mainGame():
    player = Player(board, 1) # we maken een speler
    game_over = False

    while not game_over: # oneindige loop
        if not player.pause:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pylint: disable=E1101
                    game_over = True
                if event.type == pygame.KEYDOWN: # pylint: disable=no-member
                    if event.key == 273 or event.key == 102: # Up or F
                        player.rotate(3, board)
                    if event.key == 100: # D
                        player.rotate(1, board)
                    if event.key == 276 or event.key == 275:
                        player.das_counter = -1


            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[276]:
                player.move(-1, board)
            if keys_pressed[275]:
                player.move(1, board)
            if keys_pressed[274]:
                try:
                    player.drop(board)
                except StopIteration:
                    game_over = True

            drawBoard(screen, board, player)

            try:
                player.next(board)
            except StopIteration:
                game_over = True

        clock.tick(60)
        print(player.das_counter)


    return player.score, player.lines, player.level

score, lines, level = mainGame()
print(f"Game over!\nYour score was {score},\nYou cleared {lines} lines and got to level {level}, well played!!")
pygame.quit() # pylint: disable=no-member