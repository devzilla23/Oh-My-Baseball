########################################################################################################################
#   #Author: Devin Millage
#   #gamemode: one player game
#   #Date:6/10/2026
#
# This is the file that handles the game
########################################################################################################################
#Imports
import pygame
import random
from Data.Classes.Player import Position
from Data.Classes.Team import *
from Data.Classes.teamMaker import makeTeams

@dataclass
class Game:
    #Class Variables
    team1: Team #home team
    team2: Team #away team
    fieldRect = pygame.Rect(-1,-1,0, 0)
    camRect = pygame.Rect(0,0,800, 480)
    fieldImage = None
    playerimg = None
    dx = 10


    def renderField(self, screen, width, height,event):
        """Draws the field and sets up the camera"""
        self.camRect.width = width
        self.camRect.height = height
        #Draws the field
        if event != None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.camRect.x > 10:
                    self.camRect.x -= 10
                elif event.key == pygame.K_RIGHT and self.camRect.x < self.fieldRect.width - self.camRect.width - 10:
                    self.camRect.x += 10
                elif event.key == pygame.K_UP and self.camRect.y > 10:
                    self.camRect.y -= 10
                elif event.key == pygame.K_DOWN and self.camRect.y < self.fieldRect.height - self.camRect.height - 10:
                    self.camRect.y += 10
        self.playerRect.x += self.dx
        if self.playerRect.x + self.playerRect.width > self.fieldRect.width or self.playerRect.x < 0:
            self.dx *= -1
        screen.blit(self.fieldImage, (0, 0), self.camRect)
        screen.blit(self.playerimg, (self.playerRect.x - self.camRect.x, self.playerRect.y - self.camRect.y))

    def setup(self):
        self.fieldImage = pygame.image.load("Data/Assets/sprites/parkPlacehold.jpg").convert()
        self.fieldRect = pygame.Rect(0, 0, self.fieldImage.get_width(), self.fieldImage.get_height())
        self.playerimg = pygame.image.load("Data/Assets/sprites/playerPlaceholder.png").convert_alpha()
        self.playerRect = pygame.Rect(0, 0, self.playerimg.get_width(), self.playerimg.get_height())
    


    
    
        
