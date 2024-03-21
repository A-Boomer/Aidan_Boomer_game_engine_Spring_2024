# This file was created by: Aidan Boomer
#Prooves it works
#changes with idetilce cde
 
# import libraries and modules
import pygame as pg
from settings import *
from sprites import *
from random import randint 
import sys
import pygame as pg
from sprites import *
pg.init()
from os import path
from healthbar import *
from random import randint
pg.mixer.init() 

'''
List-
health
mobs
maps
Wanting to add more maps to expand ganme while having health and mobs that can kill
'''
def draw_health_bar(surf, x, y, pct):
    if pct < 0:
        pct = 0
    BAR_LENGTH = 32
    BAR_HEIGHT = 10
    fill = (pct / 100) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)

    
 
# Define game class...
class Game:
    # Define a special method to init the properties of said class...
    def __init__(self):
        # init pygame
        pg.init()
        # set size of screen and be the screen
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        # setting game clock
        self.clock = pg.time.Clock()
        self.load_data()
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
      
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
        self.snd_folder = path.join(game_folder, 'sounds') 

    def new(self):
         pg.mixer.music.load(path.join(self.snd_folder, 'soundtrack2.mp3'))
    # code is broken cant figure out how to import sounds images 
    def load_data(self):
        game_folder = path.dirname(__file__)
        img_folder = path.join(game_folder, 'images')
        self.player_img = pg.image.load(path.join(img_folder, 'shrek.png')).convert_alpha()
        self.img_folder = path.join(game_folder, 'images')
        #block in pylance 
        self.snd_folder = path.join(game_folder, 'sounds')

        self.player_img = pg.image.load(path.join(self.img_folder, 'shrek.png')).convert_alpha()
        self.map_data = []
        with open(path.join(game_folder, 'map.txt'), 'r') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
 
    # Create run method which runs the whole GAME
    def new(self):
        print("create new game...")
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.power_ups = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.health = pg.sprite.Group()
        # self.player1 = Player(self, 1, 1)
        # for x in range(10, 20):
        # ranges
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)
                if tile == 'C':
                    Coin(self, col, row)
                if tile == 'H':
                    Health(self, col, row)
                if tile == 'M':
                    Mob(self, col, row)
    def run(self):
        #
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
         pg.quit()
         sys.exit()
 
    def update(self):
        self.all_sprites.update()

    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
   
    def draw_grid(self):
         for x in range(0, WIDTH, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
         for y in range(0, HEIGHT, TILESIZE):
              pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def draw_text(self, surface, text, size, color, x, y):
        font_name = pg.font.match_font('arial')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (x,y)
        surface.blit(text_surface, text_rect)
    def draw(self):
        print('drawing')
        draw_health_bar(self.screen, self.player.rect.x, self.player.rect.y-8, self.player.hitpoints)
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.draw_text(self.screen, "Lives " + str(self.player.hitpoints), 24, WHITE, 2, 3)
        self.all_sprites.draw(self.screen)
        # self.draw_text(self.screen, str(self.cooldown.current_time), 24, WHITE, WIDTH/2 - 32, 2)
        # self.draw_text(self.screen, str(self.cooldown.get_countdown()), 24, WHITE, WIDTH/2 - 32, 120)

        pg.display.flip()
 
    def events(self):
         for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            # if event.type == pg.KEYDOWN:
            #     if event.key == pg.K_LEFT:
            #         self.player.move(dx=-1)
            #     if event.key == pg.K_RIGHT:
            #         self.player.move(dx=1)
            #     if event.key == pg.K_UP:
            #         self.player.move(dy=-1)
            #     if event.key == pg.K_DOWN:
            #         self.player.move(dy=1)
                
    def show_start_screen(self):
        self.screen.fill(BGCOLOR)
        self.draw_text(self.screen, f"{TITLE}", 24, WHITE, WIDTH//2, HEIGHT//2)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False
    # def show_go_screen(self):
    #     if not self.running:
    #         return
    #     self.screen.fill(BGCOLOR)
    #     self.draw_text(self.screen, 24, WHITE, WIDTH/2, HEIGHT/2)
    #     pg.display.flip()
    #     self.wait_for_key()
  
# creates start screen
    def show_start_screen(self):
        # fills the background color
        self.screen.fill(BGCOLOR)
        # draws text on the background
        self.draw_text(self.screen, "Press a Key to Begin. Collect the coins without touching the enemies.", 24, WHITE, WIDTH/4 - 32, 2)
        # waits for a keyboard input to start the game
        pg.display.flip()
        self.wait_for_key()
 
    # creates loss screen
    def show_loss_screen(self):
        # Creates bank of insults
        myinsults = ["do better.", "wow!", "lil bro", "good luck chuck.", "Really?", "...", "WStop playing."]
        # fills the background color
        self.screen.fill(BGCOLOR)
        # draws text on the background
        # Adds random insult when you die - center centers the text in the space of 200 characters
        #self.draw_text(self.screen, random.choice(myinsults).center(200), 24, WHITE, 0, HEIGHT/2 - 24)
        # runs the game over method and opens the menu without closing it
        pg.display.flip()
        self.game_over()
 
    # creates victory screen
    def show_victory_screen(self):
        # Creates bank of compliments
        mycompliments = ["WIN!", "finally.", "Proud of you", "Nice!"]
        # fills the background color
        self.screen.fill(BGCOLOR)
        # draws text on the background
        # adds random compliment when you win - center centers the text in the space of 200 characters
        #self.draw_text(self.screen, random.choice(mycompliments).center(200), 24, WHITE, 0, HEIGHT/2 - 24)
        # runs the game over method and opens the menu without closing it
        pg.display.flip()
        self.game_over()
        # defines the wait for key method
    
    def wait_for_key(self):
        # when we are waiting, the clock ticks
        waiting = True
        while waiting:
            # our clock ticks based on frames per second
            self.clock.tick(FPS)
            # when we quit the game, run the quit method and we are no longer waiting
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                # when we release the key, we are no longer waiting
                if event.type == pg.KEYUP:
                    waiting = False
 
    # creates a new method that does not remove the menu when we release a key
    def game_over(self):
        # when we are waiting, the clock ticks
        waiting = True
        while waiting:
            # our clock ticks based on frames per second
            self.clock.tick(FPS)
            # when we quit the game, run the quit method and we are no longer waiting
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()


class SpeedUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.speed_up_img
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


    # Inside the load_data() method
        self.speed_up_img = pg.image.load(path.join(self.img_folder, 'speed_up.png')).convert_alpha()

    # Inside the Player class
def update(self):
    self.speed = PLAYER_SPEED
    # Handle player movement
    keys = pg.key.get_pressed() 
    if keys[pg.K_LEFT]:
        self.rect.x -= self.speed
        self.collide_with_power_ups('speed_up')
    # Add similar logic for other directions

def collide_with_power_ups(self, power_up_type):
    hits = pg.sprite.spritecollide(self, self.game.power_ups, True)
    for hit in hits:
        if power_up_type == 'speed_up':
            self.speed *= 2  # Double the player's speed temporarily
            pg.time.set_timer(SPEED_UP_EXPIRE_EVENT, 600)  # Set timer to reset speed after 5 seconds

            SPEED_UP_EXPIRE_EVENT = pg.USEREVENT + 1

            # Inside the events() method
        def events(self):
            if events.type == SPEED_UP_EXPIRE_EVENT:
                self.player.speed /= 2  # Reset speed back to normal
        
 
# Instantiate the game...
g = Game()
# use game method run to run
g.show_start_screen()
while True:
    g.new()
    g.run()
    # g.show_go_screen()