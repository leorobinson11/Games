from random import randint
from matplotlib import image
import pygame
import os
import math


class Enemy1(pygame.sprite.Sprite):
    def __init__(self, pos, imagepath, wing_imagepth):
        pygame.sprite.Sprite.__init__(self)
        self.pos = pos
        self.image = pygame.image.load(imagepath).convert_alpha()
        self.image = pygame.transform.scale(self.image,(70,70))
        self.rect = self.image.get_rect(center=self.pos)

        self.angle = 0
        self.attacking = False
        self.time_since_attack = pygame.time.get_ticks()

        #movement paramaters
        self.vel = 4
        self.acc = 0.2
        self.term = 12

        self.cool_down = randint(1200, 2000)
        self.attack_duration = randint(600,1000)

        #wings
        self.wings = pygame.image.load(wing_imagepth).convert_alpha()
        self.wings = pygame.transform.scale(self.wings,(220,252))
        self.wingsrect = self.wings.get_rect(center=self.rect.center)
        self.wings_angle = randint(0,90)
        
        self.lives = 1000
    
    def Rotate_center(self,image,angle):
        rotated_image = image.copy()
        if angle > 90 or angle < -90:
            rotated_image = pygame.transform.flip(rotated_image,False,True)
        #rotating the center
        rotated_image = pygame.transform.rotozoom(rotated_image,angle,1)
        #reajusting the center of the rotated image
        rotated_rect = rotated_image.get_rect(center = self.rect.center)
        return rotated_image, rotated_rect

    def GETangle(self, player_pos):
        #finding the angel between two points on a cartesian plane (the gun center and the mouse pointer)
        #the position of the two points:
        point1 = self.rect.center
        point2 = player_pos
        #finding the lengths of the triangle
        dx = point2[0] - point1[0]
        dy = point2[1] - point1[1]
        #math module function + converting it to degrees (-dy because pygame works in matrix coordinatess)
        return (math.atan2(-dy,dx)*180)/math.pi

    def Start_attack(self, player_pos):
        #adjust the angle to face the player
        self.angle = self.GETangle(player_pos)
        if not self.attacking:
            #if its been long enougth since the attack
            if pygame.time.get_ticks() - self.time_since_attack > self.cool_down:
                self.attacking = True
                self.attack_angle = self.angle
                #starting the timer for the attack
                self.attack_starting_time = pygame.time.get_ticks()
                self.attack_duration = randint(600,1000)

    def Attack(self):
        if self.attacking:
            time = pygame.time.get_ticks() - self.attack_starting_time
            if time > self.attack_duration:
                #ending the attack
                self.attacking = False

                #setting up the countdown until the next attack
                self.time_since_attack = pygame.time.get_ticks()
                self.cool_down = randint(1200, 2000)
            else:
                #accelerating
                if time < self.attack_duration*0.75:
                    if self.vel < self.term:
                        self.vel += self.acc
                else:
                    #decelerating
                    self.vel -= self.acc
                #moving the character towards the player
                radians = (self.attack_angle*math.pi)/180
                #adding the x and y componants of the velocity to the position
                #and rescaling them acording to the angle
                self.rect.centerx += self.vel*math.cos(radians)
                self.rect.centery -= self.vel*math.sin(radians)
            self.wings_angle += 3

    def draw(self, SCREEN):
        #rotating the main body image to face the
        rotated_image, rotated_rect = self.Rotate_center(self.image, self.angle)
        SCREEN.blit(rotated_image, rotated_rect)
        
        #drawing the wings on to the screen
        rotated_image, rotated_rect = self.Rotate_center(self.wings, self.wings_angle)
        SCREEN.blit(rotated_image, rotated_rect)

    def IS_HIT(self, bullets):
        if pygame.sprite.spritecollide(self, bullets, False):
            if self.lives <= 1:
                self.kill()
            else:   
                self.lives -= 1
        
    def update(self, x_scroll=0,  y_scroll=0, player_pos=0, bullets=0):
        #the scroll from the player movement - if the function is called from the player
        if x_scroll or y_scroll:
            self.rect.centerx -= x_scroll
            self.rect.centery -= y_scroll
        #if the function is called from the main code
        elif player_pos: 
            self.Start_attack(player_pos)
            self.Attack()
            self.IS_HIT(bullets)


"""
class Enemy2(Enemy1):
    def __init__(self, pos, imagepath, wing_imagepath):
        super().__init__(pos, imagepath, wing_imagepath)

    def draw(self, SCREEN):
        #rotating the main body image to face the
        rotated_image, rotated_rect = self.Rotate_center(self.image, self.angle - 90)
        SCREEN.blit(rotated_image, rotated_rect)
        
        #drawing the wings on to the screen
        rotated_image, rotated_rect = self.Rotate_center(self.wings, self.wings_angle)
        SCREEN.blit(rotated_image, rotated_rect)
"""
    

class All_E1:
    def __init__(self):
        self.enemies_bodies = pygame.sprite.Group()
        self.build_map()

    def build_map(self):
        #all the enemies
        self.enemies_bodies.add(Enemy1((randint(0,1000),randint(0,1000)), 
                                        os.path.join('images','sprites','enemies','e1','main_body.png'),
                                        os.path.join('images','sprites','enemies','e1','wings.png')))
        #self.enemies_bodies.add(Enemy2((randint(0,1000),randint(0,1000)), 
        #                                os.path.join('images','sprites','enemies','e1','main_body2.png'),
        #                                os.path.join('images','sprites','enemies','e1','wings2.png')))
    
    def DRAW(self, SCREEN):
        for enemie in self.enemies_bodies:
            enemie.draw(SCREEN)

    def MOVE(self, player_pos, bullets):
        self.enemies_bodies.update(player_pos=player_pos, bullets=bullets)

