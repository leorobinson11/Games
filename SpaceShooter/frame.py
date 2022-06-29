from scene_starting import Starting_scene
from scene_playing import Playing_scene
import pygame
import os


class Frame:
    def __init__(self):
        #loading functions from the pygame module
        pygame.init()
        #setting up the screen tick rate
        self.FPS = 50
        self.CLOCK = pygame.time.Clock()
        #setting the screen to be the screen size
        infoObject = pygame.display.Info()
        self.SCREENSIZE = infoObject.current_w, infoObject.current_h
        self.SCREEN = pygame.display.set_mode(self.SCREENSIZE)
        #setting the icon
        icon = pygame.image.load(os.path.join('images','extras','icon.png'))
        pygame.display.set_icon(icon)
        pygame.display.set_caption('Space Shooter')

    def QUIT(self):
        #quiting the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
        return True

    def RUN(self):
        #the loop that ensures the game continues running
        won = None
        self.s0 = Starting_scene(self.SCREENSIZE, self.SCREEN, won)
        self.s1 = Playing_scene(self.SCREENSIZE, self.SCREEN)
        has_quit = True
        while has_quit:
            has_quit = self.QUIT()
            self.CLOCK.tick(self.FPS) #frame rate
            if self.s0.running:
                self.s0.RUN()
                if not self.s1.running:
                    self.s1 = Playing_scene(self.SCREENSIZE, self.SCREEN)
            elif self.s1.running:
                won = self.s1.RUN()
            else:
                self.s0 = Starting_scene(self.SCREENSIZE, self.SCREEN, won)
            pygame.display.flip()
            
if __name__ == '__main__':
    game = Frame()
    game.RUN()