import pygame
from os import getcwd

CWD = getcwd() # Get the current working directory
BIFD = CWD + "\\bankrollBust\\images\\buttons\\" # Button Images Folder Directory

class button:
    def __init__(self, screen: pygame.Surface, centre: tuple, name: str, scale = 1.0, interactable = True):
        # Variables
        self.bid = BIFD + "button" # BID: Button Image Directory
        self.name = name
        self.centre = centre # Centre of the button
        self.screen = screen # Defining the screen
        self.scale = scale # Defining the scale
        self.interactable = interactable
        # Loading Images
        self.defaultImg = pygame.transform.scale_by(pygame.image.load(self.bid+".png"), self.scale)
        self.hoveredImg = pygame.transform.scale_by(pygame.image.load(self.bid+"_hovered"+".png"), self.scale)
        self.pressedImg = pygame.transform.scale_by(pygame.image.load(self.bid+"_pressed"+".png"),self.scale)
        self.inactiveImg = pygame.transform.scale_by(pygame.image.load(self.bid+"_inactive"+".png"),self.scale)
        # Creating button variables
        self.interactableImage = self.defaultImg
        self.interactableObj = self.interactableImage.get_rect(center = centre) # Turn the image into a rect with the specified centre
        # Create text object
        self.font = pygame.font.SysFont("", 36) # Sets the font to pygame default and sets the size
        self.titleSurface = self.font.render(f"{name}", True, (255, 255, 255)) # Creates the text screen, colour black
        self.titleRect = self.titleSurface.get_rect(center=centre) # Draws the text with the same centre as the button so it is over it
    
    def draw(self): # Blits the rect onto the screen
        self.updateImage() # Ensure image is updated
        self.screen.blit(self.interactableImage, self.interactableObj)
        self.screen.blit(self.titleSurface, self.titleRect)
        
    def checkHover(self): # Checks if the mouse is hovered over the rect
        mousePos = pygame.mouse.get_pos() # Gets the position of the mouse
        return self.interactableObj.collidepoint(mousePos) # Returns a boolean if the mouse pos overlaps the rect

    def pressed(self, event): # Checks if the mouse is pressed while it hovers over the button
        if self.interactable: # Don't allow button to be pressed if it isn't interactable
            if self.checkHover() and event.type == pygame.MOUSEBUTTONDOWN: # Checking if the button press is a mouse press
                if event.button == 1: # Checks if the button pressed is the left mouse button
                    self.interactableImage = self.pressedImg
                    return True
                else:
                    self.interactable = self.defaultImg
        return False
                
    def makeInteractable(self):
        self.interactable = True
    
    def makeUninteractable(self):
        self.interactable = False
        
    def updateImage(self): # Updates the image depending on how the button is being interacted with
        if self.interactable:
            self.interactableImage = self.defaultImg
            if self.checkHover():
                self.interactableImage = self.hoveredImg
        else:
            self.interactableImage = self.inactiveImg
        
class discreteSlider(button):
    def __init__(self, screen: pygame.Surface, name: str, centre: tuple, values: list, scale = 1.0, interactable = True):
        # Variables
        super().__init__(screen, centre, name, scale, interactable)
        self.values = values
        self.value = values[0] # Sets the default value to be the first one, which will be on the very left
        # Creating Slider Guide
        self.guideImage = pygame.transform.scale_by(pygame.image.load(BIFD + "sliderGuide.png"), self.scale)
        self.guideRect = self.guideImage.get_rect(center = centre)
        # Variables for slider thumb
        self.thumbLBound = self.guideRect.left
        self.thumbUBound = self.guideRect.right
        # Loading images for the thumb
        self.defaultImg = pygame.transform.scale_by(pygame.image.load(BIFD + "thumb.png"), self.scale)
        self.hoveredImg = pygame.transform.scale_by(pygame.image.load(BIFD + "thumbHovered.png"), self.scale)
        # Creating the rect objects for the slider
        self.interactableImage = self.defaultImg
        self.interactableObj = self.interactableImage.get_rect(center = (self.thumbLBound, self.guideRect.centery))
        # Variables for Logic
        self.mouseHeld = False # Mouse isn't held by default
        self.valuePoints = self.getValuePoints()
        
    def getValuePoints(self): # Figures out where a point should be on the slider
        xRange = self.thumbUBound - self.thumbLBound # Gets the range between the bounds
        step = xRange // (len(self.values)-1) + (xRange%len(self.values)) # Gets the step between nodes
        valuePoints = {} 
        currentX = self.thumbLBound # Initial position is the very left
        for i in range(len(self.values)): # Loops through all the values
            if i == 0: # if it's the first value
                valuePoints[self.thumbLBound] = self.values[i] # Automatically sets the left most node to the very left
            elif i == len(self.values) - 1: # If it's the last value
                valuePoints[self.thumbUBound] = self.values[i] # Automatically sets the right most node to be the very right
            else:
                currentX += step # Increments the current X value by the step
                valuePoints[currentX] = self.values[i] # Sets the current position to correspond to the value
        return valuePoints # Returns the dictionary with the X coordinate as the key and the value as the value e.g 100: 3 Players
    
    def snapThumb(self):
        xVals = list(self.valuePoints.keys()) # Gets a list of all the X coordinates of the node
        xCurrent = self.interactableObj.centerx # The current X is the X Coordinate of the thumb
        upperBound, lowerBound = 0,0 # Creating upperbound & lowerbound variables which will be the 2 nodes the thumb is between
        # Loop through all the X Coordinates of the nodes
        for i in range(len(xVals)-1): # Find where is the closest Point
            if xVals[i] <= xCurrent and xVals[i+1] >= xCurrent: # If it is between the 2 nodes
                lowerBound = xVals[i] # Lower bound is the node to the left
                upperBound = xVals[i+1] # Upper bound is the node to the right
                break # Breaks the loop to stop unneeded looping
        if abs(xCurrent - lowerBound) <= abs(xCurrent - upperBound): # Gets the absolute difference between the thumb and the nodes
            return lowerBound # If it's closer to the lowerbound
        else:
            return upperBound # If it's closer to the upper bound
                    
    def draw(self):
        # Draw thumb and guide
        self.screen.blit(self.guideImage, self.guideRect)
        self.screen.blit(self.interactableImage, self.interactableObj)
        # Create the text object
        font = pygame.font.SysFont("", 22) # Sets the font to default python font with size 22
        titleSurface = font.render(f"{self.name}: {self.value}", True, (255, 255, 255)) # Creates text screen with colour black
        titleRect = titleSurface.get_rect(center=(self.centre[0], self.centre[1]-15)) # Creates the rect with the offset to appear above the slider
        # Draw Text
        self.screen.blit(titleSurface, titleRect) # Draws on every iteration to update the value displayed
        # # For visibility of Nodes during testing
        # for i in list(self.valuePoints.keys()):
        #     pygame.draw.circle(self.screen, (0,255,0), (i,self.guideRect.centery), 5)

    def moveThumb(self, event):
        mousePos = pygame.mouse.get_pos() # Gets the position of the mouse
        offsetX = 0 # Create the offset variable
        if self.mouseHeld == False: # If the mouse isn't held
            if self.checkHover(): # Check if the mouse is hovering
                # If it is set the image of the thumb to the hovered image
                self.interactableImage = self.hoveredImg
                self.getHeld(event) # Checking if the mouse is pressed
                if self.mouseHeld: # If the mouse is held down
                    offsetX = mousePos[0] - self.interactableObj.centerx # Set the offset so the thumb doesn't snap to the mouse
            else:
                # Is the mouse isn't hovering, change the image to the default
                self.interactableImage = self.defaultImg
        if self.mouseHeld == True: # If the mouse is held down
            self.getHeld(event) # Check if the mouse is pressed
            if mousePos[0] > self.thumbLBound and mousePos[0] < self.thumbUBound: # Keep the sun within the bounds
                self.interactableObj.centerx = mousePos[0]-offsetX # Set the centre of the thumb to be the mouse position accounting for the offset
            if not self.mouseHeld: # If the mouse isn't held down
                snapPos = self.snapThumb() # get where the thumb should snap to
                self.interactableObj.centerx = snapPos # Snap the thumb to that pos
        
    def getValue(self, event):
        self.moveThumb(event) # Call the move thumb method
        closestValue = self.snapThumb() # get where the thumb is
        self.value = self.valuePoints[closestValue] # Set the current value to the value the thumb is over
        return self.value # Return the value
    
    def getHeld(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: # Checks if mouse button is pressed down
            if event.button == 1: # Checks if it's the left mouse button that is pressed
                self.mouseHeld = True # Sets to held 
        # Not using elif to account for single presses
        if event.type == pygame.MOUSEBUTTONUP: # Checks if mouse button is released
            if event.button == 1: # Checks if it's the left mouse button that is released
                self.mouseHeld = False # Sets held to false
                
class inputBox(button):
    def __init__(self, screen: pygame.Surface, centre: tuple, name: str, inputType: str , defaultValue:str, scale=1.0, interactable = True, minMax = []):
        # Variables
        super().__init__(screen, centre, name, scale, interactable)
        self.inputType = inputType # What input the box takes can be any from: ["alpha", "num", "alphanum"]
        self.defaultValue = defaultValue
        self.selected = False
        self.value = defaultValue # Setting to a default value
        self.minMax = minMax
        # Creating the text for the inputbox title
        self.title_font = pygame.font.SysFont("", 22) # Sets the font of the text to the default pygame font and the size to 22
        self.title_titleSurface = self.title_font.render(f"{self.name}", True, (255, 255, 255)) # Creates the text screen with black colour
        self.title_titleRect = self.title_titleSurface.get_rect(center=(self.centre[0], self.centre[1]-25*self.scale)) # Creates the rect with an offset to appear above the input box
    
    def draw(self):
        # Check if it's interactable
        if self.interactable:
            self.interactableImage = self.defaultImg
        else:
            self.interactableImage = self.inactiveImg
        # Button
        self.screen.blit(self.interactableImage, self.interactableObj)
        # Create the text object for value
        self.input_font = pygame.font.SysFont("", 22) # Sets the font to pygame default with size 22
        self.input_titleSurface = self.title_font.render(f"{self.value}", True, (255, 255, 255)) # Creates text screen with colour black
        self.input_titleRect = self.title_titleSurface.get_rect(center=self.centre) # Creates the rect of the text so the centre is over the box
        # Draw Text
        self.screen.blit(self.title_titleSurface, self.title_titleRect)
        self.screen.blit(self.input_titleSurface, self.input_titleRect)
    
    def checkSelected(self, event):
        if self.interactable: # Only do something if the box can be used
            if self.pressed(event): # Checks if the mouse was pressed
                if self.checkHover(): # Checks if the mouse was hovering over the box when it was pressed
                    self.selected = True # If it was then selected is true
                    self.value = "" # Value is blank
                else: 
                    self.selected = False # Selected is now false
                    if self.value == "": # If no value was set when it was pressed then the default value is set bac
                        self.value = self.defaultValue
                    elif self.minMax != (): # There is a minimum and maximum value meaning value is an int or float
                        if float(self.value) < self.minMax[0]:
                            self.value = str(self.minMax[0]) # If it's smaller than allowed set to min value
                        elif float(self.value) > self.minMax[1]:
                            self.value = str(self.minMax[1]) # If it's greater than allowed set to max value
                    
    def checkAllowed(self, strToCheck):
        # Checks if the input is accepted, returns boolean
        if self.inputType == "num":
            if strToCheck == "0" and self.value == "": # Checks to make sure the player isn't putting 0s before the number, makes display cleaner
                return False
            return strToCheck.isnumeric()
        elif self.inputType == "alpha":
            return strToCheck.isalpha()
        elif self.inputType == "alphanum":
            return strToCheck.isalnum()

    def setMax(self, maxBet):
        self.minMax[1] = maxBet

    def getInput(self, event):
        self.checkSelected(event) # Checks if the box was selected
        if self.selected: # if it was selected
            if event.type == pygame.KEYDOWN: # Checks for keyboard presses
                key_pressed = pygame.key.name(event.key) # Gets the key pressed
                if pygame.key.key_code(key_pressed) == 8: # Key Code 8 is backspace
                    if len(self.value) > 1: # Checks if string is longer than one
                        self.value = self.value[0:len(self.value)-1] # Removes the last character in the string
                    else: # If value is only one character or is empty, avoids implosion
                        self.value = "" # Sets value to 0
                elif self.checkAllowed(key_pressed): # Only accepts numeric inputs
                    self.value = self.value + key_pressed # Adds the input to the value string
        if self.inputType == "num":
            # Returns the value as a integer if it isn't empty
            return float(self.value) if self.value != "" else 0
        return self.value # returns the value string
    
class revealableButton(button):
    def __init__(self, screen: pygame.Surface, centre: tuple, name: str, scale = 1.0, interactable = True, revealed = False):
        super().__init__(screen, centre,  name, scale, interactable)
        self.interactableObj = pygame.Rect(0, 0, 170, 35)
        # Create text object
        self.font = pygame.font.SysFont("", 30) # Sets the font to pygame default and sets the size
        self.titleSurface = self.font.render(f"{name}", True, (255, 255, 255)) # Creates the text screen, colour black
        self.titleRect = self.titleSurface.get_rect(center=centre) # Draws the text with the same centre as the button so it is over it
        self.interactableObj.center = centre
        self.interactableObjColour = (110,49,6)
        self.revealed = revealed
        self.revealedText = None
        
    def draw(self):
        if self.checkHover(): # Sets the colour of the rect depending on whether it's hovered over
            self.interactableObjColour = (179,80,10)
        else:
            self.interactableObjColour = (110,49,6)
        if not self.revealed:
            # Draw the centre covering the text
            pygame.draw.rect(self.screen, self.interactableObjColour, self.interactableObj)
            self.screen.blit(self.titleSurface, self.titleRect)
        else:
            # Create the text object for the revlealed text
            revealedTextSurface = self.font.render(f"{self.revealedText}", True, "black")
            revealedText = revealedTextSurface.get_rect(center=self.centre)
            # Draw text on screen
            self.screen.blit(revealedTextSurface, revealedText)
        # Draw border
        pygame.draw.rect(self.screen, "black", self.interactableObj, 3)
        pygame.draw.rect(self.screen, (79,25,4), self.interactableObj, 2)
        
    def setRevealedText(self, info):
        self.revealedText = info
        