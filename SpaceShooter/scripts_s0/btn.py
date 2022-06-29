import pygame
import time

class btn:
    def __init__(self, function, image_path, position, size):
        #a function that gets exicutet when the button is pressed
        self.function = function
        self.size = size
        self.orig_size = self.size
        self.position = position

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image,
                (self.size,(self.size/self.image.get_width())*self.image.get_height())
                )
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=self.position)
        self.fill = (0,0,0)

    def hovering(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_x, mouse_y):
            self.fill = (38,50,56)
            self.size = self.orig_size + 10
            self.is_hovering = True
        else:
            self.fill = (0,0,0)
            self.size = self.orig_size
            self.is_hovering = False

    def pressed(self, *args):
        if self.is_hovering and any(pygame.mouse.get_pressed()):
            time.sleep(0.1)
            return self.function(args)
        else: 
            return False

    def UPDATE(self):
        self.hovering()

    def DRAW(self, SCREEN):
        if self.image.get_width() != self.size:
            self.image = pygame.transform.scale(self.orig_image,
                (self.size,(self.size/self.image.get_width())*self.image.get_height())
                )
            self.rect = self.image.get_rect(center=self.position)
        pygame.draw.rect(SCREEN, self.fill, (self.rect.x, self.rect.y, self.image.get_width(), self.image.get_height()))
        SCREEN.blit(self.image, self.rect)
    
   