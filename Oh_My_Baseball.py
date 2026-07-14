########################################################################################################################
#   #Author: Devin Millage
#   #gamemode: ohMyBaseball driver
#   #Date:6/10/2026
#
# This is the file that handles the assignment of player positions and batting order
########################################################################################################################
import sys

import json

import pygame

pygame.init()
pygame.font.init()

from Data import oneP # team setup file
import Data.Classes.Team as Team
from Data import playone # game file
########################################################################################################################
#Main
def main():
    

    width = 800
    height = 480
    FPS = 60
    clock = pygame.time.Clock()
    team1, team2 = loadTeams()
    teamSet = oneP.oneP(team1)
    game = playone.Game(team1, team2)


    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("Oh My Baseball!")
    game.setup()
    running = True
    homeTeam = None
    while running:
        hasEvent = False
        for event in pygame.event.get():
            hasEvent = True
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h
            elif homeTeam == None:
                homeTeam = teamSet.main(screen, event, width, height)
            else:
                game.renderField(screen, width, height, event)
        if homeTeam != None and not hasEvent:
            game.renderField(screen, width, height, None)

        clock.tick(FPS)
        pygame.display.flip()

    pygame.quit() 
    sys.exit()

def loadTeams():
    with open('Data/Assets/homeTeam.json', 'r') as H:
        team1 = Team.Team(**json.load(H))
    with open('Data/Assets/awayTeam.json', 'r') as A:
        team2 = Team.Team(**json.load(A))
    return team1, team2

main()



   