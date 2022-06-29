from random import randint
import pygame
import os
import math


class Bullet(pygame.sprite.Sprite):
    def __init__(self,position, angle):
        pygame.sprite.Sprite.__init__(self)
        imagepath = os.path.join('images','sprites','playerextras','bullet.png')
        self.image = pygame.image.load(imagepath).convert_alpha()
        self.size = 15
        self.image = pygame.transform.scale(self.image,(self.size,self.size))
        self.rect = self.image.get_rect()
        self.image_record = self.image.copy()

        #kinematik paramaters
        self.rect.center = position
        self.angle = angle
        self.vel = 20
        
        #time the bullet was created
        self.born = pygame.time.get_ticks()
        self.shape_change = False

    def Colided(self,blocks):
        try:
            if pygame.sprite.spritecollide(self, blocks, False):
                #if the block already has colided (for bullets generated inside of blocks)
                if self.shape_change:
                    self.kill()
                #simulating them bouncing of walls
                self.vel *= -1
                self.angle = 180-self.angle
                #starting the countdown for being removed
                self.shape_change = True
                self.resize_start = pygame.time.get_ticks()
                self.resize_speed = -0.5
                self.resize_duration = 1000
        except:
            pass

    def Hit(self, enemies):
        try:
            if pygame.sprite.spritecollide(self, enemies, False):
                self.vel = 0
                self.shape_change = True
                self.resize_start = pygame.time.get_ticks()
                self.resize_speed = randint(10,17)/10
                self.resize_duration = 500
        except:
            pass

    def update(self, x_scroll,  y_scroll, blocks=0, enemies=0):
        if x_scroll or y_scroll:
            #moving in the opposite direction as the player
            self.rect.centerx -= x_scroll
            self.rect.centery -= y_scroll
        else:
            #checks colisions with blocks
            self.Colided(blocks)
            #checking colision with the enemie
            self.Hit(enemies)
            #if the sprite has been existed to long it gets removed from the group
            #(to same memory from off screen spritess)
            if pygame.time.get_ticks() - self.born > 1000:
                self.kill()
            else:
                radians = (self.angle*math.pi)/180
                #adding the x and y componants of the velocity to the position
                #and rescaling them acording to the angle
                self.rect.centerx += self.vel*math.cos(radians)
                self.rect.centery -= self.vel*math.sin(radians)

            if self.shape_change:
                #shrinking the bullet
                self.size += self.resize_speed
                if self.size > 60:
                    self.size *= -1
                try:
                    self.image = pygame.transform.scale(self.image_record,(self.size,self.size))
                    self.rect = self.image.get_rect(center=self.rect.center)
                    if pygame.time.get_ticks() - self.resize_start >= self.resize_duration:
                        self.kill()
                except:
                    self.kill()


class ALLBullets:
    def __init__(self)->None:
        self.collection = pygame.sprite.Group()
        self.delay = 200
        self.timer = pygame.time.get_ticks()

    def GETpositionOnCircle(self, center, angle):
        #finding the point given an angle (the gun angle), a center point (the player position) 
        #and a radius the 
        GUN_RADIUS = 80
        x, y = center
        #converting the angle to radians
        randians = (angle*math.pi)/180
        #obtaining x and y components
        bulletX = x + GUN_RADIUS*math.cos(-randians)
        bulletY = y + GUN_RADIUS*math.sin(-randians)
        return (bulletX,bulletY)
    
    def UPDATE(self, player, angle):
        #Adds bullets to with coresponding angles and positions
        if any(pygame.mouse.get_pressed()) and pygame.time.get_ticks() - self.timer > self.delay:
            #reseting the timer
            self.timer = pygame.time.get_ticks()
            #calculating the position of the bullet
            starting_point = self.GETpositionOnCircle(player.rect.center, angle)
            #adding a bullet to the pygame sprite Group object
            new_bullet = Bullet(starting_point, angle)
            self.collection.add(new_bullet)
            
    def MOVE(self, x_scroll=False,  y_scroll=False, blocks=0, enemies=0):
        self.collection.update(x_scroll,  y_scroll, blocks, enemies)

    def DRAW(self, SCREEN):
        self.collection.draw(SCREEN)
