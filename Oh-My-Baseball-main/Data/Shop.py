########################################################################################################################
#   #Author: Devin Millage
#   #gamemode: Shop
#   #Date:7/20/2026
#
# This is the file that handles the purchasing of new attributes
########################################################################################################################
#Imports
import pygame
import random
import json

class shop(object):
    # Class variables
    def __init__(self, screen):
        #Font setup
        pygame.font.init()
        self.font1 = pygame.font.SysFont("couriernew", 25) #used for title
        self.font2 = pygame.font.SysFont("couriernew", 18) #Used button text
        self.font1.bold = True
        self.stats = self.loadStatsSheet()
        self.bStat = self.stats[0] #batting stat
        self.cStat = self.stats[1] #contact stat (less likelihood of fouls)
        self.nStat = self.stats[2] #number of pitches
        self.dStat = self.stats[3] #distance multiplier
        self.screen = screen
        self.buttons = self.makeButtons()
        self.ft = self.loadFtSheet()
        self.costs = self.loadCostsSheet()

    def main(self, event):
        self.draw()
        if event.type == pygame.MOUSEBUTTONDOWN:
            for button in self.buttons:
                if button[3].collidepoint(event.pos):
                    if button[0] == "exit":
                        self.exitShop()
                        return
                    else:
                        self.upgradeStat(button[0], button[2])



    def draw(self):
        """Draws the screen"""
        self.screen.fill((34, 139, 34)) #green background

        ft = self.font1.render(f"{self.ft:.0f} ft", True, (255, 255, 255))
        ft_rect = ft.get_rect(topright=(self.screen.get_width() - 20, 15))
        self.screen.blit(ft, ft_rect)

        for button in self.buttons:
            pygame.draw.rect(self.screen, (220, 220, 220), button[3])
            pygame.draw.rect(self.screen, (0, 0, 0), button[3], 2) #button border
            text = None
            if button[0] == "exit":
                text = "Exit"
                value = -1
            elif button[0] == "bStat":
                value = self.bStat
            elif button[0] == "cStat":
                value = self.cStat
            elif button[0] == "nStat":
                value = self.nStat
            elif button[0] == "dStat":
                value = self.dStat
            maxed = " (MAX)" if value >= button[2] else ""
            if value != -1:
                text = f'{button[1]}: {value}/{button[2]}{maxed}'
            text = self.font2.render(text, True, (0, 0, 0))
            text_rect = text.get_rect(center=button[3].center)
            self.screen.blit(text, text_rect)

            if button[0] != "exit":
                is_maxed = value >= button[2]
                if is_maxed:
                    cost_str = "MAXED"
                else:
                    cost_str = f"{self.costs[button[0]]} ft"
                if is_maxed:
                    cost_color = (170, 170, 170)
                else:
                    cost_color = (255, 255, 255)
                cost_text = self.font2.render(cost_str, True, cost_color)
                cost_rect = cost_text.get_rect(midleft=(button[3].right + 15, button[3].centery))
                self.screen.blit(cost_text, cost_rect)

        title = self.font1.render("SHOP", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.screen.get_rect().centerx, 40))
        self.screen.blit(title, title_rect)



    def createStatsSheet(self):
        self.stats = [self.bStat, self.cStat, self.nStat, self.dStat]
        with open("Data/playerStats.json", "w") as file:
            json.dump(self.stats, file)

    def createFtSheet(self):
        with open("Data/playerFt.json", "w") as file:
            json.dump(self.ft, file)

    def loadStatsSheet(self):
        with open("Data/playerStats.json", "r") as file:
            return json.load(file)
    def loadFtSheet(self):
        with open("Data/playerFt.json", "r") as file:
            return json.load(file)

    def createCostsSheet(self):
        with open("Data/costs.json", "w") as file:
            json.dump(self.costs, file)

    def loadCostsSheet(self):
        with open("Data/costs.json", "r") as file:
            return json.load(file)

    def makeButtons(self):
        """Builds rects buttons"""
        stat_defs = [
            ("bStat", "Batting", 99),
            ("cStat", "Contact", 99),
            ("nStat", "Pitches", 20),
            ("dStat", "Distance", 99),
        ]

        y = 80
        buttons = []
        for stat, label, maxVal in stat_defs:
            rect = pygame.Rect(self.screen.get_width() // 2 - 240 // 2, y, 240, 44)
            buttons.append((stat, label, maxVal,rect))
            y += 44 + 14

        y += 20  # extra gap before Exit
        exit_rect = pygame.Rect(self.screen.get_width() // 2 - 240 // 2, y, 240, 44)
        buttons.append(("exit", "Exit", 0, exit_rect))

        return buttons

    def upgradeStat(self, key, max):
        """Raises one stat by 1"""
        cost = self.costs[key]
        if key == "bStat" and self.bStat < max and self.ft > cost:
            self.bStat += 1
            self.ft -= cost
            self.costs[key] = round(cost * 1.5)
        elif key == "cStat" and self.cStat < max and self.ft > cost:
            self.cStat += 1
            self.ft -= cost
            self.costs[key] = round(cost * 1.5)
        elif key == "nStat" and self.nStat < max and self.ft > cost:
            self.nStat += 1
            self.ft -= cost
            self.costs[key] = round(cost * 1.5)
        elif key == "dStat" and self.dStat < max and self.ft > cost:
            self.dStat += 1
            self.ft -= cost
            self.costs[key] = round(cost * 1.5)

    def exitShop(self):
        """Saves current stats to disk and stops the shop loop."""
        self.createStatsSheet()
        self.createFtSheet()
        self.createCostsSheet()

