import pygame


class Car:
    def __init__(self):
        self.surface = pygame.image.load("assets/car.png")
        self.pos = [600, 675]
