import pygame as pg
import numpy as np
import sys
from game import *

class Block(GameObjSolid):

    def __init__(self, grid, x, y, width, height, rgb):
        super().__init__(grid, x, y, width, height, rgb)


class BlockAngle(GameObjSolidAngle):

    def __init__(self, grid, x1, y1, x2, y2, rgb):
        super().__init__(grid, x1, y1, x2, y2, rgb)

