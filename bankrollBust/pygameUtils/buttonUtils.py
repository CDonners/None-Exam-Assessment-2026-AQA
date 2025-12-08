import pygame
import os

CWD = os.getcwd() # Get the current working directory
BIFD = CWD + "\\bankrollBust\\images\\buttons\\" # Button Images Folder Directory

class button:
    def __init__(self, surface: pygame.Surface, centre: tuple, name: str, scale = 1.0):
        # Variables
        self.bid = BIFD + "button" # BID: Button Image Directory
        self.centre = centre # Centre of the button
        self.surface = surface # Defining the surface
        self.scale = scale # Defining the scale
        # Creating the interactable button
        self.interactableImage = pygame.transform.scale_by(pygame.image.load(self.bid+".png"), scale) # Loading the image and adjusting it to the specified scale
        self.interactableObj = self.interactableImage.get_rect(center = centre) # Turn the image into a rect with the specified centre
        # Create text object
        self.font = pygame.font.SysFont("", 36)
        self.text_surface = self.font.render(f"{name}", True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=centre)
        
    
    def draw(self): # Blits the rect onto the surface
        self.surface.blit(self.interactableImage, self.interactableObj)
        self.surface.blit(self.text_surface, self.text_rect)
        
    def checkHover(self): # Checks if the mouse is hovered over the rect
        mousePos = pygame.mouse.get_pos()
        return self.interactableObj.collidepoint(mousePos)

    def checkPressed(self, event): # Checks if the mouse is pressed while it hovers over the button
        if event.type == pygame.MOUSEBUTTONDOWN: # Checking if the button press is a mouse press
            if event.button == 1: # Checks if the button pressed is the left mouse button
                return True
        
    def updateImage(self, event): # Updates the image depending on how the button is being interacted with
        pressed = False 
        if self.checkHover(): # Check if the mouse is over the button
            if self.checkPressed(event): # Button is Pressed
                self.interactableImage = pygame.transform.scale_by(pygame.image.load(self.bid+"_pressed"+".png"),self.scale)
                pressed = True
            else: # Buttons isn't pressed
                self.interactableImage = pygame.transform.scale_by(pygame.image.load(self.bid+"_hovered"+".png"), self.scale)
        else: # Button isn't being interacted with
            self.interactableImage = pygame.transform.scale_by(pygame.image.load(self.bid+".png"), self.scale)
        self.draw() # Draw the updated image
        return pressed
        
class discreteSlider(button):
    def __init__(self, surface: pygame.Surface, name: str, centre: tuple, values: list, scale = 1.0):
        # Variables
        self.surface = surface
        self.name = name
        self.centre = centre
        self.values = values
        self.scale = scale
        self.value = values[0]
        # Creating Slider Guide
        self.guideImage = pygame.transform.scale_by(pygame.image.load(BIFD + "sliderGuide.png"), self.scale)
        self.guideRect = self.guideImage.get_rect(center = centre)
        # Variables for slider thumb
        self.thumbLBound = self.guideRect.left
        self.thumbUBound = self.guideRect.right
        # Creating the rect objects for the slider
        self.interactableImage = pygame.transform.scale_by(pygame.image.load(BIFD + "thumb.png"), self.scale)
        self.interactableObj = self.interactableImage.get_rect(center = (self.thumbLBound, self.guideRect.centery))
        # Variables for Logic
        self.mouseHeld = False
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
                    
    def draw(self):
        # Draw thumb and guide
        self.surface.blit(self.guideImage, self.guideRect)
        self.surface.blit(self.interactableImage, self.interactableObj)
        # Create the text object
        font = pygame.font.SysFont("", 22)
        text_surface = font.render(f"{self.name}: {self.value}", True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(self.centre[0], self.centre[1]-15))
        # Draw Text
        self.surface.blit(text_surface, text_rect)
        # For visibility of Nodes during testing
        # for i in list(self.valuePoints.keys()):
        #     pygame.draw.circle(self.surface, (0,255,0), (i,self.guideRect.centery), 5)

    def moveThumb(self, event):
        mousePos = pygame.mouse.get_pos()
        offsetX = 0
        if self.mouseHeld == False:
            if self.checkHover():
                self.interactableImage = pygame.transform.scale_by(pygame.image.load(BIFD + "thumbHovered.png"), self.scale)
                self.checkPressed(event)
                if self.mouseHeld:
                    offsetX = mousePos[0] - self.interactableObj.centerx
            else:
                self.interactableImage = pygame.transform.scale_by(pygame.image.load(BIFD + "thumb.png"), self.scale)
        if self.mouseHeld == True:
            self.checkPressed(event)
            if mousePos[0] > self.thumbLBound and mousePos[0] < self.thumbUBound:
                self.interactableObj.centerx = mousePos[0]-offsetX
            if not self.mouseHeld:
                snapPos = self.snapThumb()
                self.interactableObj.centerx = snapPos
        
    def getValue(self, event):
        self.moveThumb(event)
        self.draw()
        closestValue = self.snapThumb()
        self.value = self.valuePoints[closestValue]
        return self.value
    
    def checkPressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouseHeld = True
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouseHeld = False
                
class inputBox(button):
    def __init__(self, surface: pygame.Surface, centre: tuple, name: str, inputType, scale=1.0):
        # Variables
        self.surface = surface
        self.centre = centre
        self.name = name
        self.inputType = inputType
        self.scale = scale
        self.selected = False
        self.value = "1000" # Setting to a default value
        # Creating the input box
        self.interactableImage = pygame.transform.scale_by(pygame.image.load(BIFD + "button.png"), self.scale)
        self.interactableObj = self.interactableImage.get_rect(center = centre)
        self.title_font = pygame.font.SysFont("", 22)
        self.title_text_surface = self.title_font.render(f"{self.name}", True, (255, 255, 255))
        self.title_text_rect = self.title_text_surface.get_rect(center=(self.centre[0], self.centre[1]-45))
        
    def pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                return True
        return False
    
    def draw(self):
        # Draw thumb and guide
        self.surface.blit(self.interactableImage, self.interactableObj)
        # Create the text object for value
        self.input_font = pygame.font.SysFont("", 22)
        self.input_text_surface = self.title_font.render(f"{self.value}", True, (255, 255, 255))
        self.input_text_rect = self.title_text_surface.get_rect(center=self.centre)
        # Draw Text
        self.surface.blit(self.title_text_surface, self.title_text_rect)
        self.surface.blit(self.input_text_surface, self.input_text_rect)
        ## For visibility of Nodes during testing
        # for i in list(self.valuePoints.keys()):
        #     pygame.draw.circle(self.surface, (0,255,0), (i,self.guideRect.centery), 5)
    
    def checkSelected(self, event):
        if self.pressed(event):
            if self.checkHover():
                self.selected = True
                self.value = ""
            else:
                self.selected = False
                if self.selected == "":
                    self.selected = "1000"
    
    def getInput(self, event):
        self.draw()
        self.checkSelected(event)
        if self.selected:
            if event.type == pygame.KEYDOWN:
                key_pressed = pygame.key.name(event.key)
                if key_pressed.isnumeric():
                    self.value = self.value + key_pressed
        return self.value            