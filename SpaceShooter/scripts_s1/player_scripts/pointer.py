import pygame
import os

class Pointer:
    def __init__(self):
        #loading the image and setting up inital conditions
        imagepath = os.path.join('images','sprites','playerextras','pointer.png')
        self.image = pygame.image.load(imagepath).convert_alpha()
        self.image = pygame.transform.scale(self.image,(30,30))
        self.red_image = self.set_color(self.image,pygame.color.Color(255,0,0))
        self.rect = self.image.get_rect()
        self.rect.center = pygame.mouse.get_pos()
        pygame.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

    def set_color(self, orig_image, color):
        image = orig_image.copy()
        for x in range(image.get_width()):
            for y in range(image.get_height()):
                color.a = image.get_at((x,y)).a #alpha value
                image.set_at((x,y),color)
        return image

    def MOVE(self):
        #the pointer will follow the mouse
        self.rect.center = pygame.mouse.get_pos()
        
    def DRAW(self, SCREEN):
        #draws the image onto the screen/ in red if the mouse is pressed
        if any(pygame.mouse.get_pressed()):
            image = self.red_image
        else:
            image = self.image
        SCREEN.blit(image, self.rect)