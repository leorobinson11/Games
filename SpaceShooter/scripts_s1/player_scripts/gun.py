import pygame
import os
import math


class Gun:
    def __init__(self):
        imagepath = os.path.join('images','sprites','playerextras','gun.png')
        self.image = pygame.image.load(imagepath).convert_alpha()
        self.image = pygame.transform.scale(self.image,(150,(150/self.image.get_width())*self.image.get_height()))
        self.rect = self.image.get_rect()
        self.angle = 0
    
    def Rotate_center(self,angle):
        rotated_image = self.image.copy()
        if angle > 90 or angle < -90:
            rotated_image = pygame.transform.flip(rotated_image,False,True)
        #rotating the center
        rotated_image = pygame.transform.rotozoom(rotated_image,angle,1)
        #reajusting the center of the rotated image
        rotated_rect = rotated_image.get_rect(center = self.rect.center)
        return rotated_image, rotated_rect

    def MOVE(self,player_pos):
        #the center of the gun (visualy the left side) will follow the center of the player
        self.rect.center = player_pos

    def GETangle(self):
        #finding the angel between two points on a cartesian plane (the gun center and the mouse pointer)
        #the position of the two points:
        point1 = self.rect.center
        point2 = pygame.mouse.get_pos()
        #finding the lengths of the triangle
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        #math module function + converting it to degrees (-dy because pygame works in matrix coordinatess)
        return (math.atan2(-dy,dx)*180)/math.pi

    def DRAW(self, SCREEN)->None:
        #draws the image onto the screen
        #rotating the image to point towards the mouse
        self.angle = self.GETangle()
        rotated_image, rotated_rect = self.Rotate_center(self.angle)
        SCREEN.blit(rotated_image, rotated_rect)