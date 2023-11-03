import pygame as pg
import numpy as np
import math
import sys

class GameObj(pg.sprite.Sprite):

    def __init__(self, grid, x, y, sprite):
        super().__init__()
        self.img = pg.image.load(sprite).convert_alpha()
        self.rect = self.img.get_rect(left = x * grid, top = y * grid)

class GameObjSolid(pg.sprite.Sprite):

    def __init__(self, grid, x, y, width, height, rgb):
        super().__init__()
        self.width = width * grid
        self.height = height * grid        
        self.img = pg.Surface((self.width, self.height))
        self.img.fill(rgb)
        self.rect = self.img.get_rect(left = x * grid, top = y * grid)

class GameObjSolidAngle(pg.sprite.Sprite):

    def __init__(self, grid, x1, y1, x2, y2, rgb):
        super().__init__()
        dy = (y1 - y2) * grid
        dx = (x2 - x1) * grid
        center_x = (x1 + x2) / 2 * grid
        center_y = (y1 + y2) / 2 * grid
        self.width = math.hypot(dx, dy)
        self.angle = math.atan(dy / dx)
        angle = self.angle * 180 / np.pi
        self.height = 2
        self.img = pg.Surface((self.width, self.height), pg.SRCALPHA)
        self.img.fill(rgb)
        self.img = pg.transform.rotate(self.img, angle)
        self.rect = self.img.get_rect(center = (center_x, center_y))

class GameObjMoving(GameObj):

    def __init__(self, grid, x, y, sprite):
        super().__init__(grid, x, y, sprite)
        self.vel_x = 0
        self.vel_y = 0
    
    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.rect.left = self.x
        self.rect.top = self.y

    def limit(self, vel_x, vel_y):
        if abs(self.vel_x) > abs(vel_x):
            self.vel_x = vel_x * self.vel_x / abs(self.vel_x)
        
        if abs(self.vel_y) > abs(vel_y):
            self.vel_y = vel_y * self.vel_y / abs(self.vel_y)
    
    def friction(self, fri_x, fri_y):
        vel_x = self.vel_x
        vel_y = self.vel_y

        if vel_x > 0 and vel_x > fri_x:
            self.vel_x -= fri_x

        if vel_x < 0 and vel_x < -fri_x:
            self.vel_x += fri_x
        
        if vel_y > 0 and vel_y > fri_y:
            self.vel_y -= fri_y

        if vel_y < 0 and vel_y < -fri_y:
            self.vel_y += fri_y

        if abs(self.vel_x) < fri_x * 2:
            self.vel_x = 0
        
        if abs(self.vel_y) < fri_y * 2:
            self.vel_y = 0

class GameObjMovingSolid(GameObjMoving):

    def __init__(self, grid, x, y, sprite):
        super().__init__(grid, x, y, sprite)
        self.left = False
        self.right = False
        self.top = False
        self.bottom = False
    
    def move_rects(self, vel_x, vel_y, blocks):
        self.rect.x += vel_x
        self.rect.y += vel_y
        
        for block in blocks:
            if self.rect.colliderect(block.rect):
                
                if vel_x > 0:
                    self.rect.right = block.rect.left
                    self.right = True
                    self.vel_x = 0
                    
                if vel_x < 0:
                    self.rect.left = block.rect.right
                    self.left = True
                    self.vel_x = 0
                    
                if vel_y > 0:
                    self.rect.bottom = block.rect.top
                    self.bottom = True
                    self.vel_y = 0
                    
                if vel_y < 0:
                    self.rect.top = block.rect.bottom
                    self.top = True
                    self.vel_y = 0
    
    def move_angled(self, grid, vel_y, angled):
        for block in angled:
            if self.rect.colliderect(block.rect):
                
                angle = block.angle
                slope = np.tan(angle)
                x = self.rect.center[0]
                x1 = block.rect.left

                if angle >= 0:
                    y1 = block.rect.bottom 
                if angle < 0:
                    y1 = block.rect.top 
                
                y = y1 - ( (x - x1) * slope)
                
                top = self.rect.top
                bot = self.rect.bottom
                
                if top < y and bot + vel_y >= y and vel_y > 0:
                    self.bottom = True
                    self.rect.bottom = y
                    self.vel_y = grid * abs(slope)
                
                if bot > y and top + vel_y <= y and vel_y < 0:
                    self.top = True
                    self.rect.top = y
                    self.vel_y = grid * abs(slope)
                

    def move_simple(self, grid, vel_x, vel_y, blocks):
        self.right = False
        self.left = False
        self.bottom = False
        self.top = False
        self.move_rects(vel_x, 0, blocks)
        self.move_rects(0, vel_y, blocks)

    def move_precise(self, grid, vel_x, vel_y, blocks, angled):
        self.right = False
        self.left = False
        self.bottom = False
        self.top = False
        self.move_rects(vel_x, 0, blocks)
        self.move_rects(0, vel_y, blocks)
        self.move_angled(grid, vel_y, angled)

class GameObjKinetic(GameObjMovingSolid):
    def __init__(self, grid, x, y, gforce, glimit, sprite):
        super().__init__(grid, x, y, sprite)
        self.gforce = gforce
        self.glimit = glimit

    def gravity(self):
        self.vel_y += self.gforce
        self.limit(self.vel_x, self.glimit)
    
