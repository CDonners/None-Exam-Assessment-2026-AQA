import pygame

fonts = pygame.sysfont.get_fonts()
emojis = [font for font in fonts if "emoji" in font]
print(emojis)