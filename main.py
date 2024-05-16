from grenade import *
from player_state import *
from world import *
from button import *
from screen_trans import *

#initialize
pygame.init()
pygame.mixer.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
FPS = 60

#game state initialize
start_game = False
start_intro = False
level = 1
MAX_LEVEL = 4
run = True
shoot = False
grenade = False
grenade_thrown = False

#game screen size
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

#game screen fade
intro_fade = Screen_transition(1,4)
death_fade = Screen_transition(2,4)

#game title
pygame.display.set_caption("Shooter")

#game music
sound = Sound_effect()
sound.play_music()

#game time clock
clock = pygame.time.Clock()

#soldier initialize
soldier_group = pygame.sprite.Group()

#weapon sprite group initialize
bullet_group = pygame.sprite.Group()
grenade_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()

#world decoration sprite group initialize
decoration_group = pygame.sprite.Group()
water_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

#create button
start_button = Button(SCREEN_WIDTH // 2 - 130,SCREEN_HEIGHT // 2 - 150,Image().get_start_button_image(),1)
exit_button = Button(SCREEN_WIDTH // 2 - 110,SCREEN_HEIGHT // 2 + 50,Image().get_exit_button_image(),1)
restart_button = Button(SCREEN_WIDTH // 2 - 120,SCREEN_HEIGHT // 2 - 50,Image().get_restart_button_image(),2)

#process world
world = World()
world_data = world.open_data(level)
player = world.process_data(world_data,soldier_group,item_group,decoration_group,water_group,exit_group)

#game loop
while run:
    #initialize game pace
    clock.tick(FPS)

    if start_game == False:
        world.draw_background(screen)
        if start_button.draw(screen):
            start_game = True
            start_intro = True
        if exit_button.draw(screen):
            run = False

    #start the game
    else:
    #draw game background
        world.draw_background(screen)
        world.draw(screen)
        Player_state().show_player_state(player,screen)

        #soldier update and draw
        for soldier in soldier_group:
            if soldier.character_type == "enemy":
                soldier.enemy_ai(player,bullet_group,world,water_group,exit_group)
            soldier.update()
            soldier.draw(screen)

        #weapon object update
        bullet_group.update(SCREEN_WIDTH,soldier_group,bullet_group,world)
        grenade_group.update(soldier_group,explosion_group,world)
        explosion_group.update(world)
        item_group.update(player,world)

        #decoration object update
        decoration_group.update(world)
        water_group.update(world)
        exit_group.update(world)

        #weapon object draw
        bullet_group.draw(screen)
        grenade_group.draw(screen)
        explosion_group.draw(screen)
        item_group.draw(screen)

        #decoration object draw
        decoration_group.draw(screen)
        water_group.draw(screen)
        exit_group.draw(screen)

        #show intro
        if start_intro == True:
            if intro_fade.fade(screen,SCREEN_WIDTH,SCREEN_HEIGHT):
                start_intro = False
                intro_fade.fade_counter = 0

        #player movememt animation if alive
        if player.alive:
            #player attack
            if shoot:
                player.shoot(bullet_group)
            elif grenade and grenade_thrown == False and player.grenade > 0:
                grenade = Grenade(player.rect.centerx + (0.5 * player.rect.size[0] * player.direction),player.rect.top,player.direction)
                grenade_group.add(grenade)
                grenade_thrown = True
                player.grenade -= 1
            
            #player move
            if player.in_air:
                player.update_action(2)
            elif player.move_left or player.move_right:
                player.update_action(1)
            else:
                player.update_action(0)
            world.screen_scroll,level_complete = player.move(player.move_left,player.move_right,world,water_group,exit_group)
            world.background_scroll -= world.screen_scroll

            #check if the level is complete
            if level_complete:
                start_intro = True
                level += 1
                world.background_scroll = 0
                world_data = world.reset_level(soldier_group,bullet_group,grenade_group,explosion_group,item_group,decoration_group,water_group,exit_group)
                if level <= MAX_LEVEL:
                    #reprocess world
                    world = World()
                    world_data = world.open_data(level)
                    player = world.process_data(world_data,soldier_group,item_group,decoration_group,water_group,exit_group)

        #when player die
        else:
            world.screen_scroll = 0
            if death_fade.fade(screen,SCREEN_WIDTH,SCREEN_HEIGHT):
                world.draw_background(screen)
                if restart_button.draw(screen):
                    death_fade.fade_counter = 0
                    start_intro = True
                    world.background_scroll = 0
                    world_data = world.reset_level(soldier_group,bullet_group,grenade_group,explosion_group,item_group,decoration_group,water_group,exit_group)

                    #reprocess world
                    world = World()
                    world_data = world.open_data(level)
                    player = world.process_data(world_data,soldier_group,item_group,decoration_group,water_group,exit_group)


    for event in pygame.event.get():
        #quit and close the game
        if event.type == pygame.QUIT:
            run = False
        
        #player control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.move_left = True
            if event.key == pygame.K_d:
                player.move_right = True
            if event.key == pygame.K_SPACE:
                shoot = True
            if event.key == pygame.K_q:
                grenade = True
            if event.key == pygame.K_w and player.alive:
                player.jump = True
                sound.jump_effect()
            if event.key == pygame.K_ESCAPE:
                run = False

        #keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.move_left = False
            if event.key == pygame.K_d:
                player.move_right = False
            if event.key == pygame.K_SPACE:
                shoot = False
            if event.key == pygame.K_q:
                grenade = False
                grenade_thrown = False

    #update the game display screen
    pygame.display.update()

#quit the game
pygame.quit()