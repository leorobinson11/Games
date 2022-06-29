import random
from numpy import block

import pygame
import os

class Block(pygame.sprite.Sprite):
    def __init__(self,size,position):
        pygame.sprite.Sprite.__init__(self)
        imagepath = os.path.join('images','blocks','block.png')
        self.image = pygame.image.load(imagepath)
        self.image = pygame.transform.scale(self.image,size)

        self.starting_pos = position
        self.rect = self.image.get_rect(center=self.starting_pos)

    def update(self,x,y):
        #updating positions - (function gets passed into the pygame.sprite.Group update function)
        self.rect.centerx -= x
        self.rect.centery -= y
                
class ALLBlocks:
    def __init__(self, SCREENSIZE):
        self.SCREENSIZE = SCREENSIZE
        self.blocks = pygame.sprite.Group()
        maps = [self.build_map0, 
                self.build_map1,
                self.build_map2]
        #loading a random map
        maps[random.randint(0,len(maps)-1)]()

    def build_map0(self):
        self.blocks.add(Block((200,40),(self.SCREENSIZE[0]/2,self.SCREENSIZE[1]-700)))
        self.blocks.add(Block((200,40),(self.SCREENSIZE[0]/2,self.SCREENSIZE[1]-500)))
        self.blocks.add(Block((700,40),(self.SCREENSIZE[0]/2,self.SCREENSIZE[1]-200)))
        
    def build_map1(self):
        self.blocks.add(Block((300,40),(300,self.SCREENSIZE[1]/2+150)))
        self.blocks.add(Block((300,40),(self.SCREENSIZE[0]-300,self.SCREENSIZE[1]/2+150)))
        self.blocks.add(Block((300,40),(self.SCREENSIZE[0]/2,self.SCREENSIZE[1]-500)))

    def build_map2(self):
        self.blocks.add(Block((300,40),(300,self.SCREENSIZE[1]-500)))
        self.blocks.add(Block((300,40),(self.SCREENSIZE[0]-300,self.SCREENSIZE[1]-500)))
        self.blocks.add(Block((300,40),(self.SCREENSIZE[0]/2,self.SCREENSIZE[1]/2+150)))

    def DRAW(self, SCREEN):
        #self.blocks.draw(SCREEN)
        self.blocks.draw(SCREEN)