import pygame,os

class Image():
    #bullet image
    def get_bullet_image(self):
        return pygame.image.load("img/icons/bullet.png").convert_alpha()
    
    #grenade image
    def get_grenade_image(self):
        return pygame.image.load("img/icons/grenade.png").convert_alpha()

    #health box image
    def get_health_box_image(self):
        return pygame.image.load("img/icons/health_box.png").convert_alpha()

    #ammo box image
    def get_ammo_box_image(self):
        return pygame.image.load("img/icons/ammo_box.png").convert_alpha()

    #grenade box image
    def get_grenade_box_image(self):
        return pygame.image.load("img/icons/grenade_box.png").convert_alpha()

    #soldier animation image
    def get_soldier_animation(self,character_type,anime_type,scale):
        soldier_animation = []
        image_amount = len(os.listdir(f"img/{character_type}/{anime_type}"))

        #loop through all the types of state
        for i in range(image_amount):
            img = pygame.image.load(f"img/{character_type}/{anime_type}/{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(int(img.get_width() * scale),int(img.get_height() * scale)))
            soldier_animation.append(img)
        return soldier_animation

    #grenade explosion animation image
    def get_grenade_explode(self,scale):
        grenade_explode = []
        for i in range(1,6):
            img = pygame.image.load(f"img/explosion/exp{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(int(img.get_width() * scale),int(img.get_height() * scale)))
            grenade_explode.append(img)
        return grenade_explode
    
    #tile image
    def get_tile_image(self,tile_type,tile_size):
        tile = []
        for i in range(tile_type):
            img = pygame.image.load(f"img/tile/{i}.png").convert_alpha()
            img = pygame.transform.scale(img,(tile_size,tile_size))
            tile.append(img)
        return tile
    
    #background sky image
    def get_sky_image(self):
        return pygame.image.load("img/background/sky_cloud.png").convert_alpha()
    
    #background mountain image
    def get_mountain_image(self):
        return pygame.image.load("img/background/mountain.png").convert_alpha()
    
    #background pine image
    def get_pine_image(self):
        return pygame.image.load("img/background/pine1.png").convert_alpha()
    
    #background dark pine image
    def get_dark_pine_image(self):
        return pygame.image.load("img/background/pine2.png").convert_alpha()
    
    #start button image
    def get_start_button_image(self):
        return pygame.image.load("img/start_btn.png").convert_alpha()
    
    #exit button image
    def get_exit_button_image(self):
        return pygame.image.load("img/exit_btn.png").convert_alpha()

    #restart button image
    def get_restart_button_image(self):
        return pygame.image.load("img/restart_btn.png").convert_alpha()