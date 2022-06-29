import imp
from scripts_s1.player_scripts.pointer import Pointer
from scripts_s1.player_scripts.player import Player
from scripts_s1.player_scripts.gun import Gun
from scripts_s1.player_scripts.bullets import ALLBullets
from scripts_s1.player_scripts.livesdisplay import Lives_display
from scripts_s1.block_scripts.block import ALLBlocks
from scripts_s1.enemie_scripts.e1 import All_E1

import time

class Playing_scene:
    def __init__(self,SCREENSIZE, SCREEN):
        self.SCREENSIZE = SCREENSIZE
        self.SCREEN = SCREEN
        self.running = True

        #all the sprites - Playerrelated
        #single sprites:
        self.player = Player(self.SCREENSIZE)
        self.gun = Gun()
        self.pointer = Pointer()
        self.disp = Lives_display()

        #platfrom sprite groups
        self.allbullets = ALLBullets()
        self.allblocks = ALLBlocks(SCREENSIZE)

        #enemie sprite groups
        self.enemies_1 = All_E1()

        #background color
        self.back_ground = (0,0,0)
    
    def DRAW(self):
        #draws everything onto the screen
        self.SCREEN.fill(self.back_ground)
        #environment:
        self.allblocks.DRAW(self.SCREEN)
        #player related:
        self.gun.DRAW(self.SCREEN)
        self.player.DRAW(self.SCREEN)
        self.allbullets.DRAW(self.SCREEN)
        #enemies
        self.enemies_1.DRAW(self.SCREEN)
        #stats:
        if len(self.enemies_1.enemies_bodies) > 0:
            self.disp.DRAW(self.SCREEN,
                           [enemy.lives for enemy in self.enemies_1.enemies_bodies][0],
                           self.SCREENSIZE[0])
        self.pointer.DRAW(self.SCREEN)

    def MOVE(self):
        #updates all the movement
        #all the sprites that scroll are requires in the player move function 
        #(with the blocks in the first place)
        self.player.MOVE([
            self.allblocks.blocks, 
            self.enemies_1.enemies_bodies,
            self.allbullets.collection
        ]) 
        self.gun.MOVE(self.player.rect.center)
        self.pointer.MOVE()
        self.allbullets.MOVE(blocks=self.allblocks.blocks, enemies=self.enemies_1.enemies_bodies)
        #enemies
        self.enemies_1.MOVE(self.player.rect.center, self.allbullets.collection)

    def UPDATE(self):
        #updates all non moving events
        self.back_ground = self.player.UPDATE(self.enemies_1.enemies_bodies)
        self.allbullets.UPDATE(self.player,self.gun.angle)

    def RUN(self):
        #exicutes all the screens functions
        self.MOVE()
        self.DRAW()
        self.UPDATE()

        #ending the game
        if len(self.enemies_1.enemies_bodies)<= 0:
            self.running = False
            time.sleep(0.1)
            return True
        elif self.player.lives <= 0:
            self.running = False
            time.sleep(0.1)
            return False