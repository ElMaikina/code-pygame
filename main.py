import pygame as pg
import numpy as np
import sys
from block import *
from game import *
from main import *
from player import *

# Initial conditions
pg.init()
clock = pg.time.Clock()
running = True
paused = False
scale = 3
grid = 12
time = 1
fps = 60

window_size = np.array([480, 270])

# Creates a display
display = pg.display.set_mode(window_size)
pg.display.set_caption('Game')

blocks = []
rgb = (255, 0, 255)
blocks.append(Block(grid, 0, 21, 40, 1, rgb))
rgb = (0, 255, 0)
blocks.append(Block(grid, 15, 18, 7, 1, rgb))
rgb = (0, 0, 255)
blocks.append(Block(grid, 20, 15, 15, 1, rgb))
rgb = (255, 255, 0)
#blocks.append(Block(grid, 24, 10, 5, 3, rgb))
rgb = (50, 255, 255)
blocks.append(Block(grid, 4, 4, 1, 3, rgb))
rgb = (255, 0, 0)
blocks.append(Block(grid, 7, 12, 3, 3, rgb))
blocks.append(Block(grid, 8, 15, 3, 3, rgb))
blocks.append(Block(grid, 8, 5, 3, 3, rgb))

angled = []
rgb = (255, 255, 0)
angled.append(BlockAngle(grid, 12, 12, 20, 13, rgb))
angled.append(BlockAngle(grid, 20, 13, 28, 8, rgb))

objects = blocks + angled

spr = 'sprites/sphere.png'
acc = 0.2
fri = 0.1
wlk = 3
run = 6
gf = 0.2
gl = grid
js = -4
x = 15
y = 10

player = Player(grid, x, y, acc, fri, wlk, run, gf, gl, js, spr)

# General game loop
while running:
    pressed_keys = pg.key.get_pressed()

	# See if the window has closed
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

    if pressed_keys[pg.K_ESCAPE]:
        pg.quit()
        sys.exit()
    	
    display.fill((0,0,50))
    	
    # Draws all of the sprites in the stage
    for object in objects:
        x = object.rect.left
        y  = object.rect.top
        display.blit(object.img, (x, y))

    # Make the player move
    player.move(grid, blocks, angled)
    x = player.rect.x
    y  = player.rect.y
    display.blit(player.img, (x, y))
	
    pg.display.update()
    clock.tick(fps)