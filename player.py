import pygame as pg
import numpy as np
import sys
from game import *

class Player(GameObjKinetic):

    def __init__(self, grid, x, y, acc, fri, wlk, run, gforce, glimit, jump, sprite):
        super().__init__(grid, x, y, gforce, glimit, sprite)
        self.acc = acc
        self.fri = fri
        self.wlk = wlk
        self.run = run
        self.vel = wlk
        self.jump = jump
        self.jumped = False
    
    def move(self, grid, blocks, angled):
        super().move_precise(grid, self.vel_x, self.vel_y, blocks, angled)
        super().limit(self.vel, grid)
        super().gravity()
    
        keys = pg.key.get_pressed()
        
        if keys[pg.K_RIGHT]:
            self.vel_x += self.acc
            
        if keys[pg.K_LEFT]:
            self.vel_x -= self.acc
        
        if not self.jumped:
            if keys[pg.K_x] and self.bottom:
                self.vel_y = self.jump
                self.jumped = True

            if keys[pg.K_x] and not self.bottom:
                if self.left:
                    self.vel_y = self.jump
                    self.vel_x = self.wlk
                    self.jumped = True

                if self.right:
                    self.vel_y = self.jump
                    self.vel_x = -self.wlk
                    self.jumped = True

        if not keys[pg.K_x]:
            self.jumped = False
        
        if self.bottom:
            if not keys[pg.K_z]:
                self.vel = self.wlk

            if keys[pg.K_z]:
                self.vel = self.run

        if not keys[pg.K_RIGHT] and not keys[pg.K_LEFT]:
            super().friction(self.fri, 0)
            
