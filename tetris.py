import pygame
import numpy as np  # for 2D fields
from player import Player
from helper import das, drawBoard, drawMenu
from init import screen, clock, field, high_scores
import json


def mainGame(level, seed=None):
    if seed == None:
        seed = 10  # generate random seed
    # Maakt een 2d lijst gevuld met 0
    board = np.zeros(field, dtype=int)
    player = Player(board, level, seed)  # we maken een speler
    game_over = False

    while not game_over:  # oneindige loop
        for animation in player.animations:
            if animation(screen):
                player.animations.pop()

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
                        player.resetDas()

            keys_pressed = pygame.key.get_pressed()
            if not (keys_pressed[276] and keys_pressed[275]):
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

            def quit_action():
                nonlocal game_over
                game_over = True

            drawBoard(screen, board, player, quit_action)

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

    return player.score, player.lines, player.level, player.tetrisCounter


def menu():
    quit_bool = False
    button_clicked = False
    current_level = 15
    prev_score = ""
    while not quit_bool:
        if button_clicked:
            button_clicked = False
            score, lines, level, tetrisCount = mainGame(current_level)

            if score > high_scores[-1]["score"]:
                Score_Obj = {
                    "Name": "Ben",
                    "score": score,
                    "lines": lines,
                    "level": level,
                    "tetrisCount": tetrisCount
                }
                if score > high_scores[0]["score"]:
                    high_scores.insert(0, Score_Obj)
                    high_scores.pop()
                else:
                    i = len(high_scores) - 1
                    while score > high_scores[i]["score"]:
                        i -= 1
                    i += 1
                    high_scores.insert(i, Score_Obj)
                    high_scores.pop()

                print("you got in the top 5")
                with open("high_scores.json", "w") as JSONFile:
                    json.dump(high_scores, JSONFile, indent=True)

            prev_score = f"Game over!\nYour score was {score},\nYou cleared {lines} lines\nwith {tetrisCount} tetrises and\ngot to level {level},\nwell played!!"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=E1101
                quit_bool = True

        def action():
            nonlocal button_clicked
            button_clicked = True

        def level_action(level, unit=False):
            nonlocal current_level
            if not unit:
                current_level = level + current_level % 10
            else:
                current_level = (current_level // 10) * 10 + level

        drawMenu(screen, prev_score, current_level,
                 action, level_select_action=level_action)


if __name__ == "__main__":
    menu()
    pygame.quit()  # pylint: disable=no-member
