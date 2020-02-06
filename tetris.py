import pygame
import numpy as np  # for 2D fields
from player import Player
from helper import das, drawBoard
from init import board, screen, clock


def mainGame(level):
    player = Player(board, level)  # we maken een speler
    game_over = False

    while not game_over:  # oneindige loop
        for animation in player.animations:
            animation(screen)

        if player.pause_ftie == None:
            player.animations.clear()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pylint: disable=E1101
                    game_over = True
                if event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                    if event.key == 273 or event.key == 102:  # Up or F
                        player.rotate(3, board)
                    if event.key == 100:  # D
                        player.rotate(1, board)
                    if event.key == 276 or event.key == 275:
                        player.das = das(16, 6)

            keys_pressed = pygame.key.get_pressed()
            if keys_pressed[276]:
                player.move(-1, board)
            if keys_pressed[275]:
                player.move(1, board)
            if keys_pressed[274]:
                try:
                    if player.drop_ftie(2):
                        player.drop(board)
                except StopIteration:
                    game_over = True

            drawBoard(screen, board, player)

            try:
                player.next(board)
            except StopIteration:
                game_over = True

        else:
            if player.pause_ftie():
                player.pause_ftie = None

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # pylint: disable=E1101
                    game_over = True

        clock.tick(60)

    return player.score, player.lines, player.level


def menu():
    pass


score, lines, level = mainGame(5)
print(
    f"Game over!\nYour score was {score},\nYou cleared {lines} lines and got to level {level}, well played!!")
pygame.quit()  # pylint: disable=no-member
