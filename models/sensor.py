from typing import Tuple
from shapely.geometry import Point

BLUE, RED = (0, 102, 204), (255, 0, 0)


class Sensor:
    def __init__(self, point: Point, color: Tuple = BLUE):
        self.point: Point = point
        self.color: Tuple = color
        self.old_color: Tuple = color
        self.crash: bool = False
        self.cell: Tuple = (int(point.x), int(point.y))

    def set_crash(self, is_crash: bool):
        if is_crash:
            self.crash = True
            self.color = RED
        else:
            self.crash = False
            self.color = self.old_color
