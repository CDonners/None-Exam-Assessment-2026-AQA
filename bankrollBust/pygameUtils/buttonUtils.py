import pygame
import os

CWD = os.getcwd() # Get the current working directory
BIFD = CWD + "\\bankrollBust\\images\\buttons\\" # Button Images Folder Directory

class button:
    def __init__(self, surface, centre, buttonName):#
        self.bid = BIFD + buttonName
        self.centre = centre
        self.image = pygame.image.load(self.bid+".png")
        self.interactableObj = self.image.get_rect(center = centre)
        self.surface = surface
    
    def draw(self):
        self.surface.blit(self.image, self.rect)
        
    def checkHover(self, obj):
        mousePos = pygame.mouse.get_pos()
        return obj.collidepoint(mousePos)

    def checkPressed(self, obj):
        if pygame.mouse.get_perssed()[0]:
            return True
        
    def updateImage(self):
        pressed = False
        if self.checkHover(self.interactableObj): # Check if the mouse is over the button
            if self.checkPressed(interactableObj): # Button is Pressed
                self.image = pygame.image.load(self.bid+"_pressed"+".png")
                pressed = True
            else: # Buttons isn't pressed
                self.image = pygame.image.load(self.bid+"_hovered"+".png")
        else: # Button isn't being interacted with
            self.image = pygame.image.load(self.bid+".png")
        self.draw() # Draw the updated image
        return pressed
        
class discreteSlider():
    def __init__(self, surface, centre, values):
        self.surface = surface
        self.centre = centre
        self.values = values
        self.guideImage = pygame.image.load(BIFD + "sliderGuide")
        self.guideRect = self.guideImage.get_rect(center = centre)
        self.thumbBounds = (self.guideRect.left, self.guideRect.right)
        self.interactableObj = pygame.draw.circle(screen, (0, 0, 0), centre = (self.thumbBounds[0], (self.guideRect.top - self.guideRect.bottom)/2), 25)

    
