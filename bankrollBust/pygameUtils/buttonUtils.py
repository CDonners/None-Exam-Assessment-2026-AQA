import pygame
import os

CWD = os.getcwd() # Get the current working directory
BIFD = CWD + "\\bankrollBust\\images\\buttons\\" # Button Images Folder Directory

class button:
    def __init__(self, surface, centre, buttonName):#
        self.bid = BIFD + buttonName
        self.centre = centre
        self.image = pygame.image.load(self.bid+".png")
        self.rect = self.image.get_rect(center = centre)
        self.surface = surface
        self.hovered = True
    
    def draw(self):
        self.surface.blit(self.image, self.rect)
        
    def checkHover(self, mousePos):
        self.hovered =  self.rect.collidepoint(mousePos)
        
    def updateImage(self):
        pressed = False
        mousePos = pygame.mouse.get_pos() # Gets the mouse position
        self.checkHover(mousePos)
        if self.hovered: # Check if the mouse is over the button
            if pygame.mouse.get_pressed()[0]: # Button is Pressed
                self.image = pygame.image.load(self.bid+"_pressed"+".png")
                pressed = True
            else: # Buttons isn't pressed
                self.image = pygame.image.load(self.bid+"_hovered"+".png")
        else: # Button isn't being interacted with
            self.image = pygame.image.load(self.bid+".png")
        self.draw() # Draw the updated image
        return pressed