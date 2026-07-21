########################################################################################################################
#   #Author: Devin Millage
#   #gamemode: fielder class
#   #Date:7/17/2026
#
# The class for the fielders
########################################################################################################################
from enum import Enum
import pygame
import math


class POS(Enum):
    PITCH = (717, 1240)
    CATCH = (720, 1570)

class FielderState(Enum):
    HOME = 0

class Fielder(object):
    """Fielder class"""
    def __init__(self, homePos, screen, cam):
        self.image = pygame.image.load("Data/Assets/sprites/fielder.png").convert_alpha()
        self.screen = screen
        self.cam = cam
        if homePos == 0:
            self.homePos = POS.CATCH
        elif homePos == 1:
            self.homePos = POS.PITCH
        else:
            self.homePos = POS.NONE
        self.rect = pygame.Rect(self.homePos.value[0], self.homePos.value[1], self.image.get_width(), self.image.get_height())


    def update(self):
        self.screen.blit(self.image, (self.rect.x - self.cam.x, self.rect.y - self.cam.y))

