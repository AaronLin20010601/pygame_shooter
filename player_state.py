from image import *

class Player_state():
    def __init__(self):
        #starting set
        self.font = pygame.font.SysFont("Futura",30)
        self.text_color = (255,255,255)
        self.max_health_color = (255,0,0)
        self.current_health_color = (0,255,0)
        self.health_bar_background = (0,0,0)

    #show all player state
    def show_player_state(self,player,screen):
        self.show_health(player,screen)
        self.show_ammo(player,screen)
        self.show_grenade(player,screen)

    #draw text on the game screen
    def draw_text(self,text,x_pos,y_pos,screen):
        img = self.font.render(text,True,self.text_color)
        screen.blit(img,(x_pos,y_pos))

    #show player health bar on the game screen
    def show_health(self,player,screen):
        pygame.draw.rect(screen,self.health_bar_background,(8,8,154,24))
        pygame.draw.rect(screen,self.max_health_color,(10,10,150,20))
        pygame.draw.rect(screen,self.current_health_color,(10,10,150 * (player.health / player.max_health),20))

    #show remaining ammo of player
    def show_ammo(self,player,screen):
        self.draw_text(f"AMMO : ",10,35,screen)
        for x in range(player.ammo):
            screen.blit(Image().get_bullet_image(),(90 + (x * 10), 40))

    #show remaining grenade of player
    def show_grenade(self,player,screen):
        self.draw_text(f"GRENADE : ",10,60,screen)
        for x in range(player.grenade):
            screen.blit(Image().get_grenade_image(),(135 + (x * 15), 60))