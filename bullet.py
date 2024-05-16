from image import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos,direction):
        #starting set
        pygame.sprite.Sprite.__init__(self)

        #movement variable
        self.speed = 20
        self.direction = direction

        #bullet object rect
        self.image = Image().get_bullet_image()
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos,y_pos)
        
    #bullet movement and update
    def update(self,width,soldier_group,bullet_group,world):
        #move nullet
        self.rect.x += (self.direction * self.speed) + world.screen_scroll

        if self.rect.right < 0 or self.rect.left > width:
            self.kill()

        #check if the bullet collide with world block
        for tile in world.obstacle_list:
            if tile[1].colliderect(self.rect):
                self.kill()
        
        #check if the bullet collide to soldier
        for soldier in soldier_group:
            if pygame.sprite.spritecollide(soldier,bullet_group,False):
                if soldier.alive:
                    soldier.health -= 5
                    self.kill()