import pygame
import neat
from models import Car

screen_width = 1500
screen_height = 800

if __name__ == "__main__":
    # Init my game
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 70)
    font = pygame.font.SysFont("Arial", 30)
    map = pygame.image.load("assets/map.png")
    car = Car()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        screen.blit(map, (0, 0))
        screen.blit(car.surface, car.pos)
        pygame.display.flip()  # update the whole screen
        clock.tick(5)
