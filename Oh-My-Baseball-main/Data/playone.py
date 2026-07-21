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
from dataclasses import dataclass
from enum import IntEnum
from Data.Classes.Fielder import *


class ballState(IntEnum):
    PITCHING = 0
    BALLHIT = 1
    NONE = 3

@dataclass
class Game:
    #Class Variables
    fieldRect = pygame.Rect(-1,-1,0, 0)
    camRect = pygame.Rect(0,0,800, 480)
    ballRect = pygame.Rect(-1,-1,0, 0)
    fieldImage = None
    ballImg = None
    ballState = ballState.NONE
    balldx = 0
    balldy = 0
    ballRot = 0 #curremt rotation of the ball
    ballSpin = 0 #spin speed of the ball
    shadowImg = None
    batImgList = []
    batAnimIndex = 0 #current frame of the swing
    batRect = None
    isSwinging = False
    hasSwung = False
    fielders = []
    landSpot = None
    ballHeight = 0
    homerCount = 0



    def renderField(self, screen, width, height,event):
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
        screen.blit(self.batImgList[self.batAnimIndex], (self.batRect.x - self.camRect.x, self.batRect.y - self.camRect.y))
        if self.ballState == ballState.PITCHING:
            self.pitch()
            self.spinBall()
            rotatedBall = pygame.transform.rotate(self.ballImg, self.ballRot)
            rotatedRect = rotatedBall.get_rect(center=self.ballRect.center)

            screen.blit(rotatedBall, (rotatedRect.x - self.camRect.x, rotatedRect.y - self.camRect.y))
            self.camMove(self.ballRect, self.balldx, self.balldy)
            
        for f in self.fielders:
            f.update()

        if self.ballState == ballState.BALLHIT:
            self.moveHitBall()
            self.spinBall()

            scale = (300 + self.ballHeight) / 300
            ballTrans = pygame.transform.scale(self.ballImg, ( (self.ballImg.get_width() * scale), 
                                                              (self.ballImg.get_height() * scale)))
            rotatedBall = pygame.transform.rotate(ballTrans, self.ballRot)
            rotatedRect = rotatedBall.get_rect(center=self.ballRect.center)
            screen.blit(self.shadowImg, (self.ballRect.x - self.camRect.x, self.ballRect.y + self.ballHeight - self.camRect.y))
            screen.blit(rotatedBall, (rotatedRect.x - self.camRect.x, rotatedRect.y - self.camRect.y))
            self.camMove(self.ballRect, self.balldx, self.balldy)

    def setup(self, screen):
        for i in range(2):
            fielder = Fielder(i, screen, self.camRect)
            self.fielders.append(fielder)
        self.fieldImage = pygame.image.load("Data/Assets/sprites/field.png").convert()
        self.fieldRect = pygame.Rect(0, 0, self.fieldImage.get_width(), self.fieldImage.get_height())
        self.ballImg = pygame.image.load("Data/Assets/sprites/ball.png").convert_alpha()
        self.ballRect = pygame.Rect(0, 0, self.ballImg.get_width(), self.ballImg.get_height())
        self.shadowImg = pygame.image.load("Data/Assets/sprites/shadow.png").convert_alpha()
        self.batRect = pygame.Rect(690,1410, 100, 200)
        for i in range(28):
            bat = pygame.image.load(f'Data/Assets/sprites/bat_anim/bat-{i + 1}.png')
            self.batImgList.append(bat)
        self.camRect.x = 340
        self.camRect.y = 1125


    def camMove(self, objRect, speedx, speedy):
        """makes the camera follow an object"""
        boxRect = pygame.Rect(self.camRect.x + (self.camRect.width * 0.1), self.camRect.y + (self.camRect.height * 0.1), self.camRect.width * 0.8, self.camRect.height * 0.8)
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
            self.ballRect.x, self.ballRect.y = 740 - self.ballRect.width // 2, 1255 - self.ballRect.height // 2
            self.ballState = ballState.PITCHING
        else:
            self.ballRect.y += 5

        if self.ballRect.y >= 1580:
            self.ballState = ballState.NONE
            self.hasSwung = False

    def startBatAnim(self, screen, cam):
        """Starts the animation of the bat swing"""
        if self.batAnimIndex < len(self.batImgList) -1:
                self.batAnimIndex += 1
                self.swing(screen,cam)
        else:
            self.batAnimIndex = 0
            self.isSwinging = False
        
    def swing(self, screen,cam):
        """Swings the bat."""
        if self.ballState == ballState.PITCHING and 1530 <= self.ballRect.y <= 1570:
            self.hasSwung = False
            if self.ballRect.y >=1555:
                self.balldx = random.randint(3,8)
            elif self.ballRect.y <= 1545:
                self.balldx = random.randint(-8,-3)
            else:
                self.balldx = random.randint (-2,2)
            self.balldy = random.randint(5, 20)
            self.ballHeight = random.randrange(1, 300) #amount of frames that the ball will be in the air for
            self.landSpot = self.predictLanding()
            self.ballState = ballState.BALLHIT

    def moveHitBall(self):
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
            self.ballState = ballState.NONE
            self.calcDist(self.landSpot)
            self.landSpot = None
            self.balldx = 0
            self.balldy = 0
            self.camRect.x = 340
            self.camRect.y = 1125

        if self.ballRect.y <= 0:
            self.ballState = ballState.NONE
            self.camRect.x = 340
            self.camRect.y = 1125

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
        converts the pixel distances to feet, using the rate of one pixel is 0.4 inches, then dividing by 12"""
        distX =742 - abs(point[0])
        distY = 1546 - abs(point[1])
        distTot = math.hypot(distX, distY)
        distTot *= 2.5
        distTot = distTot / 12
        print(f"{distTot} ft")
        return distTot


    


    
    
        
