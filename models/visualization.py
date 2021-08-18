import pygame
from .car import Car
from .libs import p2l

RED = (255, 0, 0)


class Visualization:
    def __init__(self, car: Car, screen):
        self.car = car
        self.screen = screen

    def draw_sensors(self):
        for s in self.car.sensors:
            pygame.draw.circle(self.screen, s.color, p2l(s.point), 5)

    def draw_radars(self):
        for r in self.car.radars:
            pygame.draw.line(self.screen, r.color, p2l(r.origin), p2l(r.target), 2)
            pygame.draw.circle(self.screen, r.color, p2l(r.target), 3)

    def draw(self):
        pygame.draw.circle(self.screen, RED, p2l(self.car.center), 5)
        self.draw_sensors()
        self.draw_radars()
