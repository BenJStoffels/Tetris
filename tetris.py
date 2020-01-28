import os
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
        [0, 1, 1],
        [1, 1, 0],
        [0, 0, 0]
    ]),
    np.array([
        [1, 1],
        [1, 1]
    ]),
    np.array([
        [0, 1, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]),
    np.array([
        [0, 0, 1],
        [1, 1, 1],
        [0, 0, 0]
    ]),
    np.array([
        [1, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]),
    np.array([
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 1, 1, 1],
        [0, 0, 0, 0]
    ])
]

# Grootte van het bord
field = HEIGHT, WIDTH = (15, 10)
# Maakt een 2d lijst gevuld met 0
board = np.zeros(field, dtype=int)

# Alles wat met de bewegende blok heeft te maken
class Player:
    def __init__(self, b):
        self.reset(b)

    # Zet de huidige blok in het veld
    def burn(self, b):
        min_y, min_x, off_y, off_x = self.rect
        for y in range(min_y, min_y + off_y):
            for x in range(min_x, min_x + off_x):
                if self.shape[y - min_y, x - min_x] == 1:
                    b[y, x] = 1

    # Kijkt of de huidige blok iets aanraakt
    def collides(self, b):
        min_y, min_x, off_y, off_x = self.rect
        if min_y < 0 or min_y + off_y > HEIGHT:
            return True
        if min_x < 0 or min_x + off_x >= WIDTH:
            return True

        for y in range(min_y, min_y+off_y):
            for x in range(min_x, min_x+off_x):
                if b[y, x] != 0 and self.shape[y-min_y, x-min_x] != 0:
                    return True
        return False

    # Beweegt de blok omlaag en kijkt of de blok helemaal beneden is
    def drop(self, b):
        self.y += 1
        if self.collides(b):
            self.y -= 1
            self.burn(b)
            self.reset(b)

    # voor naar links en rechts te bewegen
    # TODO: collision detection
    def move(self, d):
        self.x += d

    # Nieuwe blok en terug naar boven
    def reset(self, b):
        self.x = 4
        self.y = 0
        self.shape = random.choice(SHAPES)
        if self.collides(b):
            # Wanneer de nieuwe blok meteen iets raakt, is het spel gedaan,
            # raise zorgt ervoor dat er een Error komt (zie later)
            raise Exception("Game Over!!")


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

# print het bord, zoals de naam zegt
def printBoard(b, player=None):
    print_b = b.copy() # b is het bord zonder de huidige blok
    if player:
        player.burn(print_b) # we zetten de huidige blok in print_b, zonder het huidige veld aan te passen

    os.system("cls") # zorgt ervoor dat het vorige veld weg is
    for l in print_b:
        print("#", end="") # muur
        for e in l:
            print([" ", "&"][e], end="")
        print("#") # muur
    print("#"*12) # grond


player = Player(board) # we maken een speler

while True: # oneindige loop
    printBoard(board, player)
    try: # weet ge nog die error
        player.drop(board)
    except Exception: # dit vangt hem op zodat ge geen crash hebt
        break # gaat uit de oneindige loop
    else: # als er geen error was
        time.sleep(1/30) # wacht


print("Game Over!!") # game over!!!
