import pygame
import math
from shapely.geometry import Point


def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def p2l(p: Point):
    return [p.x, p.y]


def calculate_next_point(p: Point, angle: float, distance: float,
                         width_min: float, height_min: float,
                         width_max: float, height_max: float) -> Point:
    # Calculate point, given point(x y), angle, and distance
    # e.g. x=5*cos(ɑ) y=5*sin(ɑ)
    x = p.x + distance * math.cos(math.radians(360 - angle))
    y = p.y + distance * math.sin(math.radians(360 - angle))
    # Check boundary
    x = width_min if x < width_min else x
    x = width_max - 260 if x > width_max - 260 else x
    y = height_min if y < height_min else y
    y = height_max - 120 if y > height_max - 120 else y
    return Point(x, y)
