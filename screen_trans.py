import pygame

class Screen_transition():
    def __init__(self,direction,speed):
        #starting set
        self.direction = direction
        self.speed = speed
        self.intro_color = (0,0,0)
        self.death_color = (235,65,54)
        self.fade_counter = 0

    #fade transition effect
    def fade(self,screen,screen_width,screen_height):
        fade_complete = False
        self.fade_counter += self.speed

        #intro fade
        if self.direction == 1:
            pygame.draw.rect(screen,self.intro_color,(0 - self.fade_counter,0,screen_width // 2,screen_height))
            pygame.draw.rect(screen,self.intro_color,(screen_width // 2 + self.fade_counter,0,screen_width,screen_height))
            pygame.draw.rect(screen,self.intro_color,(0,0 - self.fade_counter,screen_width,screen_height // 2))
            pygame.draw.rect(screen,self.intro_color,(0,screen_height // 2 + self.fade_counter,screen_width,screen_height))

        #death fade
        if self.direction == 2:
            pygame.draw.rect(screen,self.death_color,(0,0,screen_width,0 + self.fade_counter))
        
        if self.fade_counter >= screen_width:
            fade_complete = True
        return fade_complete