import pygame
import os

class Lives_display:
    def __init__(self)->None:
        self.image_size = 30
        imagepath = os.path.join('images','sprites','playerextras','fuel.png')
        self.image = pygame.image.load(imagepath).convert_alpha()
        self.image = pygame.transform.scale(self.image,(self.image_size,self.image_size))
    
    def DRAW(self, SCREEN, fuel, screen_width)->None:
        fuel = int((fuel+120)/120) #one square represents 6 bullets
        #prints the fuel out evenly
        for i in range(fuel):    
            SCREEN.blit(self.image, (screen_width-45-(self.image_size+8)*i,35))