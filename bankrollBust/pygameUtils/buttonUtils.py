import pygame
import os

CWD = os.getcwd() # Get the current working directory
BIFD = CWD + "\\bankrollBust\\images\\buttons\\" # Button Images Folder Directory

class button:
    def __init__(self, surface, centre, buttonName):#
        self.bid = BIFD + buttonName + ".png"
        self.image = pygame.image.load(self.bid)
        self.rect = self.image.get_rect(center = centre)
        self.surface = surface
    
    def draw(self):
        self.surface.blit(self.image, self.rect)
        
