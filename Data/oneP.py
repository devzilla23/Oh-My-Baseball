########################################################################################################################
#   #Author: Devin Millage
#   #gamemode: player select
#   #Date:6/10/2026
#
# This is the file that handles the assignment of player positions and batting order
########################################################################################################################
#Imports
import pygame
import random
from Data.Classes.Player import Position
from Data.Classes.Team import *
from Data.Classes.teamMaker import makeTeams


@dataclass
class oneP:
    #Class variables
    currselect = -1
    poslist = [Position.CATCH, Position.FIRST, Position.SECOND, Position.SHORT, Position.THIRD, Position.LF, Position.CF, Position.RF, Position.PITCH]
    rectList = []
    battList = []
    basesList = []
    contRect = pygame.Rect(-1,-1,0, 0)
    randRect = pygame.Rect(-1,-1,0, 0)


    #Font setup
    font1 = pygame.font.SysFont("couriernew", 12) #must be monospaced for columns to work used fore player roster
    font2 = pygame.font.SysFont("couriernew", 20) #Used for continue text
    font1.bold = True
    team: Team




    def draw_field(self, screen, width, height):
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
        secondRect.center = ((baseLocs[2][0] + baseLocs[3][0]) // 2, (baseLocs[2][1] + baseLocs[3][1]) // 2)
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
        self.basesList = [homeRect, firstRect, secondRect,  shortRect, thirdRect, LFRect, CFRect, RFRect, pitchRect]
        pygame.draw.polygon(screen, (244, 160, 100), baseLocs)
        pygame.draw.polygon(screen, (255, 255, 255), baseLocs, 3)


        for i in range(len(self.basesList)):
            pygame.draw.rect(screen, (245, 245, 245), self.basesList[i])
            for player in self.team.roster:
                if player.position == self.poslist[i]:
                    bText = self.font1.render(player.getInitials(), True, (0, 0, 0))
                    bTextRect = bText.get_rect()
                    bTextRect.center = self.basesList[i].center
                    screen.blit(bText, bTextRect)

    def draw_batting(self, width, height, screen):
        self.battList = []
        battRight = width//2
        incriment = 30
        for i in range(len(self.team.roster)):
            battRect = pygame.Rect(battRight+incriment, height - 50, 30, 30)
            pygame.draw.rect(screen, (245, 245, 245), battRect)
            incriment += 32
            self.battList.append(battRect)

        for i in range(len(self.battList)):
            for player in self.team.roster:
                if player.order == i and player.order != -1:
                    bText = self.font1.render(player.getInitials(), True, (0, 0, 0))
                    bTextRect = bText.get_rect()
                    bTextRect.center = self.battList[i].center
                    screen.blit(bText, bTextRect)
        



    def draw_team(self, screen, width, height):
        self.rectList = []
        pygame.draw.rect(screen, (43, 45, 47), pygame.Rect(10,10, width//2 - 45, height - 20))
        textTop = 20
        incriment = (height - 20) // 9
        for player in self.team.roster:
            pText = self.font1.render(f"{player.name:<15} #{player.num:<2}    P: {player.pStat:<2} B: {player.bStat:<2} "
                                f"F: {player.fStat:<2} S: {player.sStat:<2}", True, (255, 255, 255))
            textRect = pText.get_rect()
            textRect.top = textTop
            textTop += incriment
            textRect.left = 20
            if player == self.team.roster[self.currselect] and self.currselect != -1:
                pygame.draw.rect(screen, (155, 161, 157), textRect)
            screen.blit(pText, textRect)
            self.rectList.append(textRect)


    def draw_continue(self, ready, screen, width, height):
        self.contRect = pygame.Rect(width // 2 + 250, height // 2 + 150, 110, 30)
        cText = self.font2.render("Continue", True, (0, 0, 0))
        cTextRect = cText.get_rect()
        cTextRect.center = self.contRect.center
        if ready:
            pygame.draw.rect(screen, (173, 235, 179), self.contRect)
        else:
            pygame.draw.rect(screen, (190, 190, 190), self.contRect)
        screen.blit(cText, cTextRect)

    def draw_random(self, screen, width, height):
        self.randRect = pygame.Rect(width // 2, height // 2 + 150, 110, 30)
        cText = self.font2.render("Random", True, (0, 0, 0))
        cTextRect = cText.get_rect()
        cTextRect.center = self.randRect.center
        pygame.draw.rect(screen, (173, 235, 179), self.randRect)

        screen.blit(cText, cTextRect)

    def main(self, screen, event, w, h):
        doneSetup = self.checkDone()

        if event.type == pygame.MOUSEBUTTONDOWN:
            colFound = False
            for i in range(len(self.rectList)):
                if self.rectList[i].collidepoint(event.pos):
                    self.currselect = i
                    colFound = True
                    break
            if not colFound and self.currselect != -1: #only if player is selected and new player was not clicked
                for i in range(len(self.basesList)):
                    if self.basesList[i].collidepoint(event.pos):
                        colFound = True
                        for player in self.team.roster:
                            if player.position == self.poslist[i]:
                                player.position = Position.LEFTBENCH
                        self.team.roster[self.currselect].position = self.poslist[i]
            if not colFound and self.currselect != -1:
                for i in range(len(self.battList)):
                    if self.battList[i].collidepoint(event.pos):
                        for player in self.team.roster:
                            if player.order == i:
                                player.order = -1
                        self.team.roster[self.currselect].order = i
                        print(self.team.roster[self.currselect].order)
            if not colFound and doneSetup:
                if doneSetup and self.contRect.collidepoint(event.pos):
                    return self.team
            if not colFound and self.randRect.collidepoint(event.pos):
                posListLocal = [Position.CATCH, Position.FIRST, Position.SECOND, Position.SHORT, Position.THIRD, Position.LF, Position.CF, Position.RF, Position.PITCH]
                random.shuffle(posListLocal)
                battRange = [0, 1, 2, 3, 4, 5, 6, 7, 8]
                random.shuffle(battRange)
                for i in range (len(self.team.roster)):
                    self.team.roster[i].position = posListLocal[i]
                    self.team.roster[i].order = battRange[i]

            

        self.draw_field(screen, w, h)
        self.draw_batting( w, h, screen)
        self.draw_team(screen, w, h)
        self.draw_continue(doneSetup, screen, w, h)
        self.draw_random(screen, w, h)


    def checkDone(self):
        """Checks if all players have been assigned a position and batting order"""
        ready = True
        for player in self.team.roster:
            if player.position == Position.LEFTBENCH or player.order == -1:
                ready = False
                break
        return ready