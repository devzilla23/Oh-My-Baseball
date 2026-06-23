########################################################################################################################
#   #Author: Devin Millage
#   #gamemode: player select
#   #Date:6/10/2026
#
# This is the file that handles the assignment of player positions and batting order
########################################################################################################################
#Imports
from _pyrepl import console
import pygame

from Data.Classes.Player import Position
from Data.Classes.Team import *
import json
from Data.Classes.teamMaker import makeTeams
import sys

#Globals
currselect = -1
poslist = [Position.CATCH, Position.FIRST, Position.SECOND, Position.SHORT, Position.THIRD, Position.LF, Position.CF, Position.RF, Position.PITCH]


#Main
pygame.init()
pygame.font.init()

width = 800
height = 480
FPS = 60

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
font1 = pygame.font.SysFont("couriernew", 12) #must be monospaced for columns to work used fore player roster
font2 = pygame.font.SysFont("couriernew", 20) #Used for continue text
font1.bold = True
pygame.display.set_caption("Oh My Baseball!")
clock = pygame.time.Clock()


def draw_field(team):
    """Draws a baseball diamond"""
    screen.fill((34, 139, 34)) #green background

    #List of locations of all bases in the infeild
    baseLocs = [ (width // 2 + 175, height // 2 + 150),  # home plate
        (width // 2 + 25, height // 2),  # 3rd base
        (width // 2 + 175, height //2 - 150),  # 2nd base
        (width // 2 + 325, height // 2),  # 1st base
    ]
    homeRect = pygame.Rect(0,0,30,30)
    homeRect.center = baseLocs[0]
    thirdRect = pygame.Rect(0, 0, 30, 30)
    thirdRect.center = baseLocs[1]
    secondRect = pygame.Rect(0, 0, 30, 30)
    secondRect.center = baseLocs[2]
    firstRect = pygame.Rect(0, 0, 30, 30)
    firstRect.center = baseLocs[3]
    pitchRect = pygame.Rect(0, 0, 30, 30)
    pitchRect.center = ((baseLocs[3][0] + baseLocs[1][0]) //2, baseLocs[1][1])
    LFRect = pygame.Rect(0, 0, 30, 30)
    LFRect.center = (((baseLocs[2][0] - baseLocs[1][0]) //2) + baseLocs[1][0] / 1.1, baseLocs[2][1])
    RFRect = pygame.Rect(0, 0, 30, 30)
    RFRect.center = (((baseLocs[3][0] - baseLocs[2][0]) // 2) + baseLocs[2][0] * 1.08, baseLocs[2][1])
    CFRect = pygame.Rect(0, 0, 30, 30)
    CFRect.center = ((baseLocs[2][0], baseLocs[2][1] - 50))
    shortRect = pygame.Rect(0, 0, 30, 30)
    shortRect.center = ((baseLocs[2][0] + baseLocs[1][0]) // 2, (baseLocs[2][1] + baseLocs[1][1]) // 2)
    basesList = [homeRect, firstRect, secondRect,  shortRect, thirdRect, LFRect, CFRect, RFRect, pitchRect]
    pygame.draw.polygon(screen, (244, 160, 100), baseLocs)
    pygame.draw.polygon(screen, (255, 255, 255), baseLocs, 3)


    for i in range(len(basesList)):
        pygame.draw.rect(screen, (245, 245, 245), basesList[i])
        for player in team.roster:
            if player.position == poslist[i]:
                bText = font1.render(player.getInitials(), True, (0, 0, 0))
                bTextRect = bText.get_rect()
                bTextRect.center = basesList[i].center
                screen.blit(bText, bTextRect)
    return basesList

def draw_batting(team):
    battList = []
    battRight = width//2
    incriment = 30
    for i in range(len(team.roster)):
        battRect = pygame.Rect(battRight+incriment, height - 50, 30, 30)
        pygame.draw.rect(screen, (245, 245, 245), battRect)
        incriment += 32
        battList.append(battRect)

    for i in range(len(battList)):
        for player in team.roster:
            if player.order == i and player.order != -1:
                bText = font1.render(player.getInitials(), True, (0, 0, 0))
                bTextRect = bText.get_rect()
                bTextRect.center = battList[i].center
                screen.blit(bText, bTextRect)
    return battList



def draw_team(team):
    rectList = []
    pygame.draw.rect(screen, (43, 45, 47), pygame.Rect(10,10, width//2 - 45, height - 20))
    textTop = 20
    incriment = (height - 20) // 9
    for player in team.roster:
        pText = font1.render(f"{player.name:<15} #{player.num:<2}    P: {player.pStat:<2} B: {player.bStat:<2} "
                             f"F: {player.fStat:<2} S: {player.sStat:<2}", True, (255, 255, 255))
        textRect = pText.get_rect()
        textRect.top = textTop
        textTop += incriment
        textRect.left = 20
        if player == team.roster[currselect] and currselect != -1:
            pygame.draw.rect(screen, (155, 161, 157), textRect)
        screen.blit(pText, textRect)
        rectList.append(textRect)
    return rectList

def draw_button(team, ready):
    buttonRect = pygame.Rect(width // 2 + 250, height // 2 + 150, 110, 30)
    cText = font2.render("Continue", True, (0, 0, 0))
    cTextRect = cText.get_rect()
    cTextRect.center = buttonRect.center
    if ready:
        pygame.draw.rect(screen, (173, 235, 179), buttonRect)
    else:
        pygame.draw.rect(screen, (190, 190, 190), buttonRect)
    screen.blit(cText, cTextRect)
    return buttonRect

def main():
    global currselect
    global width
    global height
    running = True
    team1, team2 = loadTeams()
    buttonRect = pygame.Rect(-1,-1,0, 0)
    rectList = []
    battList = []
    basesList = []
    doneSetup = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.VIDEORESIZE:
                width = event.w
                height = event.h
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                colFound = False
                for i in range(len(rectList)):
                    if rectList[i].collidepoint(event.pos):
                        currselect = i
                        colFound = True
                        break
                if not colFound and currselect != -1: #only if player is selected and new player was not clicked
                    for i in range(len(basesList)):
                        if basesList[i].collidepoint(event.pos):
                            colFound = True
                            for player in team1.roster:
                                if player.position == poslist[i]:
                                    player.position = Position.LEFTBENCH
                            team1.roster[currselect].position = poslist[i]
                            doneSetup = checkDone(team1)
                if not colFound and currselect != -1:
                    for i in range(len(battList)):
                        if battList[i].collidepoint(event.pos):
                            for player in team1.roster:
                                if player.order == i:
                                    player.order = -1
                            team1.roster[currselect].order = i
                            print(team1.roster[currselect].order)
                            doneSetup = checkDone(team1)
                if not colFound and doneSetup:
                    if buttonRect.collidepoint(event.pos):
                        running = False

        basesList = draw_field(team1)
        battList = draw_batting(team1)
        rectList = draw_team(team1)
        buttonRect = draw_button(team1, doneSetup)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


def checkDone(team):
    ready = True
    for player in team.roster:
        if player.position == Position.LEFTBENCH or player.order == -1:
            ready = False
            break
    return ready

def loadTeams():
    with open('Assets/homeTeam.json', 'r') as H:
        team1 = Team(**json.load(H))
    with open('Assets/awayTeam.json', 'r') as A:
        team2 = Team(**json.load(A))
    return team1, team2
makeTeams()
main()
