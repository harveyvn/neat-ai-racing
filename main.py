import pygame
import neat
from models import Car, Visualization

screen_width = 1500
screen_height = 800

if __name__ == "__main__":
    # Init my game
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 70)
    font = pygame.font.SysFont("Arial", 30)
    map_game = pygame.image.load("assets/map_00.png")

    car = Car(map_game, "assets/car.png")
    viz = Visualization(car, screen)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        car.update()
        screen.blit(map_game, (0, 0))
        screen.blit(car.get_surface(), car.get_point())
        viz.draw()
        pygame.display.flip()  # update the whole screen
        clock.tick(10)
