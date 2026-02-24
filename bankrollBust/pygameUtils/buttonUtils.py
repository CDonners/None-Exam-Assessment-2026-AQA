import pygame
import os

CWD = os.getcwd() # Get the current working directory
BIFD = CWD + "\\bankrollBust\\images\\buttons\\" # Button Images Folder Directory

class button:
    def __init__(self, surface: pygame.Surface, centre: tuple, name: str, scale = 1.0, interactable = True):
        # Variables
        self.bid = BIFD + "button" # BID: Button Image Directory
        self.centre = centre # Centre of the button
        self.surface = surface # Defining the surface
        self.scale = scale # Defining the scale
        self.interactable = interactable
        # Creating the interactable button
        self.interactableImage = pygame.transform.scale_by(pygame.image.load(self.bid+".png"), scale) # Loading the image and adjusting it to the specified scale
        self.interactableObj = self.interactableImage.get_rect(center = centre) # Turn the image into a rect with the specified centre
        # Create text object
        self.font = pygame.font.SysFont("", 36) # Sets the font to pygame default and sets the size
        self.text_surface = self.font.render(f"{name}", True, (255, 255, 255)) # Creates the text surface, colour black
        self.text_rect = self.text_surface.get_rect(center=centre) # Draws the text with the same centre as the button so it is over it
        
    
    def draw(self): # Blits the rect onto the surface
        self.surface.blit(self.interactableImage, self.interactableObj)
        self.surface.blit(self.text_surface, self.text_rect)
        
    def checkHover(self): # Checks if the mouse is hovered over the rect
        mousePos = pygame.mouse.get_pos() # Gets the position of the mouse
        return self.interactableObj.collidepoint(mousePos) # Returns a boolean if the mouse pos overlaps the rect

    def pressed(self, event): # Checks if the mouse is pressed while it hovers over the button
        if event.type == pygame.MOUSEBUTTONDOWN: # Checking if the button press is a mouse press
            if event.button == 1: # Checks if the button pressed is the left mouse button
                return True
            
    def makeInteractable(self):
        self.interactable = True
    
    def makeUninteractable(self):
        self.interactable = False
        
    def updateImage(self, event): # Updates the image depending on how the button is being interacted with
        pressed = False # Button isn't pressed by default
        if self.interactable: # Button can be interacted with
            if self.checkHover(): # Check if the mouse is over the button
                if self.pressed(event): # Button is Pressed
                    # Set the button to the pressed image
                    self.interactableImage = pygame.transform.scale_by(pygame.image.load(self.bid+"_pressed"+".png"),self.scale)
                    pressed = True # Telling us the button is pressed
                else: # Buttons isn't pressed6
                    # Set button to the hovered image
                    self.interactableImage = pygame.transform.scale_by(pygame.image.load(self.bid+"_hovered"+".png"), self.scale)
            else: # Button isn't being interacted with
                # Set the button image to the regular image as it's not being interacted with
                self.interactableImage = pygame.transform.scale_by(pygame.image.load(self.bid+".png"), self.scale)
        else:
            self.interactableImage = pygame.transform.scale_by(pygame.image.load(self.bid+"_inactive"+".png"),self.scale)
        self.draw() # Draw the updated image
        return pressed # Returns whether button is pressed
        
class discreteSlider(button):
    def __init__(self, surface: pygame.Surface, name: str, centre: tuple, values: list, scale = 1.0, interactable = True):
        # Variables
        self.surface = surface
        self.name = name
        self.centre = centre
        self.values = values
        self.scale = scale
        self.interactable = interactable
        self.value = values[0] # Sets the default value to be the first one, which will be on the very left
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
        self.surface.blit(self.guideImage, self.guideRect)
        self.surface.blit(self.interactableImage, self.interactableObj)
        # Create the text object
        font = pygame.font.SysFont("", 22) # Sets the font to default python font with size 22
        text_surface = font.render(f"{self.name}: {self.value}", True, (255, 255, 255)) # Creates text surface with colour black
        text_rect = text_surface.get_rect(center=(self.centre[0], self.centre[1]-15)) # Creates the rect with the offset to appear above the slider
        # Draw Text
        self.surface.blit(text_surface, text_rect) # Draws on every iteration to update the value displayed
        # # For visibility of Nodes during testing
        # for i in list(self.valuePoints.keys()):
        #     pygame.draw.circle(self.surface, (0,255,0), (i,self.guideRect.centery), 5)

    def moveThumb(self, event):
        mousePos = pygame.mouse.get_pos() # Gets the position of the mouse
        offsetX = 0 # Create the offset variable
        if self.mouseHeld == False: # If the mouse isn't held
            if self.checkHover(): # Check if the mouse is hovering
                # If it is set the image of the thumb to the hovered image
                self.interactableImage = pygame.transform.scale_by(pygame.image.load(BIFD + "thumbHovered.png"), self.scale)
                self.pressed(event) # Checking if the mouse is pressed
                if self.mouseHeld: # If the mouse is held down
                    offsetX = mousePos[0] - self.interactableObj.centerx # Set the offset so the thumb doesn't snap to the mouse
            else:
                # Is the mouse isn't hovering, change the image to the default
                self.interactableImage = pygame.transform.scale_by(pygame.image.load(BIFD + "thumb.png"), self.scale) 
        if self.mouseHeld == True: # If the mouse is held down
            self.pressed(event) # Check if the mouse is pressed
            if mousePos[0] > self.thumbLBound and mousePos[0] < self.thumbUBound: # Keep the sun within the bounds
                self.interactableObj.centerx = mousePos[0]-offsetX # Set the centre of the thumb to be the mouse position accounting for the offset
            if not self.mouseHeld: # If the mouse isn't held down
                snapPos = self.snapThumb() # get where the thumb should snap to
                self.interactableObj.centerx = snapPos # Snap the thumb to that pos
        
    def getValue(self, event):
        self.moveThumb(event) # Call the move thumb method
        self.draw() # Draw the images
        closestValue = self.snapThumb() # get where the thumb is
        self.value = self.valuePoints[closestValue] # Set the current value to the value the thumb is over
        return self.value # Return the value
    
    def pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN: # Checks if mouse button is pressed down
            if event.button == 1: # Checks if it's the left mouse button that is pressed
                self.mouseHeld = True # Sets to held 
        # Not using elif to account for single presses
        if event.type == pygame.MOUSEBUTTONUP: # Checks if mouse button is released
            if event.button == 1: # Checks if it's the left mouse button that is released
                self.mouseHeld = False # Sets held to false
                
class inputBox(button):
    def __init__(self, surface: pygame.Surface, centre: tuple, name: str, inputType: str , defaultValue:str, scale=1.0, interactable = True, minMax = []):
        # Variables
        self.surface = surface
        self.centre = centre
        self.name = name
        self.inputType = inputType # What input the box takes can be any from: ["alpha", "num", "alphanum"]
        self.defaultValue = defaultValue
        self.scale = scale
        self.interactable = interactable
        self.selected = False
        self.value = defaultValue # Setting to a default value
        self.minMax = minMax
        # Creating the input box
        self.interactableImage = pygame.transform.scale_by(pygame.image.load(BIFD + "button.png"), self.scale)
        self.interactableObj = self.interactableImage.get_rect(center = centre)
        # Creating the text for the slider title
        self.title_font = pygame.font.SysFont("", 22) # Sets the font of the text to the default pygame font and the size to 22
        self.title_text_surface = self.title_font.render(f"{self.name}", True, (255, 255, 255)) # Creates the text surface with black colour
        self.title_text_rect = self.title_text_surface.get_rect(center=(self.centre[0], self.centre[1]-50*self.scale)) # Creates the rect with an offset to appear above the input box
    
    def draw(self):
        # Check if it's interactable
        if self.interactable:
            self.interactableImage = pygame.transform.scale_by(pygame.image.load(BIFD + "button.png"), self.scale)
        else:
            self.interactableImage = pygame.transform.scale_by(pygame.image.load(BIFD + "button_inactive.png"), self.scale)
        # Button
        self.surface.blit(self.interactableImage, self.interactableObj)
        # Create the text object for value
        self.input_font = pygame.font.SysFont("", 22) # Sets the font to pygame default with size 22
        self.input_text_surface = self.title_font.render(f"{self.value}", True, (255, 255, 255)) # Creates text surface with colour black
        self.input_text_rect = self.title_text_surface.get_rect(center=self.centre) # Creates the rect of the text so the centre is over the box
        # Draw Text
        self.surface.blit(self.title_text_surface, self.title_text_rect)
        self.surface.blit(self.input_text_surface, self.input_text_rect)
    
    def checkSelected(self, event):
        if self.interactable: # Only do something if the box can be used
            if self.pressed(event): # Checks if the mouse was pressed
                if self.checkHover(): # Checks if the mouse was hovering over the box when it was pressed
                    self.selected = True # If it was then selected is true
                    self.value = "" # Value is blank
                else: # Otherwise
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
        self.draw() # Draws the rects
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
            return int(self.value) # Returns the value as a integer
        return self.value # returns the value string