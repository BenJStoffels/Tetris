import random
from helper import SHAPES, das, drop, pause, clearLines, createBlockdropAnimation
from init import HEIGHT, WIDTH
import numpy as np

class Player:
    def __init__(self, b, level):
        self.x = 4
        self.y = 0
        self.nextShape = random.choice(SHAPES).copy()
        self.shape = random.choice(SHAPES).copy()
        while self.shape[-self.y, :].max() == 0:
            self.y -= 1
        self.level = level
        self.lines = 0
        self.score = 0
        self.linesUntilNextLevel = min((level + 1) * 10, max(100, level * 10 - 50))
        self.pause_ftie = None
        self.das = das(16, 6)
        self.drop_ftie = drop(self.dropRate, True)
        self.animations = []

    # Zet de huidige blok in het veld
    def burn(self, b):
        min_y, min_x, off_y, off_x = self.rect
        for y in range(min_y, min_y + off_y):
            for x in range(min_x, min_x + off_x):
                if self.shape[y - min_y, x - min_x] != 0:
                    b[y, x] = self.shape[y - min_y, x - min_x]

    def calcDelay(self, lines):
        y = self.y + self.shape.shape[0]
        delay = 2 * ((21 - y) // 4) + 10
        if lines:
            delay += 20
        return delay

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
        if self.collides(b):
            self.y -= 1
            self.reset(b)

    # voor naar links en rechts te bewegen
    def move(self, d, b):
        if self.das():
            self.x += d
            if self.collides(b):
                self.das(True)
                self.x -= d

    def next(self, b):
        
        if self.drop_ftie():
            self.drop(b)


    # Nieuwe blok en terug naar boven
    def reset(self, b):
        self.burn(b)
        huidige_lines = clearLines(b)
        self.lines += huidige_lines
        self.linesUntilNextLevel -= huidige_lines
        self.score += self.calcScore(huidige_lines)
        self.pause_ftie = pause(self.calcDelay(huidige_lines != 0))

        self.animations.append(createBlockdropAnimation({"x": self.x, "y": self.y, "shape": self.shape.copy()}))

        if self.linesUntilNextLevel <= 0:
            self.level += 1
            self.drop_ftie = drop(self.dropRate)
            self.linesUntilNextLevel = 10

        self.x = 4
        self.y = 0
        self.shape = self.nextShape.copy()
        self.nextShape = random.choice(SHAPES).copy()
        while self.shape[-self.y, :].max() == 0:
            self.y -= 1
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
