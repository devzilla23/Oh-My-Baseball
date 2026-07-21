########################################################################################################################
#   #Author: Devin Millage
#   #gamemode: Title Screen
#   #Date:7/21/2026
#
# This is the file that handles the title screen and mode selection
########################################################################################################################
#Imports
import pygame
from PIL.ImageChops import screen


class TitleScreen(object):
    def __init__(self, screen):
        pygame.font.init()
        self.screen = screen
        self.font1 = pygame.font.SysFont("couriernew", 40) #used for title
        self.font1.bold = True
        self.font2 = pygame.font.SysFont("couriernew", 22) #used for button text
        self.buttons = self.makeButtons()
        self.choice = None
        self.img = pygame.image.load("Data/Assets/sprites/titleScreen.png")

    def main(self, event):
        self.draw()
        if event != None and event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button[2].collidepoint(event.pos):
                    self.choice = button[0]

    def draw(self):
        """Draws the title screen"""
        self.screen.blit(self.img, (0, 0))

        for button in self.buttons:
            pygame.draw.rect(self.screen, (220, 220, 220), button[2])
            pygame.draw.rect(self.screen, (0, 0, 0), button[2], 2) #button border
            text = self.font2.render(button[1], True, (0, 0, 0))
            text_rect = text.get_rect(center=button[2].center)
            self.screen.blit(text, text_rect)

    def makeButtons(self):
        """Builds rects for the title screen buttons"""
        button_defs = [
            ("play", "Play Ball"),
            ("shop", "Shop"),
            ("quit", "Quit"),
        ]

        y = 200
        buttons = []
        for key, label in button_defs:
            rect = pygame.Rect(self.screen.get_width() // 2 - 240 // 2, y, 240, 44)
            buttons.append((key, label, rect))
            y += 44 + 14

        return buttons