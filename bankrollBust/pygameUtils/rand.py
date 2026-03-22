from os import urandom

def genRandInt(numberOfBits: int):
            # Ensure numberOfBits is greater than 0
            if numberOfBits < 0:
                raise ValueError("Error: Cannot have less than 0 bits")
            byteStringLen = (numberOfBits+7)//8 # Converts n into bytes rounding up
            byteString = urandom(byteStringLen) # Generates a random string of bytes from within the machine with specified length
            byteStringValue = int.from_bytes(byteString) # Converts byte string back to an integer
            integer = byteStringValue
            return integer
        
def genRandFloat(lowerBound: float, upperBound: float):
    upperBound = round(upperBound, 3) * 100
    lowerBound = round(lowerBound, 3) * 100
    integerGenerated = 0
    invalidGeneration = True
    if upperBound == lowerBound:
         integerGenerated = upperBound
    else:
        while invalidGeneration: # While it isn't between the bounds
            integerGenerated = genRandInt(8) # Regenerate integer
            if lowerBound < integerGenerated < upperBound:
                invalidGeneration = False
    generatedFloat = round(integerGenerated, 3) / 100
    return generatedFloat
    
def shuffleList(givenList):
    for _ in range(3): # Repeat shuffle 3 times to ensure proper shuffle
        for pos in range(len(givenList)-1,-1,-1):
            # Get the new position
            bitLength = pos.bit_length() # Gets how many bits is in the index
            newPos = genRandInt(bitLength) # Create Position
            while newPos >= len(givenList)-1: # If the position is out of range gen again
                newPos = genRandInt(bitLength) # Creates a new position
            givenList[pos], givenList[newPos] = givenList[newPos], givenList[pos] # Flips position values
    return givenList