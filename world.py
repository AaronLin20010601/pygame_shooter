import csv
from soldier import *
from item_box import *

class World():
    def __init__(self):
        #screen initialize
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = int(self.SCREEN_WIDTH * 0.8)
        self.LEVEL_ROWS = 16
        self.LEVEL_COLS = 150

        #tile initialize
        self.GRAVITY = 0.75
        self.TILE_SIZE = self.SCREEN_HEIGHT // self.LEVEL_ROWS
        self.TILE_TYPE = 21
        self.tile_list = Image().get_tile_image(self.TILE_TYPE,self.TILE_SIZE)
        self.obstacle_list = []

        #background image
        self.sky_img = Image().get_sky_image()
        self.mountain_img = Image().get_mountain_image()
        self.pine_img = Image().get_pine_image()
        self.dark_pine_img = Image().get_dark_pine_image()

        #background scroll variable
        self.SCROLL_THRESH = 200
        self.screen_scroll = 0
        self.background_scroll = 0
        self.background_width = self.sky_img.get_width()

    #draw background
    def draw_background(self,screen):
        for x in range(5):
            screen.blit(self.sky_img,((x * self.background_width) - self.background_scroll * 0.5,0))
            screen.blit(self.mountain_img,((x * self.background_width) - self.background_scroll * 0.6,self.SCREEN_HEIGHT - self.mountain_img.get_height() - 300))
            screen.blit(self.pine_img,((x * self.background_width) - self.background_scroll * 0.7,self.SCREEN_HEIGHT - self.pine_img.get_height() - 150))
            screen.blit(self.dark_pine_img,((x * self.background_width) - self.background_scroll * 0.8,self.SCREEN_HEIGHT - self.dark_pine_img.get_height()))

    #read and open the world data file
    def open_data(self,level):
        world_data = [[-1 for j in range(self.LEVEL_COLS)] for i in range(self.LEVEL_ROWS)]
        with open(f"level/level{level}_data.csv",newline = "") as csvfile:
            reader = csv.reader(csvfile,delimiter = ",")
            for x_pos,row in enumerate(reader):
                for y_pos,tile in enumerate(row):
                    world_data[x_pos][y_pos] = int(tile)
        return world_data

    #process and print out data file into map
    def process_data(self,data,soldier_group,item_group,decoration_group,water_group,exit_group):
        #get level length
        self.level_length = len(data[0])

        for y_pos,row in enumerate(data):
            for x_pos,tile in enumerate(row):
                if tile >= 0:
                    img = self.tile_list[tile]
                    img_rect = img.get_rect()
                    img_rect.x = x_pos * self.TILE_SIZE
                    img_rect.y = y_pos * self.TILE_SIZE
                    tile_data = (img,img_rect)

                    #dirt block
                    if tile >= 0  and tile <= 8:
                        self.obstacle_list.append(tile_data)

                    #water block
                    elif tile >= 9 and tile <= 10:
                        water = Water(img,x_pos * self.TILE_SIZE,y_pos * self.TILE_SIZE)
                        water_group.add(water)

                    #decoration block
                    elif tile >= 11 and tile <= 14:
                        decoration = Decoration(img,x_pos * self.TILE_SIZE,y_pos * self.TILE_SIZE)
                        decoration_group.add(decoration)
                    
                    #create player
                    elif tile == 15:
                        player = Soldier("player",x_pos * self.TILE_SIZE,y_pos * self.TILE_SIZE,1.65,5,20,5,100)
                        soldier_group.add(player)

                    #create enemy
                    elif tile == 16:
                        enemy = Soldier("enemy",x_pos * self.TILE_SIZE,y_pos * self.TILE_SIZE,1.65,2,20,0,20)
                        soldier_group.add(enemy)

                    #create ammo box
                    elif tile == 17:
                        ammo_box = Item_box(self.TILE_SIZE,"Ammo",x_pos * self.TILE_SIZE,y_pos * self.TILE_SIZE)
                        item_group.add(ammo_box)

                    #create grenade box
                    elif tile == 18:
                        grenade_box = Item_box(self.TILE_SIZE,"Grenade",x_pos * self.TILE_SIZE,y_pos * self.TILE_SIZE)
                        item_group.add(grenade_box)

                    #create health box
                    elif tile == 19:
                        health_box = Item_box(self.TILE_SIZE,"Health",x_pos * self.TILE_SIZE,y_pos * self.TILE_SIZE)
                        item_group.add(health_box)

                    #create exit
                    elif tile == 20:
                        exit = Exit(img,x_pos * self.TILE_SIZE,y_pos * self.TILE_SIZE)
                        exit_group.add(exit)
        return player

    #draw all obstacle item on the screen
    def draw(self,screen):
        for tile in self.obstacle_list:
            tile[1][0] += self.screen_scroll
            screen.blit(tile[0],tile[1])

    #reset level when new level start or restart original level
    def reset_level(self,soldier_group,bullet_group,grenade_group,explosion_group,item_group,decoration_group,water_group,exit_group):
        soldier_group.empty()
        bullet_group.empty()
        grenade_group.empty()
        explosion_group.empty()
        item_group.empty()
        decoration_group.empty()
        water_group.empty()
        exit_group.empty()

        #return empty tile list data
        empty_data = [[-1 for j in range(self.LEVEL_COLS)] for i in range(self.LEVEL_ROWS)]
        return empty_data

class Decoration(pygame.sprite.Sprite):
    def __init__(self,img,x_pos,y_pos):
        #starting set
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x_pos + World().TILE_SIZE // 2,y_pos + (World().TILE_SIZE) - self.image.get_height())

    #scroll decoration with the world
    def update(self,world):
        self.rect.x += world.screen_scroll

class Water(pygame.sprite.Sprite):
    def __init__(self,img,x_pos,y_pos):
        #starting set
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x_pos + World().TILE_SIZE // 2,y_pos + (World().TILE_SIZE) - self.image.get_height())

    #scroll water with the world
    def update(self,world):
        self.rect.x += world.screen_scroll

class Exit(pygame.sprite.Sprite):
    def __init__(self,img,x_pos,y_pos):
        #starting set
        pygame.sprite.Sprite.__init__(self)
        self.image = img
        self.rect = self.image.get_rect()
        self.rect.midtop = (x_pos + World().TILE_SIZE // 2,y_pos + (World().TILE_SIZE) - self.image.get_height())

    #scroll exit with the world
    def update(self,world):
        self.rect.x += world.screen_scroll