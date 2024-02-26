# libraries
import pygame as pg
import sys

# TRANSPLANT THIS...
from os import path

#>>>>>>>>>>>>>>>>>>>>>SETTINGS<<<<<<<<<<<<<<<<<<<<

# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
LIGHTGREY = (100, 100, 100)

# game settings
TILESIZE = 64
WIDTHFACTOR = 8
HEIGHTFACTOR = 8
WIDTH = TILESIZE*WIDTHFACTOR   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = TILESIZE*HEIGHTFACTOR # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = WHITE
 

#>>>>>>>>>>>>>>>>>>>>>SPRITES<<<<<<<<<<<<<<<<<<<<
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # add wall to groups via the Sprite class parameter
        self.groups = game.all_sprites, game.walls
        # init superclass
        pg.sprite.Sprite.__init__(self, self.groups)
        # add game to properties of wall class
        self.game = game
        # setup image in pygame using Surface class
        self.image = pg.Surface((TILESIZE, TILESIZE))
        # fill the image
        self.image.fill(BLUE)
        # get the rectangular dimensions and locations using the get_rect method
        self.rect = self.image.get_rect()
        # create the x and y coordinate properties for use below
        self.x = x
        self.y = y
        # set the x and y coordinate properties using the rect from get_rect
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

#>>>>>>>>>>>>>>>>>>>>>GAME CLASS<<<<<<<<<<<<<<<<<<<<        
class Game:
    def __init__(self):
        # init the pygame module
        pg.init()
        # use pygame display to setup screen properties for game
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        # set window caption
        pg.display.set_caption(TITLE)
        # setup the pg clock
        self.clock = pg.time.Clock()
        # set the key repeat interval for keyboard controls
        pg.key.set_repeat(500, 100)
        # call the load data method below
        self.load_data()

    # TRANSPLANT THIS
    def load_data(self):
        game_folder = path.dirname(__file__)
        self.map_data = []
        # 'r'     open for reading (default)
        # 'w'     open for writing, truncating the file first
        # 'x'     open for exclusive creation, failing if the file already exists
        # 'a'     open for writing, appending to the end of the file if it exists
        # 'b'     binary mode
        # 't'     text mode (default)
        # '+'     open a disk file for updating (reading and writing)
        # 'U'     universal newlines mode (deprecated)
        # below opens file for reading in text mode
        # with 
        '''
        The with statement is a context manager in Python. 
        It is used to ensure that a resource is properly closed or released 
        after it is used. This can help to prevent errors and leaks.
        '''
        with open(path.join(game_folder, 'map.txt'), 'rt') as f:
            for line in f:
                print(line)
                self.map_data.append(line)
    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        # TRANSPLANT THIS
        for row, tiles in enumerate(self.map_data):
            print(row)
            for col, tile in enumerate(tiles):
                print(col)
                if tile == '1':
                    print("a wall at", row, col)
                    Wall(self, col, row)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()
    def quit(self):
        pg.quit()
        sys.exit()

    #>>>>>>>>>>>>>>>>>>>>>INPUT<<<<<<<<<<<<<<<<<<<<    
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

    #>>>>>>>>>>>>>>>>>>>>>PROCESS<<<<<<<<<<<<<<<<<<<<
    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
    
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
        text_rect.topleft = (x*TILESIZE,y*TILESIZE)
        surface.blit(text_surface, text_rect)

    #>>>>>>>>>>>>>>>>>>>>>OUTPUT<<<<<<<<<<<<<<<<<<<<
    def draw(self):
        self.screen.fill(BGCOLOR)
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        # self.draw_text(self.screen, "Hello world", 42, BLACK, 2, 2)
        self.draw_text(self.screen, str(self.dt), 42, BLACK, 1, 1)
        pg.display.flip()
    
#>>>>>>>>>>>>>>>>>>>>>INSTANTIATE GAME CLASS<<<<<<<<<<<<<<<<<<<<
g = Game()

#>>>>>>>>>>>>>>>>>>>>>GAME LOOP<<<<<<<<<<<<<<<<<<<<
while True:
    g.new()
    g.run()
