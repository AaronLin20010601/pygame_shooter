import random
from bullet import *
from sound_effect import *

class Soldier(pygame.sprite.Sprite):
    #soldier initialize
    def __init__(self,character_type,x_pos,y_pos,scale,speed,ammo,grenade,health):
        #starting set
        pygame.sprite.Sprite.__init__(self)
        self.character_type = character_type

        #soldier variable
        self.speed = speed
        self.health = health
        self.max_health = health
        self.ammo = ammo
        self.max_ammo = 30
        self.grenade = grenade
        self.max_grenade = 10
        self.shot_sound = Sound_effect()

        #movement variable
        self.direction = 1
        self.jump_velocity = 0
        self.shoot_cooldown = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.alive = True

        #animation data initialize
        self.animation = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #append all animation into list
        animation_type = ["Idle","Run","Jump","Death"]
        for anime_type in animation_type:
            self.animation.append(Image().get_soldier_animation(self.character_type,anime_type,scale))

        #soldier object rect
        self.image = self.animation[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos,y_pos)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

        #move state
        self.move_left = False
        self.move_right = False

        #enemy ai variable
        self.move_counter = 0
        self.vision = pygame.Rect(0,0,150,20)
        self.idling = False
        self.idling_counter = 0

    #update all movemont of the soldier
    def update(self):
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    #move the soldier
    def move(self,move_left,move_right,world,water_group,exit_group):
        screen_scroll = 0

        #delta of x and y to record current change
        dx = 0
        dy = 0

        #change state after moving
        if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        if self.jump == True and self.in_air == False:
            self.jump_velocity = -11
            self.jump = False
            self.in_air = True

        #jump velocity dynamic changing
        self.jump_velocity += world.GRAVITY
        if self.jump_velocity > 10:
            self.jump_velocity
        dy += self.jump_velocity
        
        #check for world collision
        for tile in world.obstacle_list:
            #x coordinate collision
            if tile[1].colliderect(self.rect.x + dx,self.rect.y,self.width,self.height):
                dx = 0

                #if enemy reach the wall then turn around
                if self.character_type == "enemy":
                    self.direction *= -1
                    self.move_counter = 0

            #y coordinate collision
            if tile[1].colliderect(self.rect.x,self.rect.y + dy,self.width,self.height):
                #check if below the ground
                if self.jump_velocity < 0:
                    self.jump_velocity = 0
                    dy = tile[1].bottom - self.rect.top

                #check if above the ground
                elif self.jump_velocity >= 0:
                    self.jump_velocity = 0
                    self.in_air = False
                    dy = tile[1].top - self.rect.bottom

        #check for water collision
        if pygame.sprite.spritecollide(self,water_group,False):
            self.health -= 1

        #check for exit collision
        level_complete = False
        if self.character_type == "player" and pygame.sprite.spritecollide(self,exit_group,False):
            level_complete = True

        #check if player fall out of the world
        if self.rect.bottom > world.SCREEN_HEIGHT:
            self.health -= 1

        #check if player go out of the world map
        if self.character_type == "player":
            if self.rect.left + dx < 0 or self.rect.right + dx > world.SCREEN_WIDTH:
                dx = 0
        
        #update rect position
        self.rect.x += dx
        self.rect.y += dy

        #update screen scroll based on player position
        if self.character_type == "player":
            if ((self.rect.right > world.SCREEN_WIDTH - world.SCROLL_THRESH and
                world.background_scroll < (world.level_length * world.TILE_SIZE) - world.SCREEN_WIDTH)
                or (self.rect.left < world.SCROLL_THRESH and world.background_scroll > dx)):
                self.rect.x -= dx
                screen_scroll = -dx
        return screen_scroll,level_complete

    #shoot bullets from soldier
    def shoot(self,bullet_group):
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 20
            bullet = Bullet(self.rect.centerx + (0.75 * self.rect.size[0] * self.direction),self.rect.centery,self.direction)
            bullet_group.add(bullet)
            self.ammo -= 1
            self.shot_sound.shot_effect()

    #enemy soldier basic ai
    def enemy_ai(self,player,bullet_group,world,water_group,exit_group):
        #scroll enemy with the world
        self.rect.x += world.screen_scroll
        self.vision.x += world.screen_scroll

        if self.alive and player.alive:
            #randomly become idling
            if self.idling == False and random.randint(1,200) == 1:
                self.update_action(0)
                self.idling = True
                self.idling_counter = 50

            #when see player starting attack
            if self.vision.colliderect(player.rect):
                self.update_action(0)
                self.shoot(bullet_group)

            #when does not see player
            else:
                #when enemy is not idling
                if self.idling == False:
                    if self.direction == 1:
                        ai_moving_right = True
                    else:
                        ai_moving_right = False
                    ai_moving_left =  not ai_moving_right
                    self.move(ai_moving_left,ai_moving_right,world,water_group,exit_group)
                    self.update_action(1)

                    #change direction and vision after certain time
                    self.move_counter += 1
                    self.vision.center = (self.rect.centerx + 75 * self.direction,self.rect.centery)
                    if self.move_counter > world.TILE_SIZE:
                        self.direction *= -1
                        self.move_counter *= -1
            
                #when enemy is idling
                else:
                    self.idling_counter -= 1
                    if self.idling_counter <= 0:
                        self.idling = False

    #update soldier animation
    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        self.image = self.animation[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1

        #continuous looping current animation
        if self.frame_index >= len(self.animation[self.action]):
            if self.action == 3:
                self.frame_index = len(self.animation[self.action]) - 1
            else:
                self.frame_index = 0

    #update soldier action state
    def update_action(self,new_action):
        if new_action != self.action:
            self.action = new_action
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()

    #check if the soldier is still alive
    def check_alive(self):
        if self.health <= 0:
            self.health = 0
            self.speed = 0
            self.alive = False
            self.update_action(3)

    #draw the soldier on the game screen
    def draw(self,screen):
        screen.blit(pygame.transform.flip(self.image,self.flip,False),self.rect)