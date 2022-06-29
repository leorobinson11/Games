from scripts_s1.player_scripts.pointer import Pointer
from scripts_s0.btn import btn

import pygame
import os

class Starting_scene:
    def __init__(self,SCREENSIZE, SCREEN, won):
        self.SCREENSIZE = SCREENSIZE
        self.SCREEN = SCREEN
        self.running = True
        self.won = won

        self.pointer = Pointer()
        self.starting_btn = btn(lambda *args:True, 
                                os.path.join('images', 'btns','start_btn.png'),
                                (self.SCREENSIZE[0]/2,self.SCREENSIZE[1]/2-50),
                                250)
        if self.won != None:
            if self.won:
                self.message = pygame.image.load(os.path.join(os.path.join('images', 'btns','Win_message.png')))
            else:
                self.message = pygame.image.load(os.path.join(os.path.join('images', 'btns','Loss_message.png')))
            self.message = pygame.transform.scale(self.message,
                    (250,(250/self.message.get_width())*self.message.get_height())
                    )

    def DRAW(self):
        self.SCREEN.fill((0,0,0))
        self.starting_btn.DRAW(self.SCREEN)
        if self.won != None:
            self.SCREEN.blit(self.message, (self.SCREENSIZE[0]/2-120,self.SCREENSIZE[1]/2-150))
        self.pointer.DRAW(self.SCREEN)

    def MOVE(self):
        self.pointer.MOVE()

    def UPDATE(self):
        self.starting_btn.UPDATE()

    def ButtonFeedback(self):
        self.running = not self.starting_btn.pressed()

    def RUN(self):
        self.MOVE()
        self.DRAW()
        self.UPDATE()
        self.ButtonFeedback()