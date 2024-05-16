from image import *
from sound_effect import *

class Grenade(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos,direction):
        #starting set
        pygame.sprite.Sprite.__init__(self)
        self.timer = 200
        self.explosion_sound = Sound_effect()

        #movement variable
        self.throw_velocity = -11
        self.speed = 7
        self.direction = direction

        #grenade object rect
        self.image = Image().get_grenade_image()
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos,y_pos)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    #grenade movement and update
    def update(self,soldier_group,explosion_group,world):
        #delta of x and y to record current change
        self.throw_velocity += world.GRAVITY
        dx = self.direction * self.speed
        dy = self.throw_velocity

        #check for world collision
        for tile in world.obstacle_list:
            #x coordinate collision
            if tile[1].colliderect(self.rect.x + dx,self.rect.y,self.width,self.height):
                self.direction *= -1
                dx = self.direction * self.speed

            #y coordinate collision
            if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):
                self.speed = 0
                #check if below the ground
                if self.throw_velocity < 0:
                    self.throw_velocity = 0
                    dy = tile[1].bottom - self.rect.top

                #check if above the ground
                elif self.throw_velocity >= 0:
                    self.throw_velocity = 0
                    dy = tile[1].top - self.rect.bottom

        self.rect.x += dx + world.screen_scroll
        self.rect.y += dy

        #grenade countdown to explosion
        self.timer -= 1
        if self.timer <= 0:
            self.kill()
            self.explosion_sound.grenade_effect()
            explosion = Grenade_explosion(self.rect.x,self.rect.y,0.5)
            explosion_group.add(explosion)

            #deal damage to soldier that is close to grenade
            for soldier in soldier_group:
                if abs(self.rect.centerx - soldier.rect.centerx) < world.TILE_SIZE * 2 and abs(self.rect.centery - soldier.rect.centery) < world.TILE_SIZE * 2:
                    soldier.health -= 50

class Grenade_explosion(pygame.sprite.Sprite):
    def __init__(self,x_pos,y_pos,scale):
        #starting set
        pygame.sprite.Sprite.__init__(self)
        self.EXPLOSION_SPEED = 4

        #animation data initialize
        self.animation = Image().get_grenade_explode(scale)
        self.frame_index = 0
        self.counter = 0
        
        #grenade object rect
        self.image = self.animation[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos,y_pos)

    #grenade explosion and update
    def update(self,world):
        #scroll explosion with the world
        self.rect.x += world.screen_scroll

        self.counter += 1
        if self.counter >= self.EXPLOSION_SPEED:
            self.counter = 0
            self.frame_index += 1

            #check if the explosion is complete
            if self.frame_index >= len(self.animation):
                self.kill()
            else:
                self.image = self.animation[self.frame_index]