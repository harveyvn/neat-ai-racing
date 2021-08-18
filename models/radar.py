from typing import Tuple
from shapely.geometry import Point

ORANGE = (255, 128, 0)


class Radar:
    def __init__(self, origin: Point, color: Tuple = ORANGE):
        self.origin: Point = origin
        self.target: Point = origin
        self.color: Tuple = color
        self.cell: Tuple = (int(origin.x), int(origin.y))
        self.length = 1
        self.max_len = 100

    def update(self, target):
        self.length += 1
        self.target = target
        self.cell = (int(target.x), int(target.y))
