import pygame
import os

CWD = os.getcwd() # Get the current working directory
BIFD = CWD + "\\bankrollBust\\images\\buttons\\" # Button Images Folder Directory

class button:
    def __init__(self, surface, centre, buttonName):#
        self.bid = BIFD + buttonName
        self.centre = centre
        self.interactableImage = pygame.image.load(self.bid+".png")
        self.interactableObj = self.interactableImage.get_rect(center = centre)
        self.surface = surface
    
    def draw(self):
        self.surface.blit(self.interactableImage, self.interactableObj)
        
    def checkHover(self):
        mousePos = pygame.mouse.get_pos()
        return self.interactableObj.collidepoint(mousePos)

    def checkPressed(self):
        if pygame.mouse.get_pressed()[0]:
            return True
        
    def updateImage(self):
        pressed = False
        if self.checkHover(): # Check if the mouse is over the button
            if self.checkPressed(): # Button is Pressed
                self.interactableImage = pygame.image.load(self.bid+"_pressed"+".png")
                pressed = True
            else: # Buttons isn't pressed
                self.interactableImage = pygame.image.load(self.bid+"_hovered"+".png")
        else: # Button isn't being interacted with
            self.interactableImage = pygame.image.load(self.bid+".png")
        self.draw() # Draw the updated image
        return pressed
        
class discreteSlider(button):
    def __init__(self, surface: pygame.Surface, centre: tuple, values: list):
        self.surface = surface
        self.centre = centre
        self.values = values
        self.guideImage = pygame.image.load(BIFD + "sliderGuide.png")
        self.guideRect = self.guideImage.get_rect(center = centre)
        self.thumbLBound = self.guideRect.left
        self.thumbUBound = self.guideRect.right
        self.interactableImage = pygame.image.load(BIFD + "thumb.png")
        self.interactableObj = self.interactableImage.get_rect(center = (self.thumbLBound, self.guideRect.centery))
        self.pressed = False
        self.valuePoints = self.getValuePoints()
        
    def getValuePoints(self): # Figures out where a point should be on the slider
        xRange = self.thumbUBound - self.thumbLBound
        step = xRange // (len(self.values)-1) + (xRange%len(self.values))
        valuePoints = {}
        currentX = self.thumbLBound
        for i in range(len(self.values)):
            if i == 0:
                valuePoints[self.thumbLBound] = self.values[i]
            elif i == len(self.values) - 1:
                valuePoints[self.thumbUBound] = self.values[i]
            else:
                currentX += step
                valuePoints[currentX] = self.values[i]
        return valuePoints
    
    def snapThumb(self):
        xVals = list(self.valuePoints.keys())
        xCurrent = self.interactableObj.centerx
        upperBound, lowerBound = 0,0
        
        for i in range(len(xVals)-1): # Find where is the closest Point
            if xVals[i] <= xCurrent and xVals[i+1] >= xCurrent:
                lowerBound = xVals[i]
                upperBound = xVals[i+1]
                break
        if abs(xCurrent - lowerBound) <= abs(xCurrent - upperBound):
            return lowerBound
        else:
            return upperBound
                    

    def moveThumb(self):
        mousePos = pygame.mouse.get_pos()
        offsetX = 0
        if self.pressed == False:
            if self.checkHover():
                if self.checkPressed():
                    offsetX = mousePos[0] - self.interactableObj.centerx
                    self.pressed = True
        if self.pressed == True:
            if mousePos[0] > self.thumbLBound and mousePos[0] < self.thumbUBound:
                self.interactableObj.centerx = mousePos[0]-offsetX
            if not self.checkPressed():
                self.pressed = False
                snapPos = self.snapThumb()
                self.interactableObj.centerx = snapPos
        self.surface.blit(self.guideImage, self.guideRect)
        self.surface.blit(self.interactableImage, self.interactableObj)
        for i in list(self.valuePoints.keys()):
            pygame.draw.circle(self.surface, (0,255,0), (i,self.guideRect.centery), 5)
