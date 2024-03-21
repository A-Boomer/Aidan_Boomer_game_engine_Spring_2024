# This file was created by: ishan routray
import pygame as pg
from settings import *
from healthbar import *
from random import randint
vec =pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.image.load('./Aidan_Boomer_game_engine_Spring_2024/images/shrek.png')
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.hitpoints = 100
    def update(self):
        self.speed = PLAYER_SPEED
    # Handle player movement
    keys = pg.key.get_pressed()
    if keys[pg.K_LEFT]:
        self.rect.x -= self.speed
    # Add similar logic for other directions

    # Check collision with enemies
    hits = pg.sprite.spritecollide(self, self.game.mobs, False)
    for hit in hits:
        self.game.player.hitpoints -= 10  # Reduce player health
        
    if self.game.player.hitpoints <= 0:
        self.game.show_loss_screen()  # If player health drops to zero, show loss screen

    # Check if player collects health
    hits = pg.sprite.spritecollide(self, self.game.health, True)
    for hit in hits:
        self.game.player.hitpoints += 20  # Increase player health
        self.collide_with_power_ups('speed_up')  # Check collision with power-ups
   
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -PLAYER_SPEED  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = PLAYER_SPEED  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -PLAYER_SPEED  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = PLAYER_SPEED
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
 
    # def move(self, dx=0, dy=0):
    #     if not self.collide_with_walls(dx, dy):
    #         self.x += dx
    #         self.y += dy
 
    # def collide_with_walls(self, dx=0, dy=0):
    #     for wall in self.game.walls:
    #         if wall.x == self.x + dx and wall.y == self.y + dy:
    #             return True
    #     return False
           
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
   #Made possible with Auyush
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
 
            if str(hits[0].__class__.__name__) == "PowerUp":
                print ("You just got Powered Up!")
            if str(hits[0].__class__.__name__) == "Health":
                self.hitpoints =+ 100
            
 
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        # add collision later
        self.collide_with_walls('x')
        self.rect.y = self.y
        # add collision later
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.health, True)
         
        # coin_hits = pg.sprite.spritecollide(self.game.coins, True)
        # if coin_hits:
        #     print("I got a coin")
       
 
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
 
class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Health(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.health
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE


class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_up
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
                self.groups = game.all_sprites, game.mobs
                pg.sprite.Sprite.__init__(self, self.groups)
                self.game = game
                self.image = pg.Surface((TILESIZE, TILESIZE))
                self.image.fill(RED)
                self.rect = self.image.get_rect()
                self.x = x
                self.y = y
                self.vx, self.vy = 100, 100
                self.x = x * TILESIZE
                self.y = y * TILESIZE
                self.speed = 1 
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        self.rect.x = randint(0, WIDTH)
        self.rect.y = randint(0, HEIGHT)
    
        if self.rect.left > WIDTH or self.rect.right < 0 or self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.rect.x = randint(0, WIDTH)
        self.rect.y = randint(0, HEIGHT)
        if pg.sprite.spritecollide(self, self.game.player, False):
            self.game.player.hitpoints -= 20  # Reduce player health if collided with the mob
        if self.game.player.hitpoints <= 0:
            self.game.show_loss_screen()  # If player health drops to zero, show loss screen
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

        self.collide_with_walls('y')

    vec =pg.math.Vector2

    def collide_with_walls(self, dir): #method in pygame library to check if player collides with walls
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width #subtracting width so that the player is directly next to wall
                if self.vx < 0:
                    self.x = hits[0].rect.right #registration point is already on right so self.width is not needed
                self.vx = 0 #resets velocity
                self.rect.x = self.x #resetting position of rectangle to self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False) #method in pygame to check if player collides with walls
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y


class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
            self.groups = game.all_sprites, game.mobs
            pg.sprite.Sprite.__init__(self, self.groups)
            self.game = game
            # self.image = game.mob
            self.image = pg.Surface((TILESIZE, TILESIZE))
            self.image.fill(ORANGE)
            self.rect = self.image.get_rect()
            # self.hit_rect.center = self.rect.center
            self.pos = vec(x, y) * TILESIZE
            self.vel = vec(0, 0)
            self.acc = vec(0, 0)
            self.rect.center = self.pos
            self.rot = 0
            self.speed = 150
        # self.health = MOB_HEALTH

    def collide_with_walls(sprite, group, dir):
     if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
     if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y