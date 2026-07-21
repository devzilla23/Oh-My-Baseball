########################################################################################################################
#   #Author: Devin Millage
#   #gamemode: ohMyBaseball driver
#   #Date:6/10/2026
#
# This is the file that handles the assignment of player positions and batting order
########################################################################################################################
import sys
import Data.Shop as shop
import json
import Data.TitleScreen as TitleScreen
from enum import IntEnum
import pygame

pygame.init()
pygame.font.init()

from Data import playone, Shop  # game file


class Mode(IntEnum):
    TITLE = 0
    PLAY = 1
    SHOP = 2


########################################################################################################################
# Main
def main():
    width = 800
    height = 480
    FPS = 60
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Oh My Baseball!")
    title = TitleScreen.TitleScreen(screen)
    shop = Shop.shop(screen)
    running = True
    game = playone.Game()
    game.setup(screen)
    mode = Mode.TITLE

    while running:
        event2 = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h
            elif event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                event2 = event

        if not running:
            break

        if mode == Mode.TITLE:
            title.main(event2)
            if title.choice == "play":
                mode = Mode.PLAY
                title.choice = None
                game.startNewRound()
            elif title.choice == "shop":
                mode = Mode.SHOP
                title.choice = None
            elif title.choice == "quit":
                running = False
        elif mode == Mode.SHOP:
            shop.main(event2)
            if shop.exit:
                shop.exit = False
                mode = Mode.TITLE
        elif mode == Mode.PLAY:
            game.renderField(screen, width, height, event2)
            if game.exit:
                game.exit = False
                mode = Mode.TITLE

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


main()