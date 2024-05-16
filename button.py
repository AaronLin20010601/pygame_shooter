import pygame

class Button():
    def __init__(self,x_pos,y_pos,image,scale):
        #starting set
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width * scale),int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x_pos,y_pos)
        self.clicked = False

    #draw button on the screen
    def draw(self,screen):
        action = False
        mouse_position = pygame.mouse.get_pos()

        #check mouse position and click action
        if self.rect.collidepoint(mouse_position):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image,(self.rect.x,self.rect.y))
        return action