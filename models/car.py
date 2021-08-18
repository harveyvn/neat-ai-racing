from typing import List
from .sensor import Sensor

import pygame
import math
from shapely.geometry import Point

screen_width = 1500
screen_height = 800
BLUE, RED = (0, 102, 204), (255, 0, 0)
CAR_BBOX = 90 / 2


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


class Car:
    def __init__(self, screen):
        self.pos = Point(600, 650)
        self.center = Point(645, 695)
        self.sensors: List[Sensor] = []
        self.surface = pygame.image.load("assets/car.png")
        self.rotate_surface = self.surface
        self.angle = 0
        self.speed = 15
        self.screen = screen

    @staticmethod
    def get_point(p: Point):
        return [p.x, p.y]

    def draw_sensors(self):
        for s in self.sensors:
            pygame.draw.circle(self.screen, s.color, [s.point.x, s.point.y], 5)

    def draw(self):
        pygame.draw.circle(self.screen, RED, [self.center.x, self.center.y], 5)
        self.sensors = self.generate_sensors()

    @staticmethod
    def calculate_next_point(p: Point, angle: float, distance: float) -> Point:
        # Calculate point, given point(x y), angle, and distance
        # e.g. x=5*cos(ɑ) y=5*sin(ɑ)
        x = p.x + distance * math.cos(math.radians(360 - angle))
        y = p.y + distance * math.sin(math.radians(360 - angle))
        # Check boundary
        x = 20 if x < 20 else x
        x = screen_width - 260 if x > screen_width - 260 else x
        y = 20 if y < 20 else y
        y = screen_height - 120 if y > screen_height - 120 else y
        return Point(x, y)

    def generate_sensors(self) -> List[Sensor]:
        p = self.center
        # Follow clockwise
        sensors: List[Sensor] = []
        for deg in [30, 150, 210, 330]:  # [top_right, bottom_right, bottom_left, top_left]
            sensors.append(Sensor(Point(p.x + CAR_BBOX * math.cos(math.radians(self.angle + deg)),
                                        p.y + CAR_BBOX * math.sin(math.radians(self.angle + deg)))))
        return sensors

    def update(self, map):
        self.rotate_surface = rot_center(self.surface, self.angle)
        # check position and update the car position
        self.pos = self.calculate_next_point(self.pos, self.angle, self.speed)
        self.center = Point(self.pos.x + 45, self.pos.y + 45)
        self.sensors = self.generate_sensors()

        for s in self.sensors:
            if map.get_at(s.cell) == (255, 255, 255, 255):
                s.set_crash(True)
                self.angle += 10
            else:
                s.set_crash(False)
        print("=================")
