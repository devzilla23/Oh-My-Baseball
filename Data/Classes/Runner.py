########################################################################################################################
#   #Author: Devin Millage
#   #gamemode: runner class
#   #Date:7/15/2026
#
# The class for the runner
########################################################################################################################
from enum import Enum
import pygame
import math

class destination(Enum):
    "the x and y values of the base that the runner targets"
    FIRST = (1040,1245)
    SECOND = (740,990)
    THIRD = (450,1240)
    HOME = (740,1540)
    

class Runner(object):
    def __init__(self, player, screen,cam):
        self.player = player
        self.destination = destination.FIRST 
        self.image = pygame.image.load("Data/Assets/sprites/helmet.png").convert_alpha()
        self.rect = pygame.Rect(724,1527, self.image.get_width(), self.image.get_height())
        self.screen = screen
        self.cam = cam
        
    def run(self):
        """run to destination"""
        speed = self.player.sStat / 12
        destX, destY = self.destination.value
        dx = destX - self.rect.x
        dy = destY - self.rect.y
        print (dx, dy)
        distance = math.hypot(dx, dy)
        dx /= distance
        dy /= distance

        if distance - speed < 1:
            if self.destination != destination.HOME:
                self.nextBase()
                self.rect.x, self.rect.y = destX, destY
            else:
                return False
        else:
            self.rect.x += dx * speed
            self.rect.y += dy * speed
        self.screen.blit(self.image, (self.rect.x - self.cam.x, self.rect.y - self.cam.y))
        return True


    def nextBase(self):
        if self.destination == destination.FIRST:
            self.destination = destination.SECOND
        elif self.destination == destination.SECOND:
            self.destination = destination.THIRD
        elif self.destination == destination.THIRD:
            self.destination = destination.HOME
        
