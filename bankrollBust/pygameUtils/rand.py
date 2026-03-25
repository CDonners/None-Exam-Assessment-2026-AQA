from os import urandom

def genRandInt(numberOfBits: int):
    # Ensure numberOfBits is greater than 0
    if numberOfBits < 0:
        raise ValueError("Error: Cannot have less than 0 bits")
    byteStringLen = (numberOfBits+7)//8 # Converts n into bytes rounding up
    # Generate a random string of bytes from within the machine with specified length
    byteString = urandom(byteStringLen) 
    byteStringValue = int.from_bytes(byteString) # Converts byte string back to an integer
    integer = byteStringValue
    return integer
        
def genRandFloat(lowerBound: float, upperBound: float, decimalPlaces = 2):
    # --- Converting Floats to Int --- #
    tenthPower = 10**decimalPlaces
    upperBound = int(round(lowerBound*tenthPower, 0))
    lowerBound = int(round(lowerBound*tenthPower, 0))
    # --- Generate an Integer --- #
    integerGenerated = 0
    invalidGeneration = True
    if upperBound == lowerBound: # Edge case, cannot generate between 2 identical numbers
         integerGenerated = upperBound
    else:
        # Ensure generate integer is within bounds
        while invalidGeneration: # While it isn't between the bounds
            integerGenerated = genRandInt(upperBound.bit_length()) # Regenerate integer
            if lowerBound < integerGenerated < upperBound:
                invalidGeneration = False
    # Convert back to float of specified decimal places
    generatedFloat = integerGenerated / tenthPower
    return generatedFloat
    
def shuffleList(givenList):
    bitLength = len(givenList).bit_length() # Gets how many bits is in the length of the list
    for _ in range(3): # Repeat shuffle 3 times to ensure proper shuffle
        for pos in range(len(givenList)-1,-1,-1):
            # Get the new position
            newPos = genRandInt(bitLength) # Create Position
            while newPos >= len(givenList)-1: # If the position is out of range gen again
                newPos = genRandInt(bitLength) # Creates a new position
            givenList[pos], givenList[newPos] = givenList[newPos], givenList[pos] # Flips position values
    return givenList