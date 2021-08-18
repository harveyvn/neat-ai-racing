import pygame
import math
from shapely.geometry import Point
from typing import List
from .sensor import Sensor
from .radar import Radar
from .libs import calculate_next_point, rot_center

screen_width = 1500
screen_height = 800
BLUE, RED, ORANGE = (0, 102, 204), (255, 0, 0), (255, 128, 0)
OUT_OF_STREET = (255, 255, 255, 255)
CAR_BBOX = 80 / 2
SCREEN_WIDTH, SCREEN_HEIGHT = 1500, 800


class Car:
    def __init__(self, map_game, asset):
        self.pos = Point(600, 650)
        self.center = Point(645, 695)
        self.sensors: List[Sensor] = []
        self.radars: List[Radar] = []
        self.surface = pygame.image.load(asset)
        self.rotate_surface = self.surface
        self.angle = 0
        self.speed = 15
        self.map = map_game
        self.is_alive = True
        self.distance = 0
        self.time_spent = 0

    def get_point(self):
        return [self.pos.x, self.pos.y]

    def get_surface(self):
        return self.rotate_surface

    def get_distance(self):
        return self.distance / 100

    def get_time_spent(self):
        return self.time_spent

    def get_alive(self):
        return self.is_alive

    def get_data(self):
        ret = [0, 0, 0, 0, 0]
        for i, r in enumerate(self.radars):
            ret[i] = int(r.length) / 100
        return ret

    def generate_sensors(self) -> List[Sensor]:
        p = self.center
        sensors: List[Sensor] = []  # Follow clockwise
        for d in [30, 150, 210, 330]:  # [right_top, left_top, left_bottom, right_bottom]
            deg = 360 - (self.angle + d)
            sensors.append(Sensor(Point(p.x + CAR_BBOX * math.cos(math.radians(deg)),
                                        p.y + CAR_BBOX * math.sin(math.radians(deg)))))
        return sensors

    def generate_radars(self) -> List[Radar]:
        radars: List[Radar] = []
        p = self.center
        for d in [90, 45, 0, 315, 270]:  # [left front right]
            radar = Radar(origin=p)
            while self.map.get_at(radar.cell) != OUT_OF_STREET and radar.length < radar.max_len:
                deg = 360 - (self.angle + d)
                x = p.x + radar.length * math.cos(math.radians(deg))
                y = p.y + radar.length * math.sin(math.radians(deg))
                radar.update(Point(x, y))
            radars.append(radar)
        return radars

    def update(self):
        # Update distance and time the car has gone through
        self.distance += self.speed
        self.time_spent += 1

        # Collect and update car position
        self.rotate_surface = rot_center(self.surface, self.angle)
        self.pos = calculate_next_point(self.pos, self.angle, self.speed, 20, 20, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.center = Point(self.pos.x + 45, self.pos.y + 45)
        self.sensors = self.generate_sensors()
        self.radars = self.generate_radars()

        # Check if the car has collision
        for s in self.sensors:
            if self.map.get_at(s.cell) == OUT_OF_STREET:
                s.set_color(False)
                self.angle += 10
                self.is_alive = False
