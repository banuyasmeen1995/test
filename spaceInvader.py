# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 21:51:58 2022

@author: ashia
"""
import pygame as pg
import random
import math
from pygame import mixer


class Screen:
    
    def __init__(self, width, height):
        # Screen
        self.screen = pg.display.set_mode((width,height))
        # running flag
        self.running = True
        # Icon and Title
        pg.display.set_caption("Space Invaders")
        self.icon = pg.image.load('files/icon.png').convert_alpha()
        pg.display.set_icon(self.icon)
        # Background
        self.background = pg.image.load('files/background.jpg').convert_alpha()
        self.background = pg. transform. scale(self.background, (800, 600))
        # background music
        mixer.music.load('files/background_music.wav')
        mixer.music.play(-1)
        
    def get_screen(self): # not really necessary if we have only one instance of screen
        return self.screen 
    
    def set_running(self):
        self.running = False
        
    def get_running(self):
        return self.running
    
    def set_background(self):
        # RGB values for galaxy purple
        # self.screen.fill((66,45,83)) 
        # background image
        self.screen.blit(self.background,(0,0))
        
    
    def update(self):
        # update the window regularly after all changes are made
        pg.display.update() 
    
    def close(self):
        if not self.running:
            pg.display.quit()
            pg.quit()

class Text:
    
    def __init__(self, screen, x = 10, y = 10, font_size = 32):
        self.x = x
        self.y = y
        self.font = pg.font.Font('files/Starjedi.ttf', font_size)
        self.val = 0 # needed for score
        self.screen = screen
        
    def get_val(self):
        return self.val
        
    def display(self, text):
        score = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(score, (self.x, self.y))
        
class Item:
    
    def __init__(self):
        self.screen = pg.display.get_surface() # gets the current active screen
        self.w, self.h = self.screen.get_size()
        self.xmargin = 10
        self.img = None
        self.x = None
        self.y = None
        self.deltaX = 0
        self.deltaY = 0
        
    def getX(self):
        return self.x
        
    def getY(self):
        return self.y
        
    def display(self):
        self.screen.blit(self.img, (self.x, self.y))
        
    def move(self):
        pass
        
        
class Player(Item):
    
    def __init__(self):
        super().__init__()
        self.img = pg.image.load('files/player2.png').convert_alpha()
        self.x = (self.w/2) - 32 # image size is 64*64
        self.y = self.h - 120 # some margin and img dim
        
    def setDir(self,direction):
        self.deltaX = direction * 0.6
        
    def move(self):
        # don't move any further if at left end
        if self.x < self.xmargin: 
            self.x = self.xmargin
        # don't move any further if at right end   
        if self.x > (self.w - 64 - self.xmargin): 
            self.x = (self.w - 64 - self.xmargin)
            
        self.x += self.deltaX
        self.display()
        
        
class Enemy(Item):

    def __init__(self):
        super().__init__()
        # random.seed(8)
        self.imgs = [pg.image.load('files/enemy{0}.png'.format(i)).convert_alpha()\
                     for i in range (1,6)]
        self.img = random.choice(self.imgs)
        # self.img = pg.image.load('files/enemy2.png')
        self.x = random.randint(self.xmargin,self.w - 64 - self.xmargin)
        self.y = random.randint(30,150) # tried values
        self.deltaX = 0.5
        self.deltaY = 40
        
    def respawn(self):
        self.x = random.randint(self.xmargin,self.w - 64 - self.xmargin)
        self.y = random.randint(30,150)
        # self.img = random.choice(self.imgs)
        
    def move(self):
        # start moving right if at left end, and move down
        if self.x < self.xmargin: 
            self.deltaX = 0.3
            self.y += self.deltaY
        # start moving left if at right end, and move down    
        if self.x > (self.w - 64 - self.xmargin): 
            self.deltaX = -0.3
            self.y += self.deltaY
        # keep moving across x-axis
        self.x += self.deltaX
        self.display()


class Bullet(Item):
    
    def __init__(self):
        super().__init__()
        self.img = pg.image.load('files/bullet.png').convert_alpha()
        self.y = self.h - 120 # some margin and img dim
        self.deltaY = -2.5 # only moves in y direction
        self.state = 'ready' # ready: can't see on screen; fire: it's moving
        self.hit = False # True if it hits an enemy
        
    def set_hit(self, bool_val):
        self.hit = bool_val
        
    def get_state(self):
        return self.state
        
    def fire(self, playerX):
        if self.state == 'ready':
            self.state = 'fire'
            self.x = playerX
            self.display()
            bullet_sound = mixer.Sound('files/laser.wav')
            bullet_sound.play()
        
    def reload(self):
        # reload if bullet is beyond scrren dimensions
        if (self.y < 0) or self.hit:
            self.set_hit(False)
            self.state = 'ready'
            self.y = self.h - 120
        
    def move(self):        
        if self.state == 'fire':
            self.display()
            self.y += self.deltaY
            
class PlayPause(Item):
    def __init__(self):
        super().__init__()
        self.img = pg.image.load('files/play.png')
        self.img2 = pg.image.load('files/pause.png')
        self.x = self.w - 64 - self.xmargin
        self.y = self.xmargin
        self.rect = self.img.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.clicked = False
        self.state = True # true: in_play; false: in_pause
        
    def get_state(self):
        return self.state
    
    def draw(self):
        action = False
        # get mouse position
        pos = pg.mouse.get_pos()
        # check mouse hover and clicked conditions
        if self.rect.collidepoint(pos):
            if pg.mouse.get_pressed()[0] and self.clicked == False:
                self.clicked = True
                self.state = not self.state
                action = True
        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False
            
        if self.state:
            self.screen.blit(self.img2, (self.x, self.y))
        elif not self.state:
            self.screen.blit(self.img, (self.x, self.y))
            
        return action
        

        
                   
###############################################################################

def isCollision(enemy, bullet):
    if bullet.get_state() == 'fire':
        # distance between top-center point of enemy and bullet
        dist = math.sqrt((((enemy.getX()+32) - (bullet.getX()+16))**2) + \
                             ((enemy.getY() - bullet.getY())**2))
        if dist <= 35:
            return True
    else:
        return False
                
                
def collisionHandle(enemyList, bullet, score_instance):
    for enemy in enemyList:
        if isCollision(enemy, bullet):
            score_instance.val += 1
            explosion_sound = mixer.Sound('files/blast.wav')
            explosion_sound.play()
            enemy.respawn()
            bullet.set_hit(True)
            bullet.reload()
            
def isGameOver(enemyList, player, go_text):
    for enemy in enemyList:
        if (enemy.y >= 410) and ((player.x) <= (enemy.x + 32) <= (player.x + 64)):
            for e in enemyList: 
                e.y = 2000
                e.deltaX = 0
            pg.mixer.music.stop()
            go_text.display("game over")
            break
        
def pause(enemyList, bullet):
    pg.mixer.music.pause()
    enemyDeltaX = []
    bulletDeltaY = bullet.deltaY
    bullet.deltaY = 0
    for e in enemyList: 
        enemyDeltaX.append(e.deltaX)
        e.deltaX = 0
        e.deltaY = 0
    return enemyDeltaX, bulletDeltaY

def play(enemyList, bullet, enemyDeltaX, bulletDeltaY):
    pg.mixer.music.unpause()
    bullet.deltaY = bulletDeltaY
    for i in range(len(enemyList)): 
        enemyList[i].deltaX = enemyDeltaX[i]
        enemyList[i].deltaY = 40
            
    
        
        

        
    