import pygame
import numpy as np
import json

with open("high_scores.json", "r") as JSONFile:
    high_scores = json.load(JSONFile)

# Grootte van het bord
field = HEIGHT, WIDTH = (20, 10)


SQUARE_SIZE = 30
window_shape = window_width, window_height = (
    (WIDTH + 2 + 9) * SQUARE_SIZE, (HEIGHT + 1) * SQUARE_SIZE)

pygame.display.init()
pygame.font.init()
screen = pygame.display.set_mode(window_shape)
pygame.display.set_caption('Tetris')
clock = pygame.time.Clock()
font = pygame.font.Font("Redkost Comic.otf", 32)
