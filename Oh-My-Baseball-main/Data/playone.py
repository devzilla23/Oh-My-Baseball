########################################################################################################################
#   #Author: Devin Millage
#   #gamemode: one player game
#   #Date:6/10/2026
#
# This is the file that handles the game
########################################################################################################################
# Imports
import pygame
import random
from dataclasses import dataclass
from enum import IntEnum
from Data.Classes.Fielder import *
import json


class ballState(IntEnum):
    PITCHING = 0
    BALLHIT = 1
    NONE = 3
    GAMEOVER = 4
    FOUL = 5


@dataclass
class Game:
    # Class Variables
    fieldRect = pygame.Rect(-1, -1, 0, 0)
    camRect = pygame.Rect(0, 0, 800, 480)
    ballRect = pygame.Rect(-1, -1, 0, 0)
    fieldImage = None
    ballImg = None
    ballState = ballState.NONE
    balldx = 0
    balldy = 0
    ballRot = 0  # curremt rotation of the ball
    ballSpin = 0  # spin speed of the ball
    shadowImg = None
    batImgList = []
    batAnimIndex = 0  # current frame of the swing
    batRect = None
    isSwinging = False
    hasSwung = False
    fielders = []
    landSpot = None
    ballHeight = 0
    stats = [0, 0, 0, 0]
    maxPitches = 3
    pitches = 0
    totDist = 0
    font1 = None
    font2 = None
    font3 = None
    exit = False
    noPitch = False
    isFoul = False
    lastHitDist = 0
    showHitText = False
    hitTextTimer = 0

    def renderField(self, screen, width, height, event):
        """Draws the field and sets up the camera"""
        self.camRect.width = width
        self.camRect.height = height

        if event != None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.ballState == ballState.NONE:
                    self.pitch()
                elif event.key == pygame.K_SPACE and self.ballState == ballState.PITCHING and not self.hasSwung:
                    self.isSwinging = True
                    self.hasSwung = True
                elif event.key == pygame.K_UP:
                    self.camRect.y -= 10

        if self.isSwinging:
            self.startBatAnim(screen, self.camRect)
        screen.blit(self.fieldImage, (0, 0), self.camRect)
        screen.blit(self.batImgList[self.batAnimIndex],
                    (self.batRect.x - self.camRect.x, self.batRect.y - self.camRect.y))
        if self.ballState == ballState.PITCHING:
            self.pitch()
            self.spinBall()
            rotatedBall = pygame.transform.rotate(self.ballImg, self.ballRot)
            rotatedRect = rotatedBall.get_rect(center=self.ballRect.center)

            screen.blit(rotatedBall, (rotatedRect.x - self.camRect.x, rotatedRect.y - self.camRect.y))
            self.camMove(self.ballRect, self.balldx, self.balldy)

        for f in self.fielders:
            f.update()

        if self.ballState == ballState.BALLHIT or self.ballState == ballState.FOUL:
            self.moveHitBall(event, screen)
            self.spinBall()

            scale = (300 + self.ballHeight) / 300
            ballTrans = pygame.transform.scale(self.ballImg, ((self.ballImg.get_width() * scale),
                                                              (self.ballImg.get_height() * scale)))
            rotatedBall = pygame.transform.rotate(ballTrans, self.ballRot)
            rotatedRect = rotatedBall.get_rect(center=self.ballRect.center)
            screen.blit(self.shadowImg,
                        (self.ballRect.x - self.camRect.x, self.ballRect.y + self.ballHeight - self.camRect.y))
            screen.blit(rotatedBall, (rotatedRect.x - self.camRect.x, rotatedRect.y - self.camRect.y))
            self.camMove(self.ballRect, self.balldx, self.balldy)
        if self.pitches == self.maxPitches:
            self.noPitch = True
        if self.noPitch and (self.ballState == ballState.NONE or self.ballState == ballState.GAMEOVER):
            self.gameEnd(event, screen)

        self.drawUI(screen)

    def setup(self, screen):
        """One-time setup: fonts, fielders, and all sprite images. This does real
        disk I/O and surface conversion (30+ images), so it should only run once
        when the program starts - not every time a new round begins."""
        pygame.font.init()
        self.font1 = pygame.font.SysFont("couriernew", 40)
        self.font1.bold = True
        self.font2 = pygame.font.SysFont("couriernew", 24)
        self.font3 = pygame.font.SysFont("couriernew", 36)
        self.font3.bold = True
        for i in range(2):
            fielder = Fielder(i, screen, self.camRect)
            self.fielders.append(fielder)
        self.fieldImage = pygame.image.load("Data/Assets/sprites/field.png").convert()
        self.fieldRect = pygame.Rect(0, 0, self.fieldImage.get_width(), self.fieldImage.get_height())
        self.ballImg = pygame.image.load("Data/Assets/sprites/ball.png").convert_alpha()
        self.ballRect = pygame.Rect(0, 0, self.ballImg.get_width(), self.ballImg.get_height())
        self.shadowImg = pygame.image.load("Data/Assets/sprites/shadow.png").convert_alpha()
        self.batRect = pygame.Rect(690, 1410, 100, 200)
        for i in range(28):
            bat = pygame.image.load(f'Data/Assets/sprites/bat_anim/bat-{i + 1}.png').convert_alpha()
            self.batImgList.append(bat)

        # Load the player's saved stats/ft balance for the very first round too
        self.startNewRound()

    def startNewRound(self):
        self.stats = self.loadStatsSheet()
        self.totDist = self.loadFtSheet()
        self.maxPitches = 3 + self.stats[2]

        self.pitches = 0
        self.ballState = ballState.NONE
        self.noPitch = False
        self.isFoul = False
        self.isSwinging = False
        self.hasSwung = False
        self.batAnimIndex = 0
        self.lastHitDist = 0
        self.showHitText = False
        self.hitTextTimer = 0
        self.exit = False
        self.camRect.x = 340
        self.camRect.y = 1125

    def camMove(self, objRect, speedx, speedy):
        """makes the camera follow an object"""
        boxRect = pygame.Rect(self.camRect.x + (self.camRect.width * 0.1), self.camRect.y + (self.camRect.height * 0.1),
                              self.camRect.width * 0.8, self.camRect.height * 0.8)
        if objRect.x <= boxRect.x and self.camRect.x > 0:
            self.camRect.x -= abs(speedx)
        if objRect.x + objRect.width >= boxRect.x + boxRect.width and self.camRect.x + self.camRect.width < self.fieldRect.width:
            self.camRect.x += abs(speedx)
        if objRect.y <= boxRect.y and self.camRect.y > 0:
            self.camRect.y -= abs(speedy)
        if objRect.y + objRect.height >= boxRect.y + boxRect.height and self.camRect.y + self.camRect.height < self.fieldRect.height:
            self.camRect.y += abs(speedy)

    def pitch(self):
        """Pitches the ball to the player."""
        if self.ballState != ballState.PITCHING:
            self.pitches += 1
            self.ballRect.x, self.ballRect.y = 740 - self.ballRect.width // 2, 1255 - self.ballRect.height // 2
            self.ballState = ballState.PITCHING
        else:
            self.ballRect.y += 5

        if self.ballRect.y >= 1580:
            self.ballState = ballState.NONE
            self.hasSwung = False

    def startBatAnim(self, screen, cam):
        """Starts the animation of the bat swing"""
        if self.batAnimIndex < len(self.batImgList) - 1:
            self.batAnimIndex += 1
            self.swing(screen, cam)
        else:
            self.batAnimIndex = 0
            self.isSwinging = False

    def swing(self, screen, cam):
        """Swings the bat."""
        if self.ballState == ballState.PITCHING and 1505 <= self.ballRect.y <= 1545:
            self.hasSwung = False
            if self.ballRect.y >= 1530:
                self.balldx = random.randint(3 - int((self.stats[1] // 33)), 8 - int((self.stats[1] // 12.4)))
            elif self.ballRect.y <= 1520:
                self.balldx = random.randint(-8 + int((self.stats[1] // 12.4)), -3 + int((self.stats[1] // 33)))
            else:
                self.balldx = random.randint(-2, 2)
            self.balldy = random.randint(1, 5) + self.stats[0] / 4
            self.ballHeight = random.randrange(1, 300)  # amount of frames that the ball will be in the air for
            self.landSpot = self.predictLanding()
            self.isFoul = self.checkFoul(self.landSpot)
            if self.isFoul:
                self.ballState = ballState.FOUL
            else:
                self.ballState = ballState.BALLHIT

    def checkFoul(self, point):
        """Checks if the ball landed in foul territory."""
        plateX = 742
        plateY = 1546

        # Left side foul
        if point[0] < plateX - 50:
            distY = plateY - point[1]
            if distY > 0:
                distX = plateX - point[0]
                if distX > distY * 0.8:
                    return True

        # Right side foul
        if point[0] > plateX + 50:
            distY = plateY - point[1]
            if distY > 0:
                distX = point[0] - plateX
                if distX > distY * 0.8:
                    return True

        return False

    def moveHitBall(self, event, screen):
        """Moves the ball after it has been hit."""
        self.ballRect.x += self.balldx
        self.ballRect.y -= self.balldy
        self.ballHeight -= 1

        if self.balldy > 0:
            self.balldy -= 0.15
        if self.balldx > 0:
            self.balldx -= 0.05
        if self.balldx < 0:
            self.balldx += 0.05

        if self.ballHeight <= 0:
            if self.ballState == ballState.FOUL:
                self.ballState = ballState.NONE
                self.isFoul = False
                self.showHitText = True
                self.hitTextTimer = 120
                self.lastHitDist = 0
            else:
                self.ballState = ballState.NONE
                self.lastHitDist = self.calcDist(self.landSpot)
                self.showHitText = True
                self.hitTextTimer = 120
            self.landSpot = None
            self.balldx = 0
            self.balldy = 0
            self.camRect.x = 340
            self.camRect.y = 1125

        if self.ballRect.y <= 0:
            self.camRect.x = 340
            self.camRect.y = 1125
            self.ballState = ballState.NONE

    def drawUI(self, screen):
        """Draws the UI on screen"""
        remaining = self.maxPitches - self.pitches
        if remaining < 0:
            remaining = 0
        pitchesText = self.font2.render(f"Pitches: {remaining}", True, (255, 255, 255))
        screen.blit(pitchesText, (10, 10))

        distText = self.font2.render(f"Total: {round(self.totDist)} ft", True, (255, 255, 255))
        screen.blit(distText, (10, 40))

        if self.showHitText and self.hitTextTimer > 0:
            self.hitTextTimer -= 1
            if self.lastHitDist > 0:
                hitText = self.font3.render(f"{round(self.lastHitDist)} ft", True, (255, 255, 0))
            else:
                hitText = self.font3.render("FOUL", True, (255, 0, 0))
            hitRect = hitText.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
            screen.blit(hitText, hitRect)
        else:
            self.showHitText = False

    def spinBall(self):
        """Spins the ball in the air"""
        if self.ballState == ballState.PITCHING:
            self.ballSpin = 80
        else:
            self.ballSpin = abs(self.balldx) * 5

        self.ballRot += self.ballSpin

    def predictLanding(self):
        """predicts where the ball lands"""
        x, y = self.ballRect.x, self.ballRect.y
        dx, dy = self.balldx, self.balldy
        height = self.ballHeight

        while height > 0 and y > 0:
            x += dx
            y -= dy
            height -= 1
            if dy > 0:
                dy -= 0.15
            if dx > 0:
                dx -= 0.05
            if dx < 0:
                dx += 0.05

        return x, y

    def calcDist(self, point):
        """calculates the distance of the ball from the plate, using 742,1546 pixels as the point of the center of the plate.
        converts the pixel distances to feet, using the rate of one pixel is 0.4 inches, then dividing by 12."""
        distX = 742 - abs(point[0])
        distY = 1546 - abs(point[1])
        distTot = math.hypot(distX, distY)
        distTot *= 2.5
        distTot = distTot / 12
        print(f"{distTot} ft")
        self.totDist += distTot * (1+self.stats[3])
        return distTot * (1+self.stats[3])

    def loadStatsSheet(self):
        with open("Data/playerStats.json", "r") as file:
            return json.load(file)

    def createFtSheet(self):
        with open("Data/playerFt.json", "w") as file:
            json.dump(self.totDist, file)

    def loadFtSheet(self):
        with open("Data/playerFt.json", "r") as file:
            return json.load(file)

    def gameEnd(self, event, screen):
        "finishes the game"
        if self.ballState != ballState.GAMEOVER:
            self.createFtSheet()
            self.ballState = ballState.GAMEOVER
        screen.fill((20, 20, 20))

        title = self.font1.render("GAME OVER", True, (255, 255, 255))
        title_rect = title.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 - 60))
        screen.blit(title, title_rect)

        dist = self.font2.render(f"Total Distance: {self.totDist:.0f} ft", True, (255, 255, 255))
        dist_rect = dist.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(dist, dist_rect)

        prompt = self.font2.render("Click anywhere to return to menu", True, (200, 200, 200))
        prompt_rect = prompt.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2 + 60))
        screen.blit(prompt, prompt_rect)

        if event != None and event.type == pygame.MOUSEBUTTONDOWN:
            self.pitches = 0
            self.ballState = ballState.NONE
            self.totDist = 0
            self.noPitch = False
            self.isFoul = False
            self.showHitText = False
            self.hitTextTimer = 0
            self.lastHitDist = 0
            self.exit = True