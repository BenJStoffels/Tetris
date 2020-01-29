import os
import pygame
import numpy as np # for 2D fields
import time
import random

# Al de vormen
SHAPES = [
    np.array([
        [1, 1, 0],
        [0, 1, 1],
        [0, 0, 0]
    ]),
    np.array([
        [0, 2, 2],
        [2, 2, 0],
        [0, 0, 0]
    ]),
    np.array([
        [3, 3],
        [3, 3]
    ]),
    np.array([
        [0, 4, 0],
        [4, 4, 4],
        [0, 0, 0]
    ]),
    np.array([
        [0, 0, 5],
        [5, 5, 5],
        [0, 0, 0]
    ]),
    np.array([
        [6, 0, 0],
        [6, 6, 6],
        [0, 0, 0]
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
field = HEIGHT, WIDTH = (21, 10)
# Maakt een 2d lijst gevuld met 0
board = np.zeros(field, dtype=int)

SQUARE_SIZE = 20
window_shape = window_height, window_width = ((HEIGHT + 1) * SQUARE_SIZE, (WIDTH + 2) * SQUARE_SIZE)

pygame.display.init()
screen = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()

# Alles wat met de bewegende blok heeft te maken
class Player:
    def __init__(self, b, level):
        self.level = level
        self.counter = 0
        self.reset(b)

    # Zet de huidige blok in het veld
    def burn(self, b):
        min_y, min_x, off_y, off_x = self.rect
        for y in range(min_y, min_y + off_y):
            for x in range(min_x, min_x + off_x):
                if self.shape[y - min_y, x - min_x] != 0:
                    b[y, x] = self.shape[y - min_y, x - min_x]

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
            self.reset(b)

    # voor naar links en rechts te bewegen
    def move(self, d, b):
        self.x += d
        if self.collides(b):
            self.x -= d

    def next(self, b):
        self.counter += 1
        
        if self.counter == self.dropRate:
            self.drop(b)

        return True

    # Nieuwe blok en terug naar boven
    def reset(self, b):
        self.x = 4
        self.y = 0
        self.shape = random.choice(SHAPES)
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
        return [48, 43, 38, 33, 28, 23, 18, 13, 8, 6, 5, 5, 5, 4, 4, 4, 3, 3, 3, 2, 2, 2, 2,2,2,2,2,2,1][self.level % 30]

    # Niet belangrijk
    @dropRate.setter
    def set_dropRate(self, val):
        raise PermissionError(
            "You can't set the dropRate attr, you should change the level instead!")


def drawBoard(s, b, player=None):
    print_b = b.copy() # b is het bord zonder de huidige blok
    if player:
        player.burn(print_b) # we zetten de huidige blok in print_b, zonder het huidige veld aan te passen

    pygame.draw.rect(s, COLORS[0], (0, 0, window_width, window_height))
    for y, l in enumerate(print_b):
        pygame.draw.rect(s, COLORS[8], (0, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
        for x, e in enumerate(l):
            if e > 0:
                pygame.draw.rect(s, COLORS[e], ((x + 1) * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        pygame.draw.rect(s, COLORS[8], ((window_width - SQUARE_SIZE), y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    pygame.draw.rect(s, COLORS[8], (0, window_height - SQUARE_SIZE, window_width, SQUARE_SIZE))
    pygame.display.update()
        
    


player = Player(board, 1) # we maken een speler
game_over = True

while game_over: # oneindige loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # pylint: disable=E1101
            game_over = False
        if event.type == pygame.KEYDOWN: # pylint: disable=no-member
            if event.key == 276: # Left
                player.move(-1, board)
            if event.key == 275: # Right
                player.move(1, board)
            if event.key == 273: # Up
                player.rotate(1, board)
            if event.key == 274: # Down
                player.drop(board)

    drawBoard(screen, board, player)

    try:
        player.next(board)
    except StopIteration:
        break

    clock.tick(60)


print("Game Over!!") # game over!!!
pygame.quit() # pylint: disable=no-member