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

import pygame

pygame.init()
pygame.font.init()

from Data import playone, Shop  # game file
########################################################################################################################
#Main
def main():
    

    width = 800
    height = 480
    FPS = 60
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Oh My Baseball!")
    shop = Shop.shop(screen)
    running = True
    game = playone.Game()
    game.setup(screen)

    while running:
        hasEvent = False
        for event in pygame.event.get():
            hasEvent = True
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h
            else:
                #shop.main(event)
                game.renderField(screen, width, height, event)
        if not hasEvent:
            #shop.main(event)
            game.renderField(screen, width, height, None)

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit() 
    sys.exit()

main()



   