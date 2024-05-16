from image import *

class Item_box(pygame.sprite.Sprite):
    def __init__(self,tile_size,item_type,x_pos,y_pos):
        #starting set
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type

        #item image initialize
        health_box = Image().get_health_box_image()
        ammo_box = Image().get_ammo_box_image()
        grenade_box = Image().get_grenade_box_image()
        item_boxes = {"Health" : health_box,"Ammo" : ammo_box,"Grenade" : grenade_box}

        #item object rect
        self.image = item_boxes[self.item_type]
        self.rect = self.image.get_rect()
        self.rect.midtop = (x_pos + tile_size // 2,y_pos + (tile_size - self.image.get_height()))

    #item update
    def update(self,soldier,world):
        #scroll item with the world
        self.rect.x += world.screen_scroll

        if pygame.sprite.collide_rect(self,soldier):
            #after player get health box
            if self.item_type == "Health":
                soldier.health += 25
                if soldier.health > soldier.max_health:
                    soldier.health = soldier.max_health

            #after player get ammo box
            elif self.item_type == "Ammo":
                soldier.ammo += 15
                if soldier.ammo > soldier.max_ammo:
                    soldier.ammo = soldier.max_ammo

            #after player get grenade box
            elif self.item_type == "Grenade":
                soldier.grenade += 3
                if soldier.grenade > soldier.max_grenade:
                    soldier.grenade = soldier.max_grenade

            self.kill()