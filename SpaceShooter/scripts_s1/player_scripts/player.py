import pygame
import os


class Player:
    def __init__(self, SCREENSIZE):
        #setting the rect and image
        self.animations = self.GETimages()
        self.image = self.animations[0]
        self.rect = self.image.get_rect()

        #setting the starting position
        self.rect.center = (SCREENSIZE[0]/2,SCREENSIZE[1]/2)

        #movement paramaters (velocity, acceleration, terminal velocity)
        self.x_vel = 0 #x velocity
        self.x_acc = 0.4 #x acceleration
        self.x_term = 12 #x terminal velocity
        self.l_right = True #the direction the character is looking in
        self.y_vel = 0 #y velocity
        self.y_acc = 0.4 #y acceleration
        self.y_term = 12 #y terminal velocity
        self.mj = 40 #max jumpheit
        self.jc = self.mj #jump counter - to keep track of the jump left
        self.f_term = 14 #terminal valing velocit

        #boundaries for the player movement
        self.x_lower = 200
        self.x_upper = SCREENSIZE[0]-200

        self.y_lower = 150
        self.y_upper = SCREENSIZE[1]-400

        self.lives = 3
        self.last_death = pygame.time.get_ticks()
        self.y_scroll_rec = 0

    def GETimages(self):
        #obtaining all images for the player as a list
        path = os.path.join('images','sprites','player')
        images = []
        for file in os.listdir(path):
            newimage = pygame.image.load(os.path.join(path,file)).convert_alpha()
            #addapting the image size without changing the w/h ratio
            newimage = pygame.transform.scale(newimage,
                (30,(30/newimage.get_width())*newimage.get_height())
                )
            images.append(newimage)
        return images

    def BlockColision(self, x_vel, y_vel, blocks):
        #solid colisions work by direction and setting the side of the player to the opisite side of the blockssssss
        for p in pygame.sprite.spritecollide(self, blocks, False):
            if x_vel > 0:
                self.rect.right = p.rect.left
            if x_vel < 0:
                self.rect.left = p.rect.right
            if y_vel > 0:
                #simulating bounse on the first collision of each jump
                if y_vel > 0.8:
                    self.rect.bottom = p.rect.top
                    self.y_vel = - round(self.y_vel/5)
                else:
                    self.rect.bottom = p.rect.top
                    self.y_vel = 0
                self.jc = self.mj
            if y_vel < 0:
                self.rect.top = p.rect.bottom
                self.y_vel = 0

    
    def MOVE(self, scrolling_sprites):
        keystate = pygame.key.get_pressed()
        #moving left
        if keystate[pygame.K_a]:
            #accelerating until terminal velocity
            self.x_vel = self.x_vel - self.x_acc if self.x_vel >= -self.x_term else self.x_vel
            if self.l_right:
                #flipping the image so that the character looks the right way
                self.animations = [pygame.transform.flip(animation,True,False) for animation in self.animations]
                self.l_right = False
        elif self.x_vel < 0 and not keystate[pygame.K_d]:
            #decelerating
                self.x_vel += self.x_acc/2

        #moving right
        if keystate[pygame.K_d]:
            #accelerating until terminal velocity
            self.x_vel = self.x_vel + self.x_acc if self.x_vel <= self.x_term else self.x_vel
            if not self.l_right:
                #flipping the image so that the character looks the right way
                self.animations = [pygame.transform.flip(animation,True,False) for animation in self.animations]
                self.l_right = True
        elif self.x_vel > 0 and not keystate[pygame.K_a]:
            #decelerating
            self.x_vel -= self.x_acc/2

        if keystate[pygame.K_w] and self.jc > 0:
            #jumpin
            self.image = self.animations[1]
            self.y_vel = self.y_vel - self.y_acc if self.y_vel >= -self.y_term else self.y_vel
            self.jc -= 1
        else:
            #falling on key release or when the max jumheit has been released
            self.image = self.animations[0]
            self.jc = 0
            self.y_vel = self.y_vel + self.y_acc if self.y_vel <= self.f_term else self.y_vel
        
        self.x_vel = round(self.x_vel,1)
        self.y_vel = round(self.y_vel,1)

        if self.x_vel < 0 and self.x_vel > -0.1 and not keystate[pygame.K_a]:
            self.x_vel = 0
        if self.x_vel > 0 and self.x_vel < 0.1 and not keystate[pygame.K_d]:
            self.x_vel = 0

        self.rect.x += self.x_vel
        #handling colisions with blocks - x direction
        self.BlockColision(self.x_vel,0,scrolling_sprites[0])
        self.rect.y += self.y_vel
        #handling colisions with blocks - y direction
        self.BlockColision(0,self.y_vel,scrolling_sprites[0])

        #scrolling for when the player reaches the screen edge limit (for vertical and horizontal)
        if self.rect.x >= self.x_upper:
            scroll = self.rect.x - self.x_upper
            self.rect.x -= scroll
            for spritegroup in scrolling_sprites:
                spritegroup.update(scroll, 0)

        if self.rect.x <= self.x_lower:
            scroll = self.rect.x - self.x_lower
            self.rect.x -= scroll
            for spritegroup in scrolling_sprites:
                spritegroup.update(scroll, 0)

        if self.rect.y <= self.y_lower:
            scroll = self.rect.y - self.y_lower
            self.rect.y -= scroll
            self.y_scroll_rec += scroll
            for spritegroup in scrolling_sprites:
                spritegroup.update(0, scroll)

        if self.rect.y >= self.y_upper:
            scroll = self.rect.y - self.y_upper
            self.rect.y -= scroll
            self.y_scroll_rec += scroll
            for spritegroup in scrolling_sprites:
                spritegroup.update(0, scroll)

    def UPDATE(self, enemies):
        #checking for falling
        if self.y_scroll_rec >= 2500:
            self.lives = 0
        #checking for colision with the enemie
        if pygame.time.get_ticks() - self.last_death > 500:
            if pygame.sprite.spritecollide(self, enemies, False):
                self.lives -= 1
                self.last_death = pygame.time.get_ticks()
            return (0,0,0)
        else:
            #the colour of the background if the enemy has just been hit
            return (88, 11, 11)
        
    def DRAW(self, SCREEN):
        #draws the image onto the screen
        SCREEN.blit(self.image, self.rect)