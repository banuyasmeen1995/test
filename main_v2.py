# -*- coding: utf-8 -*-
"""
Created on Sat Oct 15 18:52:47 2022

@author: ashia
"""

import pygame as pg
import spaceInvader as si

# Initialize the pygame
pg.init()

# create a blank screen
width = 800
height = 600
screen1 = si.Screen(width, height)

# Score
score = si.Text(screen1.get_screen())

# game over text
go_text = si.Text(screen1.get_screen(), 200, 250, 64)

# play pause button
pp_button = si.PlayPause()

# Player
p1 = si.Player()

# Enemy
numEnemies = 5
e = [si.Enemy() for i in range(numEnemies)]

# Bullet
b1 = si.Bullet()

# Game Loop
while screen1.get_running():
    
    screen1.set_background()
    if pp_button.draw():
        
        if not pp_button.get_state(): # game in pause state so call pause()
            enemyDeltaX, bulletDeltaY = si.pause(e, b1)
        else: # game in play state so call play()
            si.play(e, b1, enemyDeltaX, bulletDeltaY)
    
    # event related changes here
    for event in pg.event.get(): # check for any event
        
        if event.type == pg.QUIT: # check if X is clicked
            screen1.set_running() 
            
        # if keystroke is pressed check whether its right or left
        if event.type == pg.KEYDOWN: # key is pressed
            if event.key == pg.K_LEFT:
                p1.setDir(-1)
            if event.key == pg.K_RIGHT:
                p1.setDir(1)
            if event.key == pg.K_SPACE:
                b1.fire(p1.getX())
                
        if event.type == pg.KEYUP: # key is realsed
            if event.key == pg.K_LEFT or event.key == pg.K_RIGHT:
                p1.setDir(0)
    
    si.collisionHandle(e, b1, score) 
    score.display("Score: " + str(score.get_val()))
    si.isGameOver(e, p1, go_text)
    b1.reload()
    b1.move()       
    p1.move()
    for i in range(numEnemies): e[i].move()
    
    # update the window regularly after all changes are made
    screen1.update()       
    
    # close the window if X was clicked (always in the end)      
    screen1.close()
            
    
    