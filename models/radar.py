from typing import Tuple
from shapely.geometry import Point

GREEN = (0, 255, 0)


class Radar:
    def __init__(self, origin: Point, color: Tuple = GREEN):
        self.origin: Point = origin
        self.target: Point = origin
        self.color: Tuple = color
        self.cell: Tuple = (int(origin.x), int(origin.y))
        self.length = 1
        self.max_len = 100000

    def update(self, target):
        self.length += 1
        self.target = target
        self.cell = (int(target.x), int(target.y))
